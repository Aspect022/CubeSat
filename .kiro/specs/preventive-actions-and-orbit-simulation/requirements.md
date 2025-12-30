# Requirements Document

## Introduction

This feature enhances the SURAKSHASat system with two key capabilities: preventive action monitoring that detects telemetry trends before they become critical anomalies, and orbit pass simulation that calculates CubeSat visibility windows over Bangalore using real orbital mechanics. The preventive actions provide early warning capabilities while maintaining normal operations, and the orbit simulation enables ground station communication planning.

## Requirements

### Requirement 1: Preventive Action Monitoring

**User Story:** As a mission operator, I want the system to detect concerning telemetry trends before they become critical anomalies, so that I can take proactive measures while the satellite remains in normal operation.

#### Acceptance Criteria

1. WHEN battery_voltage_v decreases steadily over the last 5 samples AND voltage is still > 6.6V THEN the system SHALL log a preventive action: "Battery trending down: preparing safe mode"
2. WHEN payload_temp_c increases faster than 2°C per minute AND temperature is still < 45°C THEN the system SHALL log a preventive action: "Thermal increase detected: throttling payload"
3. WHEN rad_cps spikes above 10 cps AND radiation is still < 50 cps THEN the system SHALL log a preventive action: "Radiation levels rising: limiting comms temporarily"
4. WHEN preventive actions are triggered THEN the system SHALL NOT change the satellite mode from NORMAL
5. WHEN preventive actions are logged THEN they SHALL appear in the same timeline as anomalies and recoveries

### Requirement 2: Preventive Actions API Endpoint

**User Story:** As a frontend developer, I want to retrieve recent preventive actions via API, so that I can display them in the dashboard alongside anomalies and recoveries.

#### Acceptance Criteria

1. WHEN a GET request is made to /preventive/actions THEN the system SHALL return recent preventive actions in JSON format
2. WHEN preventive actions are returned THEN each action SHALL include timestamp, type, description, and telemetry data
3. WHEN no preventive actions exist THEN the system SHALL return an empty array

### Requirement 3: Frontend Preventive Actions Display

**User Story:** As a mission operator, I want to see preventive actions in the dashboard, so that I can monitor early warning indicators alongside critical anomalies.

#### Acceptance Criteria

1. WHEN preventive actions exist THEN they SHALL be displayed in the "Anomaly Flags & Recovery" card
2. WHEN displaying preventive actions THEN they SHALL use a ⚠️ icon and yellow highlight
3. WHEN preventive actions are shown THEN they SHALL be visually distinct from critical anomalies and recoveries

### Requirement 4: Orbit Pass Calculation

**User Story:** As a mission operator, I want to calculate CubeSat visibility passes over Bangalore, so that I can plan ground station communication windows.

#### Acceptance Criteria

1. WHEN orbit_pass.py is executed THEN it SHALL use Skyfield library with TLE data from Celestrak
2. IF internet connection is available THEN the system SHALL load TLE data from https://celestrak.org/NORAD/elements/stations.txt
3. IF internet is unavailable THEN the system SHALL fall back to a hardcoded mock TLE string for the ISS
4. WHEN calculating passes THEN the system SHALL use Bangalore coordinates: 12.9716°N, 77.5946°E, 0m elevation
5. WHEN orbit calculations complete THEN the system SHALL compute the next 3 visibility passes

### Requirement 5: Orbit Pass Data Output

**User Story:** As a mission operator, I want orbit pass data saved in multiple formats, so that I can analyze passes programmatically and visually.

#### Acceptance Criteria

1. WHEN orbit passes are calculated THEN the system SHALL save results to orbit_pass.csv with columns: start_time, end_time, duration
2. WHEN orbit passes are calculated THEN each pass SHALL include rise time, set time, and duration in seconds
3. WHEN orbit_pass.py runs THEN it SHALL print the 3 passes to console with human-readable format
4. WHEN orbit calculations complete THEN the system SHALL generate a matplotlib plot showing elevation vs time
5. WHEN the plot is generated THEN it SHALL show elevation curve for at least one pass and save as orbit_pass.png

### Requirement 6: Modular Architecture for Future AI Integration

**User Story:** As a developer, I want the preventive action system to be modular, so that I can later replace rule-based logic with AI-generated suggestions via Gemini API.

#### Acceptance Criteria

1. WHEN implementing preventive actions THEN the detection logic SHALL be separated from the action execution
2. WHEN designing the preventive system THEN it SHALL support pluggable detection strategies
3. WHEN preventive actions are triggered THEN the system SHALL use a consistent interface that can accommodate future AI integration

### Requirement 7: Standalone Orbit Simulation Script

**User Story:** As a mission operator, I want orbit_pass.py to run independently, so that I can generate orbit data without running the full CubeSat simulation system.

#### Acceptance Criteria

1. WHEN orbit_pass.py is executed directly THEN it SHALL run without dependencies on the main telemetry system
2. WHEN the script runs THEN it SHALL use clean, well-commented Python code
3. WHEN execution completes THEN all output files SHALL be generated in the current directory
4. WHEN the script encounters errors THEN it SHALL provide clear error messages and graceful fallbacks
