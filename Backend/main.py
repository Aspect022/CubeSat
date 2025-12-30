"""
SURAKSHASat FastAPI Application

FastAPI backend for the CubeSat telemetry simulation system.
Provides REST API endpoints for telemetry data, satellite mode, and fault injection.
"""

import asyncio
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from telemetry import (
    get_simulator, 
    run_telemetry_stream, 
    TelemetrySimulator, 
    SatelliteMode,
    TelemetryData
)

# Global simulator instance
simulator: Optional[TelemetrySimulator] = None

# Pydantic models for request/response
class FaultInjectionRequest(BaseModel):
    type: str = Field(..., description="Type of fault to inject")
    duration: float = Field(..., description="Duration of fault in seconds")

class FaultInjectionResponse(BaseModel):
    message: str
    fault_type: str
    duration: float
    telemetry: Dict[str, Any]

class TelemetryResponse(BaseModel):
    timestamp: datetime
    battery_voltage_v: float
    battery_current_a: float
    battery_soc_pct: float
    bus_5v_v: float
    bus_3v3_v: float
    solar_array_power_w: float
    payload_power_w: float
    eps_mode: str
    battery_temp_c: float
    obc_board_temp_c: float
    payload_temp_c: float
    panel_temp_c: float
    rad_cps: float
    mode: str
    fault_injected: bool

class CriticalTelemetryResponse(BaseModel):
    timestamp: datetime
    battery_voltage_v: float
    battery_soc_pct: float
    battery_temp_c: float
    obc_board_temp_c: float
    payload_temp_c: float
    mode: str
    fault_injected: bool

class EventLogResponse(BaseModel):
    timestamp: datetime
    type: str
    description: str
    data: Dict[str, Any]

class ModeResponse(BaseModel):
    mode: str
    timestamp: datetime

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - start and stop background tasks"""
    global simulator
    
    # Startup
    print("Starting SURAKSHASat telemetry simulator...")
    simulator = get_simulator()
    
    # Start the telemetry stream as a background task
    telemetry_task = asyncio.create_task(run_telemetry_stream(1.0))
    
    print("Telemetry simulator started successfully!")
    
    yield
    
    # Shutdown
    print("Shutting down telemetry simulator...")
    telemetry_task.cancel()
    try:
        await telemetry_task
    except asyncio.CancelledError:
        pass
    print("Telemetry simulator stopped.")

# Create FastAPI app with lifespan management
app = FastAPI(
    title="SURAKSHASat Telemetry API",
    description="REST API for CubeSat telemetry simulation and monitoring",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_simulator_instance() -> TelemetrySimulator:
    """Get the global simulator instance, raising error if not available"""
    if simulator is None:
        raise HTTPException(status_code=503, detail="Telemetry simulator not initialized")
    return simulator

def telemetry_to_dict(telemetry: TelemetryData) -> Dict[str, Any]:
    """Convert TelemetryData to dictionary for JSON serialization"""
    return {
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
        "mode": telemetry.mode.value,
        "fault_injected": telemetry.fault_injected
    }

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "SURAKSHASat Telemetry API",
        "version": "1.0.0",
        "endpoints": {
            "telemetry": "/telemetry/latest",
            "logs": "/telemetry/logs", 
            "mode": "/mode",
            "downlink": "/downlink",
            "fault_injection": "POST /simulate/fault",
            "recovery_status": "/recovery/status",
            "recovery_history": "/recovery/history",
            "health": "/health"
        }
    }

@app.get("/telemetry/latest", response_model=TelemetryResponse)
async def get_latest_telemetry():
    """
    Get the most recent telemetry reading as JSON.
    
    Returns complete telemetry data including all power, thermal, and radiation parameters.
    """
    sim = get_simulator_instance()
    telemetry = sim.get_latest_telemetry()
    return TelemetryResponse(**telemetry_to_dict(telemetry))

@app.get("/telemetry/logs", response_model=List[EventLogResponse])
async def get_telemetry_logs():
    """
    Get the event log (anomalies, recoveries, faults) as a JSON list.
    
    Returns all logged events including anomalies, mode changes, and fault injections.
    """
    sim = get_simulator_instance()
    events = sim.get_event_log()
    
    # Convert events to response format
    return [
        EventLogResponse(
            timestamp=event["timestamp"],
            type=event["type"],
            description=event["description"],
            data=event["data"]
        )
        for event in events
    ]

@app.get("/mode", response_model=ModeResponse)
async def get_satellite_mode():
    """
    Get the current satellite mode (NORMAL, SAFE, RECOVERED).
    
    Returns the current operational mode of the satellite.
    """
    sim = get_simulator_instance()
    return ModeResponse(
        mode=sim.current_mode.value,
        timestamp=datetime.now(timezone.utc)
    )

@app.get("/downlink")
async def get_downlink_data():
    """
    Get telemetry according to data prioritization rules:
    - NORMAL → return all telemetry fields
    - SAFE → return only critical telemetry (battery_voltage_v, battery_soc_pct, battery_temp_c, obc_board_temp_c, payload_temp_c)
    
    Returns telemetry data filtered based on current satellite mode.
    """
    sim = get_simulator_instance()
    telemetry = sim.get_latest_telemetry()
    
    if sim.current_mode == SatelliteMode.NORMAL:
        # Return all telemetry data
        return telemetry_to_dict(telemetry)
    elif sim.current_mode == SatelliteMode.SAFE:
        # Return only critical telemetry
        return CriticalTelemetryResponse(
            timestamp=telemetry.timestamp,
            battery_voltage_v=telemetry.battery_voltage_v,
            battery_soc_pct=telemetry.battery_soc_pct,
            battery_temp_c=telemetry.battery_temp_c,
            obc_board_temp_c=telemetry.obc_board_temp_c,
            payload_temp_c=telemetry.payload_temp_c,
            mode=telemetry.mode.value,
            fault_injected=telemetry.fault_injected
        )
    else:  # RECOVERED mode - return all data like NORMAL
        return telemetry_to_dict(telemetry)

@app.post("/simulate/fault", response_model=FaultInjectionResponse)
async def inject_fault(request: FaultInjectionRequest):
    """
    Inject a fault into the simulator.
    
    Accepts JSON with fault type and duration to simulate various failure scenarios.
    Returns confirmation and updated telemetry data.
    """
    sim = get_simulator_instance()
    
    # Validate fault type
    valid_fault_types = ["LOW_VOLTAGE", "HIGH_TEMP", "RADIATION_SPIKE", "POWER_FAILURE"]
    if request.type not in valid_fault_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid fault type. Must be one of: {', '.join(valid_fault_types)}"
        )
    
    # Validate duration
    if request.duration <= 0 or request.duration > 3600:  # Max 1 hour
        raise HTTPException(
            status_code=400,
            detail="Duration must be between 0 and 3600 seconds"
        )
    
    # Inject the fault
    sim.inject_fault(request.type, request.duration)
    
    # Get updated telemetry
    telemetry = sim.get_latest_telemetry()
    
    return FaultInjectionResponse(
        message=f"Fault '{request.type}' injected for {request.duration} seconds",
        fault_type=request.type,
        duration=request.duration,
        telemetry=telemetry_to_dict(telemetry)
    )

@app.get("/recovery/status")
async def get_recovery_status():
    """
    Get current recovery engine status.
    
    Returns information about active recovery actions and mode transitions.
    """
    sim = get_simulator_instance()
    
    try:
        from recovery import get_recovery_engine
        recovery_engine = get_recovery_engine(sim)
        return recovery_engine.get_recovery_status()
    except ImportError:
        return {
            "current_mode": sim.current_mode.value,
            "recovery_active": False,
            "recovery_start_time": None,
            "active_recovery": None,
            "recovery_history_count": 0
        }

@app.get("/recovery/history")
async def get_recovery_history():
    """
    Get recovery history.
    
    Returns list of past recovery actions and their outcomes.
    """
    sim = get_simulator_instance()
    
    try:
        from recovery import get_recovery_engine
        recovery_engine = get_recovery_engine(sim)
        return recovery_engine.get_recovery_history()
    except ImportError:
        return []

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    sim = get_simulator_instance()
    return {
        "status": "healthy",
        "simulator_running": sim is not None,
        "current_mode": sim.current_mode.value if sim else "unknown",
        "timestamp": datetime.now(timezone.utc)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)