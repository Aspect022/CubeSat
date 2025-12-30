"""
SURAKSHASat Telemetry Simulator

Generates synthetic CubeSat telemetry in real time with:
- Sun/eclipse cycles affecting power generation
- Thermal lag modeling for temperature parameters
- Occasional radiation spikes
- Fault injection capabilities
"""

import asyncio
import time
import random
import math
from datetime import datetime, timezone
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SatelliteMode(Enum):
    """Satellite operational modes"""
    NORMAL = "NORMAL"
    SAFE = "SAFE"
    RECOVERED = "RECOVERED"


@dataclass
class TelemetryData:
    """Telemetry data structure"""
    timestamp: datetime
    # Power/EPS parameters
    battery_voltage_v: float
    battery_current_a: float
    battery_soc_pct: float
    bus_5v_v: float
    bus_3v3_v: float
    solar_array_power_w: float
    payload_power_w: float
    eps_mode: str
    
    # Thermal parameters
    battery_temp_c: float
    obc_board_temp_c: float
    payload_temp_c: float
    panel_temp_c: float
    
    # Radiation
    rad_cps: float
    
    # Operational state
    mode: SatelliteMode
    fault_injected: bool = False


@dataclass
class HealthyRanges:
    """Healthy operating ranges for telemetry parameters"""
    battery_voltage_v: tuple = (6.6, 8.4)
    battery_soc_pct: tuple = (20, 100)
    battery_temp_c: tuple = (-5, 45)
    obc_board_temp_c: tuple = (0, 60)
    payload_temp_c: tuple = (-10, 55)
    panel_temp_c: tuple = (-50, 60)
    rad_cps: tuple = (0.1, 5)  # Normal range, spikes allowed to 80
    bus_5v_v: tuple = (4.9, 5.1)
    bus_3v3_v: tuple = (3.25, 3.40)


class TelemetrySimulator:
    """
    Real-time CubeSat telemetry simulator with orbital mechanics,
    thermal modeling, and fault injection capabilities.
    """
    
    def __init__(self, orbital_period_minutes: float = 90.0):
        """
        Initialize the telemetry simulator.
        
        Args:
            orbital_period_minutes: Orbital period in minutes (default 90 min for LEO)
        """
        self.orbital_period = orbital_period_minutes * 60  # Convert to seconds
        self.sun_eclipse_ratio = 0.6  # 60% sun, 40% eclipse
        self.healthy_ranges = HealthyRanges()
        
        # Simulation state
        self.start_time = time.time()
        self.current_mode = SatelliteMode.NORMAL
        self.fault_active = False
        self.fault_type = None
        
        # Thermal state (for lag modeling)
        self.thermal_state = {
            'battery_temp_c': 20.0,
            'obc_board_temp_c': 25.0,
            'payload_temp_c': 22.0,
            'panel_temp_c': -20.0
        }
        
        # Thermal time constants (seconds)
        self.thermal_constants = {
            'battery_temp_c': 300.0,      # 5 minutes
            'obc_board_temp_c': 180.0,    # 3 minutes
            'payload_temp_c': 240.0,      # 4 minutes
            'panel_temp_c': 60.0          # 1 minute (fastest)
        }
        
        # Radiation spike parameters
        self.radiation_spike_probability = 0.001  # 0.1% chance per update
        self.radiation_spike_duration = 30.0      # 30 seconds
        self.radiation_spike_start = None
        
        # Callbacks for external systems
        self.telemetry_callbacks: List[Callable[[TelemetryData], None]] = []
        
        # Event log
        self.event_log: List[Dict] = []
        
        logger.info(f"Telemetry simulator initialized with {orbital_period_minutes} min orbital period")
    
    def add_telemetry_callback(self, callback: Callable[[TelemetryData], None]):
        """Add a callback function to be called when new telemetry is generated"""
        self.telemetry_callbacks.append(callback)
    
    def log_event(self, event_type: str, description: str, data: Optional[Dict] = None):
        """Log an event to the event timeline"""
        event = {
            'timestamp': datetime.now(timezone.utc),
            'type': event_type,
            'description': description,
            'data': data or {}
        }
        self.event_log.append(event)
        logger.info(f"Event: {event_type} - {description}")
    
    def get_orbital_phase(self) -> float:
        """
        Get current orbital phase (0.0 = eclipse start, 0.5 = sun start, 1.0 = eclipse start again)
        """
        elapsed = time.time() - self.start_time
        phase = (elapsed % self.orbital_period) / self.orbital_period
        return phase
    
    def is_in_sunlight(self) -> bool:
        """Determine if satellite is currently in sunlight"""
        phase = self.get_orbital_phase()
        return phase < self.sun_eclipse_ratio
    
    def get_solar_irradiance_factor(self) -> float:
        """
        Get solar irradiance factor based on orbital position.
        Returns 0.0 in eclipse, 1.0 at peak sun, with smooth transitions.
        """
        phase = self.get_orbital_phase()
        
        if not self.is_in_sunlight():
            return 0.0
        
        # Smooth transition from eclipse to sun and back
        if phase < 0.1:  # Transitioning from eclipse to sun
            return phase / 0.1
        elif phase > self.sun_eclipse_ratio - 0.1:  # Transitioning from sun to eclipse
            return (self.sun_eclipse_ratio - phase) / 0.1
        else:  # In full sunlight
            return 1.0
    
    def update_thermal_state(self, target_temps: Dict[str, float], dt: float):
        """
        Update thermal state with lag modeling using exponential approach.
        
        Args:
            target_temps: Target temperatures for each component
            dt: Time step in seconds
        """
        for component, target_temp in target_temps.items():
            if component in self.thermal_state:
                current_temp = self.thermal_state[component]
                tau = self.thermal_constants[component]
                
                # Exponential approach to target temperature
                alpha = 1 - math.exp(-dt / tau)
                self.thermal_state[component] = current_temp + alpha * (target_temp - current_temp)
    
    def generate_radiation_spike(self) -> float:
        """Generate radiation spike if conditions are met"""
        current_time = time.time()
        
        # Check if we should start a new spike
        if (self.radiation_spike_start is None and 
            random.random() < self.radiation_spike_probability):
            self.radiation_spike_start = current_time
            self.log_event("RADIATION_SPIKE", "Radiation spike detected", 
                          {"spike_start": current_time})
        
        # Check if we're in an active spike
        if (self.radiation_spike_start is not None and 
            current_time - self.radiation_spike_start < self.radiation_spike_duration):
            # Generate spike with random intensity (10-80 cps)
            return random.uniform(10.0, 80.0)
        else:
            # End the spike
            if self.radiation_spike_start is not None:
                self.log_event("RADIATION_SPIKE_END", "Radiation spike ended")
                self.radiation_spike_start = None
            
            # Normal radiation levels
            return random.uniform(0.1, 5.0)
    
    def inject_fault(self, fault_type: str, duration: float = 60.0):
        """
        Inject a fault into the telemetry simulation.
        
        Args:
            fault_type: Type of fault to inject
            duration: Duration of fault in seconds
        """
        self.fault_active = True
        self.fault_type = fault_type
        self.log_event("FAULT_INJECTED", f"Fault injected: {fault_type}", 
                      {"fault_type": fault_type, "duration": duration})
        
        # Schedule fault removal
        asyncio.create_task(self._remove_fault_after_delay(duration))
    
    async def _remove_fault_after_delay(self, delay: float):
        """Remove fault after specified delay"""
        await asyncio.sleep(delay)
        self.fault_active = False
        self.fault_type = None
        self.log_event("FAULT_REMOVED", "Injected fault removed")
    
    def generate_telemetry(self) -> TelemetryData:
        """Generate a single telemetry data point"""
        current_time = datetime.now(timezone.utc)
        solar_factor = self.get_solar_irradiance_factor()
        is_sunlight = self.is_in_sunlight()
        
        # Base power parameters
        base_battery_voltage = 7.5
        base_battery_soc = 75.0
        base_solar_power = 8.0  # Watts
        
        # Apply solar cycle effects
        solar_array_power = base_solar_power * solar_factor
        battery_charging = solar_array_power > 2.0  # Charging if significant solar power
        
        # Battery voltage and SOC with charging/discharging
        if battery_charging:
            battery_voltage = base_battery_voltage + random.uniform(0.1, 0.3)
            battery_soc = min(100.0, base_battery_soc + random.uniform(0.5, 2.0))
        else:
            battery_voltage = base_battery_voltage - random.uniform(0.1, 0.4)
            battery_soc = max(20.0, base_battery_soc - random.uniform(0.2, 1.0))
        
        # Battery current (positive = charging, negative = discharging)
        if battery_charging:
            battery_current = random.uniform(0.1, 0.5)
        else:
            battery_current = -random.uniform(0.2, 0.8)
        
        # Bus voltages (regulated, stable)
        bus_5v = 5.0 + random.uniform(-0.05, 0.05)
        bus_3v3 = 3.3 + random.uniform(-0.02, 0.02)
        
        # Payload power consumption
        if self.current_mode == SatelliteMode.SAFE:
            payload_power = random.uniform(0.5, 1.0)  # Reduced power in safe mode
        else:
            payload_power = random.uniform(2.0, 4.0)  # Normal operation
        
        # EPS mode
        if battery_soc < 30:
            eps_mode = "LOW_POWER"
        elif battery_soc > 90:
            eps_mode = "FULL_CHARGE"
        else:
            eps_mode = "NORMAL"
        
        # Target temperatures based on solar exposure and mode
        if is_sunlight:
            # Sun-facing side gets hot
            target_panel_temp = random.uniform(40, 60)
            target_battery_temp = random.uniform(25, 35)
            target_obc_temp = random.uniform(30, 45)
            target_payload_temp = random.uniform(25, 40)
        else:
            # Eclipse side gets cold
            target_panel_temp = random.uniform(-40, -20)
            target_battery_temp = random.uniform(5, 15)
            target_obc_temp = random.uniform(10, 25)
            target_payload_temp = random.uniform(5, 20)
        
        # Apply thermal lag
        target_temps = {
            'battery_temp_c': target_battery_temp,
            'obc_board_temp_c': target_obc_temp,
            'payload_temp_c': target_payload_temp,
            'panel_temp_c': target_panel_temp
        }
        
        # Update thermal state (assuming 1-second update interval)
        self.update_thermal_state(target_temps, 1.0)
        
        # Generate radiation
        rad_cps = self.generate_radiation_spike()
        
        # Apply fault injection
        fault_injected = False
        if self.fault_active:
            fault_injected = True
            if self.fault_type == "LOW_VOLTAGE":
                battery_voltage *= 0.7  # 30% voltage drop
                battery_soc *= 0.6      # 40% SOC drop
            elif self.fault_type == "HIGH_TEMP":
                self.thermal_state['battery_temp_c'] += 20
                self.thermal_state['obc_board_temp_c'] += 25
            elif self.fault_type == "RADIATION_SPIKE":
                rad_cps = random.uniform(50, 100)
            elif self.fault_type == "POWER_FAILURE":
                battery_voltage *= 0.5
                solar_array_power *= 0.3
                payload_power *= 0.2
        
        # Create telemetry data
        telemetry = TelemetryData(
            timestamp=current_time,
            battery_voltage_v=round(battery_voltage, 2),
            battery_current_a=round(battery_current, 3),
            battery_soc_pct=round(battery_soc, 1),
            bus_5v_v=round(bus_5v, 2),
            bus_3v3_v=round(bus_3v3, 2),
            solar_array_power_w=round(solar_array_power, 2),
            payload_power_w=round(payload_power, 2),
            eps_mode=eps_mode,
            battery_temp_c=round(self.thermal_state['battery_temp_c'], 1),
            obc_board_temp_c=round(self.thermal_state['obc_board_temp_c'], 1),
            payload_temp_c=round(self.thermal_state['payload_temp_c'], 1),
            panel_temp_c=round(self.thermal_state['panel_temp_c'], 1),
            rad_cps=round(rad_cps, 2),
            mode=self.current_mode,
            fault_injected=fault_injected
        )
        
        return telemetry
    
    def set_mode(self, mode: SatelliteMode):
        """Set the satellite operational mode"""
        if mode != self.current_mode:
            self.log_event("MODE_CHANGE", f"Mode changed from {self.current_mode.value} to {mode.value}")
            self.current_mode = mode
    
    def get_latest_telemetry(self) -> TelemetryData:
        """Get the latest telemetry data with recovery processing"""
        # Generate base telemetry
        telemetry = self.generate_telemetry()
        
        # Process through recovery engine if available
        try:
            from recovery import get_recovery_engine
            recovery_engine = get_recovery_engine(self)
            telemetry = recovery_engine.process_telemetry(telemetry)
            # Update current mode to match recovery engine
            self.current_mode = recovery_engine.current_mode
        except ImportError:
            # Recovery engine not available, use base telemetry
            pass
        
        return telemetry
    
    def get_event_log(self, limit: Optional[int] = None) -> List[Dict]:
        """Get the event log, optionally limited to recent entries"""
        if limit:
            return self.event_log[-limit:]
        return self.event_log.copy()
    
    def check_anomalies(self, telemetry: TelemetryData) -> List[str]:
        """
        Check telemetry against healthy ranges and return list of anomalies.
        
        Args:
            telemetry: Telemetry data to check
            
        Returns:
            List of anomaly descriptions
        """
        anomalies = []
        
        # Check each parameter against healthy ranges
        checks = [
            ('battery_voltage_v', telemetry.battery_voltage_v, self.healthy_ranges.battery_voltage_v),
            ('battery_soc_pct', telemetry.battery_soc_pct, self.healthy_ranges.battery_soc_pct),
            ('battery_temp_c', telemetry.battery_temp_c, self.healthy_ranges.battery_temp_c),
            ('obc_board_temp_c', telemetry.obc_board_temp_c, self.healthy_ranges.obc_board_temp_c),
            ('payload_temp_c', telemetry.payload_temp_c, self.healthy_ranges.payload_temp_c),
            ('panel_temp_c', telemetry.panel_temp_c, self.healthy_ranges.panel_temp_c),
            ('bus_5v_v', telemetry.bus_5v_v, self.healthy_ranges.bus_5v_v),
            ('bus_3v3_v', telemetry.bus_3v3_v, self.healthy_ranges.bus_3v3_v),
        ]
        
        for param_name, value, (min_val, max_val) in checks:
            if value < min_val or value > max_val:
                anomalies.append(f"{param_name} out of range: {value} (healthy: {min_val}-{max_val})")
        
        # Special check for radiation (allow spikes up to 80 cps)
        if telemetry.rad_cps > 80:
            anomalies.append(f"radiation spike too high: {telemetry.rad_cps} cps (max allowed: 80)")
        
        return anomalies


# Global simulator instance
_simulator_instance: Optional[TelemetrySimulator] = None


def get_simulator() -> TelemetrySimulator:
    """Get the global telemetry simulator instance"""
    global _simulator_instance
    if _simulator_instance is None:
        _simulator_instance = TelemetrySimulator()
    return _simulator_instance


async def run_telemetry_stream(update_interval: float = 1.0):
    """
    Run the telemetry stream in the background.
    
    Args:
        update_interval: Time between telemetry updates in seconds
    """
    simulator = get_simulator()
    
    # Import recovery engine here to avoid circular imports
    from recovery import get_recovery_engine
    recovery_engine = get_recovery_engine(simulator)
    
    while True:
        try:
            # Generate new telemetry
            telemetry = simulator.generate_telemetry()
            
            # Process telemetry through recovery engine
            telemetry = recovery_engine.process_telemetry(telemetry)
            
            # Update simulator's current mode to match recovery engine
            simulator.current_mode = recovery_engine.current_mode
            
            # Call all registered callbacks
            for callback in simulator.telemetry_callbacks:
                try:
                    callback(telemetry)
                except Exception as e:
                    logger.error(f"Error in telemetry callback: {e}")
            
            await asyncio.sleep(update_interval)
            
        except Exception as e:
            logger.error(f"Error in telemetry stream: {e}")
            await asyncio.sleep(update_interval)


if __name__ == "__main__":
    # Example usage and testing
    async def main():
        simulator = get_simulator()
        
        # Add a simple callback to print telemetry
        def print_telemetry(telemetry: TelemetryData):
            print(f"[{telemetry.timestamp}] Mode: {telemetry.mode.value}, "
                  f"Battery: {telemetry.battery_voltage_v}V ({telemetry.battery_soc_pct}%), "
                  f"Solar: {telemetry.solar_array_power_w}W, "
                  f"Radiation: {telemetry.rad_cps} cps")
        
        simulator.add_telemetry_callback(print_telemetry)
        
        # Inject a test fault after 10 seconds
        asyncio.create_task(simulator.inject_fault("LOW_VOLTAGE", 30.0))
        
        # Run the telemetry stream
        await run_telemetry_stream(1.0)
    
    # Run the example
    asyncio.run(main())