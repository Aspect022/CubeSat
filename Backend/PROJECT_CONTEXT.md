# SURAKSHASat – Hackathon MVP

**Goal:**  
Build a software-only simulation of an autonomous CubeSat self-healing system.  
The MVP demonstrates how a CubeSat can autonomously detect anomalies and apply recovery strategies, going beyond traditional "safe mode."  

---

## Core MVP Features
1. **Simulated Telemetry Stream**
   - Real-time synthetic CubeSat telemetry.
   - Parameters:
     - Power/EPS: `battery_voltage_v`, `battery_current_a`, `battery_soc_pct`, `bus_5v_v`, `bus_3v3_v`, `solar_array_power_w`, `payload_power_w`, `eps_mode`.
     - Thermal: `battery_temp_c`, `obc_board_temp_c`, `payload_temp_c`, `panel_temp_c`.
     - Radiation: `rad_cps`.
   - Behaviors: sun/eclipse cycles, thermal lag, occasional radiation spikes, fault injections.

2. **Digital Twin**
   - Defines "healthy" ranges for telemetry.
   - Compares simulated vs expected values.
   - Flags deviations.

3. **Anomaly Detection**
   - Threshold-based (e.g., voltage < 6.6V, temp > 45°C).
   - Hook for future ML (Isolation Forest).

4. **Autonomous Recovery / Self-Healing Logic**
   - On anomaly, apply corrective action:
     - Power drop → switch to SAFE, simulate sun-pointing.
     - Thermal spike → shut down payload.
     - Radiation spike → log & throttle.
   - Maintain mode state: NORMAL, SAFE, RECOVERED.

5. **Event Timeline / Logs**
   - Append anomalies & recoveries with timestamp.
   - Store in-memory list of dicts.

6. **Data Prioritization**
   - NORMAL → downlink all telemetry.
   - SAFE → downlink critical only (voltage, temp, soc).

7. **API Endpoints**
   - `/telemetry/latest`
   - `/telemetry/logs`
   - `/mode`
   - `/downlink`
   - `/simulate/fault` (optional, demo only).

---

## Tech Stack
- **Backend:** Python 3.10+, FastAPI
- **Frontend:** React + Next.js (to be scaffolded later)
- **Data:** In-memory storage for telemetry + logs
- **Deployment:** Local run for hackathon demo

---

## Development Strategy
1. Build telemetry simulator.
2. Add digital twin ranges.
3. Add anomaly detection.
4. Add recovery logic.
5. Add logging system.
6. Expose via FastAPI endpoints.
7. Connect dashboard later.

---

## Healthy Ranges (Baseline)
- `battery_voltage_v`: 6.6 – 8.4 V  
- `battery_soc_pct`: 20 – 100 %  
- `battery_temp_c`: −5 – 45 °C  
- `obc_board_temp_c`: 0 – 60 °C  
- `payload_temp_c`: −10 – 55 °C  
- `panel_temp_c`: −50 – 60 °C  
- `rad_cps`: 0.1 – 5 cps (spikes allowed to 80 cps)  
- `bus_5v_v`: 4.9 – 5.1 V  
- `bus_3v3_v`: 3.25 – 3.40 V
