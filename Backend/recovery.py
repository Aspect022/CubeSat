"""
SURAKSHASat Recovery Logic Module

Implements autonomous recovery strategies for CubeSat anomalies.
Manages mode state machine and applies corrective actions based on detected anomalies.
"""

import asyncio
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Callable
from enum import Enum
from dataclasses import dataclass
import logging

from telemetry import SatelliteMode, TelemetryData, TelemetrySimulator

logger = logging.getLogger(__name__)


class RecoveryAction(Enum):
    """Types of recovery actions that can be applied"""
    MODE_CHANGE = "MODE_CHANGE"
    PAYLOAD_SHUTDOWN = "PAYLOAD_SHUTDOWN"
    SUN_POINTING = "SUN_POINTING"
    SYSTEM_THROTTLING = "SYSTEM_THROTTLING"
    POWER_REDUCTION = "POWER_REDUCTION"


@dataclass
class RecoveryStrategy:
    """Defines a recovery strategy for a specific anomaly type"""
    anomaly_type: str
    target_mode: SatelliteMode
    actions: List[RecoveryAction]
    description: str
    recovery_duration: float = 60.0  # How long to stay in recovery mode


class RecoveryEngine:
    """
    Autonomous recovery engine for CubeSat anomalies.
    Manages mode state machine and applies recovery strategies.
    """
    
    def __init__(self, simulator: TelemetrySimulator):
        """
        Initialize the recovery engine.
        
        Args:
            simulator: Reference to the telemetry simulator
        """
        self.simulator = simulator
        self.current_mode = SatelliteMode.NORMAL
        self.recovery_active = False
        self.recovery_start_time = None
        self.last_anomaly_check = time.time()
        
        # Recovery strategies for different anomaly types
        self.recovery_strategies = self._initialize_recovery_strategies()
        
        # Recovery state tracking
        self.active_recovery = None
        self.recovery_history: List[Dict] = []
        
        # Mode transition callbacks
        self.mode_change_callbacks: List[Callable[[SatelliteMode, SatelliteMode], None]] = []
        
        logger.info("Recovery engine initialized")
    
    def _initialize_recovery_strategies(self) -> Dict[str, RecoveryStrategy]:
        """Initialize recovery strategies for different anomaly types"""
        strategies = {
            "LOW_VOLTAGE": RecoveryStrategy(
                anomaly_type="LOW_VOLTAGE",
                target_mode=SatelliteMode.SAFE,
                actions=[RecoveryAction.MODE_CHANGE, RecoveryAction.SUN_POINTING, RecoveryAction.PAYLOAD_SHUTDOWN],
                description="Power drop detected - switching to safe mode with sun pointing",
                recovery_duration=120.0
            ),
            "HIGH_TEMP": RecoveryStrategy(
                anomaly_type="HIGH_TEMP",
                target_mode=SatelliteMode.SAFE,
                actions=[RecoveryAction.MODE_CHANGE, RecoveryAction.PAYLOAD_SHUTDOWN],
                description="Thermal spike detected - shutting down payload",
                recovery_duration=90.0
            ),
            "RADIATION_SPIKE": RecoveryStrategy(
                anomaly_type="RADIATION_SPIKE",
                target_mode=SatelliteMode.SAFE,
                actions=[RecoveryAction.MODE_CHANGE, RecoveryAction.SYSTEM_THROTTLING],
                description="Radiation spike detected - throttling system",
                recovery_duration=60.0
            ),
            "POWER_FAILURE": RecoveryStrategy(
                anomaly_type="POWER_FAILURE",
                target_mode=SatelliteMode.SAFE,
                actions=[RecoveryAction.MODE_CHANGE, RecoveryAction.SUN_POINTING, RecoveryAction.PAYLOAD_SHUTDOWN, RecoveryAction.POWER_REDUCTION],
                description="Power failure detected - emergency safe mode",
                recovery_duration=180.0
            )
        }
        return strategies
    
    def add_mode_change_callback(self, callback: Callable[[SatelliteMode, SatelliteMode], None]):
        """Add a callback for mode changes"""
        self.mode_change_callbacks.append(callback)
    
    def set_mode(self, new_mode: SatelliteMode, reason: str = ""):
        """
        Set the satellite mode with proper logging and callbacks.
        
        Args:
            new_mode: Target mode
            reason: Reason for mode change
        """
        if new_mode != self.current_mode:
            old_mode = self.current_mode
            self.current_mode = new_mode
            
            # Log mode change
            self.simulator.log_event(
                "MODE_CHANGE", 
                f"Mode changed from {old_mode.value} to {new_mode.value}" + (f" - {reason}" if reason else ""),
                {
                    "old_mode": old_mode.value,
                    "new_mode": new_mode.value,
                    "reason": reason
                }
            )
            
            # Call mode change callbacks
            for callback in self.mode_change_callbacks:
                try:
                    callback(old_mode, new_mode)
                except Exception as e:
                    logger.error(f"Error in mode change callback: {e}")
            
            logger.info(f"Mode changed: {old_mode.value} → {new_mode.value} ({reason})")
    
    def apply_recovery_strategy(self, anomaly_type: str, anomalies: List[str]) -> bool:
        """
        Apply recovery strategy for detected anomalies.
        
        Args:
            anomaly_type: Type of anomaly detected
            anomalies: List of specific anomaly descriptions
            
        Returns:
            True if recovery strategy was applied, False otherwise
        """
        if anomaly_type not in self.recovery_strategies:
            logger.warning(f"No recovery strategy defined for anomaly type: {anomaly_type}")
            return False
        
        strategy = self.recovery_strategies[anomaly_type]
        
        # Don't apply recovery if already in the target mode
        if self.current_mode == strategy.target_mode:
            logger.debug(f"Already in {strategy.target_mode.value} mode, skipping recovery")
            return False
        
        logger.info(f"Applying recovery strategy for {anomaly_type}: {strategy.description}")
        
        # Apply each action in the strategy
        for action in strategy.actions:
            self._apply_recovery_action(action, strategy)
        
        # Set recovery state
        self.recovery_active = True
        self.recovery_start_time = time.time()
        self.active_recovery = {
            "strategy": strategy,
            "start_time": self.recovery_start_time,
            "anomalies": anomalies
        }
        
        # Log recovery action
        self.simulator.log_event(
            "RECOVERY_APPLIED",
            f"Recovery strategy applied: {strategy.description}",
            {
                "anomaly_type": anomaly_type,
                "strategy": strategy.description,
                "actions": [action.value for action in strategy.actions],
                "target_mode": strategy.target_mode.value,
                "anomalies": anomalies
            }
        )
        
        return True
    
    def _apply_recovery_action(self, action: RecoveryAction, strategy: RecoveryStrategy):
        """Apply a specific recovery action"""
        if action == RecoveryAction.MODE_CHANGE:
            self.set_mode(strategy.target_mode, f"Recovery for {strategy.anomaly_type}")
        
        elif action == RecoveryAction.SUN_POINTING:
            # Set EPS mode to sun pointing
            self.simulator.log_event(
                "RECOVERY_ACTION",
                "EPS mode set to SUN_POINT for power recovery",
                {"action": "SUN_POINTING"}
            )
        
        elif action == RecoveryAction.PAYLOAD_SHUTDOWN:
            # Payload shutdown is handled in telemetry generation
            self.simulator.log_event(
                "RECOVERY_ACTION",
                "Payload shutdown initiated for thermal/power safety",
                {"action": "PAYLOAD_SHUTDOWN"}
            )
        
        elif action == RecoveryAction.SYSTEM_THROTTLING:
            # System throttling is handled in telemetry generation
            self.simulator.log_event(
                "RECOVERY_ACTION",
                "System throttling initiated for radiation protection",
                {"action": "SYSTEM_THROTTLING"}
            )
        
        elif action == RecoveryAction.POWER_REDUCTION:
            # Power reduction is handled in telemetry generation
            self.simulator.log_event(
                "RECOVERY_ACTION",
                "Power reduction initiated for emergency power management",
                {"action": "POWER_REDUCTION"}
            )
    
    def check_mode_recovery(self, telemetry: TelemetryData) -> bool:
        """
        Check if conditions are met to recover from SAFE mode.
        
        Args:
            telemetry: Current telemetry data
            
        Returns:
            True if mode recovery was applied, False otherwise
        """
        if not self.recovery_active or not self.active_recovery:
            return False
        
        # Check if recovery duration has passed
        recovery_duration = time.time() - self.recovery_start_time
        strategy = self.active_recovery["strategy"]
        
        if recovery_duration < strategy.recovery_duration:
            return False
        
        # Check if anomalies have cleared
        anomalies = self.simulator.check_anomalies(telemetry)
        if anomalies:
            logger.debug(f"Anomalies still present: {anomalies}, staying in {self.current_mode.value} mode")
            return False
        
        # Anomalies have cleared, start recovery sequence
        self._apply_mode_recovery()
        return True
    
    def _apply_mode_recovery(self):
        """Apply mode recovery sequence: SAFE → RECOVERED → NORMAL"""
        if self.current_mode == SatelliteMode.SAFE:
            # Transition to RECOVERED
            self.set_mode(SatelliteMode.RECOVERED, "Anomalies cleared, entering recovery phase")
            
            # Schedule transition to NORMAL after a delay
            asyncio.create_task(self._schedule_normal_mode_transition())
            
        elif self.current_mode == SatelliteMode.RECOVERED:
            # This shouldn't happen as we schedule the transition
            logger.warning("Unexpected RECOVERED mode state")
    
    async def _schedule_normal_mode_transition(self):
        """Schedule transition from RECOVERED to NORMAL mode"""
        # Wait 30 seconds in RECOVERED mode
        await asyncio.sleep(30.0)
        
        if self.current_mode == SatelliteMode.RECOVERED:
            self.set_mode(SatelliteMode.NORMAL, "Recovery phase complete, resuming normal operations")
            self._clear_recovery_state()
    
    def _clear_recovery_state(self):
        """Clear recovery state and return to normal operations"""
        if self.active_recovery:
            recovery_duration = time.time() - self.recovery_start_time
            
            self.simulator.log_event(
                "RECOVERY_COMPLETE",
                f"Recovery completed successfully after {recovery_duration:.1f} seconds",
                {
                    "recovery_duration": recovery_duration,
                    "final_mode": self.current_mode.value,
                    "strategy": self.active_recovery["strategy"].description
                }
            )
            
            # Add to recovery history
            self.recovery_history.append({
                "timestamp": datetime.now(timezone.utc),
                "strategy": self.active_recovery["strategy"].anomaly_type,
                "duration": recovery_duration,
                "success": True
            })
        
        self.recovery_active = False
        self.recovery_start_time = None
        self.active_recovery = None
    
    def detect_anomaly_type(self, anomalies: List[str]) -> Optional[str]:
        """
        Detect the primary anomaly type from a list of anomalies.
        
        Args:
            anomalies: List of anomaly descriptions
            
        Returns:
            Primary anomaly type or None if no specific type detected
        """
        # Check for specific anomaly patterns
        for anomaly in anomalies:
            if "battery_voltage_v" in anomaly and ("out of range" in anomaly or "low" in anomaly.lower()):
                return "LOW_VOLTAGE"
            elif "temp_c" in anomaly and "out of range" in anomaly:
                return "HIGH_TEMP"
            elif "radiation" in anomaly.lower() and "spike" in anomaly.lower():
                return "RADIATION_SPIKE"
            elif "power" in anomaly.lower() and ("failure" in anomaly.lower() or "low" in anomaly.lower()):
                return "POWER_FAILURE"
        
        # Check for fault injection types
        if self.simulator.fault_active and self.simulator.fault_type:
            return self.simulator.fault_type
        
        return None
    
    def process_telemetry(self, telemetry: TelemetryData) -> TelemetryData:
        """
        Process telemetry data and apply recovery actions if needed.
        
        Args:
            telemetry: Current telemetry data
            
        Returns:
            Modified telemetry data with recovery actions applied
        """
        # Check for anomalies
        anomalies = self.simulator.check_anomalies(telemetry)
        
        # Apply recovery strategies if anomalies detected
        if anomalies:
            anomaly_type = self.detect_anomaly_type(anomalies)
            if anomaly_type:
                self.apply_recovery_strategy(anomaly_type, anomalies)
        
        # Check for mode recovery
        self.check_mode_recovery(telemetry)
        
        # Apply recovery actions to telemetry
        modified_telemetry = self._apply_recovery_to_telemetry(telemetry)
        
        return modified_telemetry
    
    def _apply_recovery_to_telemetry(self, telemetry: TelemetryData) -> TelemetryData:
        """
        Apply recovery actions to telemetry data.
        
        Args:
            telemetry: Original telemetry data
            
        Returns:
            Modified telemetry data with recovery actions applied
        """
        # Create a copy of telemetry data
        modified_data = {
            "timestamp": telemetry.timestamp,
            "battery_voltage_v": telemetry.battery_voltage_v,
            "battery_current_a": telemetry.battery_current_a,
            "battery_soc_pct": telemetry.battery_soc_pct,
            "bus_5v_v": telemetry.bus_5v_v,
            "bus_3v3_v": telemetry.bus_3v3_v,
            "solar_array_power_w": telemetry.solar_array_power_w,
            "payload_power_w": telemetry.payload_power_w,
            "eps_mode": telemetry.eps_mode,
            "battery_temp_c": telemetry.battery_temp_c,
            "obc_board_temp_c": telemetry.obc_board_temp_c,
            "payload_temp_c": telemetry.payload_temp_c,
            "panel_temp_c": telemetry.panel_temp_c,
            "rad_cps": telemetry.rad_cps,
            "mode": self.current_mode,  # Use recovery engine's mode
            "fault_injected": telemetry.fault_injected
        }
        
        # Apply recovery actions based on current mode and active recovery
        if self.current_mode == SatelliteMode.SAFE:
            # Payload shutdown in safe mode
            modified_data["payload_power_w"] = 0.0
            
            # Sun pointing for power recovery
            if self.active_recovery and "SUN_POINTING" in [action.value for action in self.active_recovery["strategy"].actions]:
                modified_data["eps_mode"] = "SUN_POINT"
            
            # System throttling for radiation protection
            if self.active_recovery and "SYSTEM_THROTTLING" in [action.value for action in self.active_recovery["strategy"].actions]:
                modified_data["solar_array_power_w"] *= 0.5  # 50% reduction
            
            # Power reduction for emergency power management
            if self.active_recovery and "POWER_REDUCTION" in [action.value for action in self.active_recovery["strategy"].actions]:
                modified_data["solar_array_power_w"] *= 0.3  # 70% reduction
                modified_data["payload_power_w"] = 0.0
        
        # Create new TelemetryData object
        return TelemetryData(**modified_data)
    
    def get_recovery_status(self) -> Dict[str, Any]:
        """Get current recovery status"""
        return {
            "current_mode": self.current_mode.value,
            "recovery_active": self.recovery_active,
            "recovery_start_time": self.recovery_start_time,
            "active_recovery": self.active_recovery["strategy"].anomaly_type if self.active_recovery else None,
            "recovery_history_count": len(self.recovery_history)
        }
    
    def get_recovery_history(self) -> List[Dict]:
        """Get recovery history"""
        return self.recovery_history.copy()


# Global recovery engine instance
_recovery_engine_instance: Optional[RecoveryEngine] = None


def get_recovery_engine(simulator: TelemetrySimulator) -> RecoveryEngine:
    """Get the global recovery engine instance"""
    global _recovery_engine_instance
    if _recovery_engine_instance is None:
        _recovery_engine_instance = RecoveryEngine(simulator)
    return _recovery_engine_instance