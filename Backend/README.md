# SURAKSHASat Backend

FastAPI backend for the CubeSat telemetry simulation system.

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

### Installation

```bash
# Navigate to backend directory
cd Backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📡 API Endpoints

### Telemetry

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/telemetry/latest` | GET | Get the most recent telemetry reading |
| `/telemetry/logs` | GET | Get the event log (anomalies, recoveries) |

### Satellite Mode

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/mode` | GET | Get current satellite mode |
| `/downlink` | GET | Get telemetry with data prioritization |

### Recovery

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/recovery/status` | GET | Get recovery engine status |
| `/recovery/history` | GET | Get recovery history |

### Fault Injection

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/simulate/fault` | POST | Inject a fault for testing |

#### Fault Injection Request

```json
{
  "type": "LOW_VOLTAGE",
  "duration": 60.0
}
```

**Fault Types:**
- `LOW_VOLTAGE` - Simulate battery voltage drop
- `HIGH_TEMP` - Simulate thermal spike
- `RADIATION_SPIKE` - Simulate radiation event
- `POWER_FAILURE` - Simulate power system failure

---

## 🏗️ Architecture

### File Structure

```
Backend/
├── main.py           # FastAPI application & API endpoints
├── telemetry.py      # Telemetry simulation engine
├── recovery.py       # Recovery logic & mode management
└── requirements.txt  # Python dependencies
```

### Components

#### TelemetrySimulator (`telemetry.py`)
- Generates synthetic CubeSat telemetry in real-time
- Models orbital mechanics (90-minute orbit, 60% sun/40% eclipse)
- Implements thermal lag modeling
- Handles radiation spike simulation
- Supports fault injection

#### RecoveryEngine (`recovery.py`)
- Monitors telemetry for anomalies
- Applies recovery strategies automatically
- Manages satellite mode state machine (NORMAL → SAFE → RECOVERED → NORMAL)
- Logs all recovery actions

---

## 🔬 Telemetry Parameters

### Power/EPS
| Parameter | Unit | Healthy Range |
|-----------|------|---------------|
| `battery_voltage_v` | V | 6.6 – 8.4 |
| `battery_current_a` | A | -0.8 – 0.5 |
| `battery_soc_pct` | % | 20 – 100 |
| `bus_5v_v` | V | 4.9 – 5.1 |
| `bus_3v3_v` | V | 3.25 – 3.40 |
| `solar_array_power_w` | W | 0 – 8 |
| `payload_power_w` | W | 0 – 4 |
| `eps_mode` | - | NORMAL/LOW_POWER/FULL_CHARGE |

### Thermal
| Parameter | Unit | Healthy Range |
|-----------|------|---------------|
| `battery_temp_c` | °C | −5 – 45 |
| `obc_board_temp_c` | °C | 0 – 60 |
| `payload_temp_c` | °C | −10 – 55 |
| `panel_temp_c` | °C | −50 – 60 |

### Radiation
| Parameter | Unit | Healthy Range |
|-----------|------|---------------|
| `rad_cps` | cps | 0.1 – 5 (spikes allowed to 80) |

---

## 🔧 Configuration

### Environment Variables

Currently, the backend runs with sensible defaults. For production deployment, consider:

```bash
# Server configuration
HOST=0.0.0.0
PORT=8000

# CORS origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.104.1 | Web framework |
| uvicorn | 0.24.0 | ASGI server |
| pydantic | 2.5.0 | Data validation |
| python-multipart | 0.0.6 | Form data handling |

---

## 🧪 Testing

```bash
# Test with curl
curl http://localhost:8000/telemetry/latest

# Inject a fault
curl -X POST http://localhost:8000/simulate/fault \
  -H "Content-Type: application/json" \
  -d '{"type": "LOW_VOLTAGE", "duration": 30}'
```

---

## 📜 License

MIT License - see [LICENSE](../LICENSE) for details.
