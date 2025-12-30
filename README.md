# 🛰️ SURAKSHASat - Autonomous Self-Healing CubeSat Simulation

<div align="center">

![SURAKSHASat Banner](https://img.shields.io/badge/SURAKSHASat-Autonomous%20CubeSat-00bfff?style=for-the-badge&logo=satellite&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776ab?style=flat-square&logo=python&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-15-black?style=flat-square&logo=next.js&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688?style=flat-square&logo=fastapi&logoColor=white)
![TypeScript](https://img.shields.io/badge/TypeScript-5.0-3178c6?style=flat-square&logo=typescript&logoColor=white)

**A software-only simulation of an autonomous CubeSat self-healing system**

[Live Demo](#demo) • [Features](#features) • [Quick Start](#quick-start) • [API Docs](#api-documentation) • [Architecture](#architecture)

</div>

---

## 📖 Overview

**SURAKSHASat** demonstrates how a CubeSat can autonomously detect anomalies and apply recovery strategies, going beyond traditional "safe mode" operations. This project was built as a hackathon MVP to showcase the potential of autonomous satellite systems.

### What It Does

- 🔴 **Simulates Real-Time Telemetry** - Power, thermal, and radiation parameters with orbital mechanics
- 🔍 **Digital Twin Comparison** - Compare actual vs expected values in real-time
- ⚠️ **Anomaly Detection** - Threshold-based detection for voltage drops, temperature spikes, radiation events
- 🔧 **Self-Healing Logic** - Autonomous recovery strategies including mode changes, payload shutdown, and sun-pointing
- 📊 **Event Timeline** - Track all anomalies and recovery actions with timestamps

---

## ✨ Features

### Backend (FastAPI)
- Real-time telemetry simulation with sun/eclipse cycles
- Thermal lag modeling for temperature parameters
- Radiation spike simulation
- Fault injection for testing
- RESTful API with automatic OpenAPI documentation

### Frontend (Next.js)
- Beautiful dark-themed dashboard
- Live telemetry charts with Recharts
- Digital twin overlay visualization
- Event timeline with color-coded events
- Anomaly injection controls
- Responsive design

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** with pip
- **Node.js 18+** with npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/SURAKSHASat.git
cd SURAKSHASat
```

### 2. Start the Backend

```bash
cd Backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000` with Swagger docs at `http://localhost:8000/docs`

### 3. Start the Frontend

```bash
cd Frontend
npm install
npm run dev
```

The dashboard will be available at `http://localhost:3000`

---

## 📡 API Documentation

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/telemetry/latest` | GET | Get the most recent telemetry reading |
| `/telemetry/logs` | GET | Get the event log (anomalies, recoveries) |
| `/mode` | GET | Get current satellite mode (NORMAL/SAFE/RECOVERED) |
| `/downlink` | GET | Get telemetry based on data prioritization |
| `/simulate/fault` | POST | Inject a fault for testing |
| `/recovery/status` | GET | Get current recovery engine status |
| `/recovery/history` | GET | Get recovery history |

### Fault Types

- `LOW_VOLTAGE` - Simulate battery voltage drop
- `HIGH_TEMP` - Simulate thermal spike
- `RADIATION_SPIKE` - Simulate radiation event
- `POWER_FAILURE` - Simulate power system failure

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           Frontend (Next.js)                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │  Dashboard  │  │    Logs     │  │  Recovery   │  │  API Docs   │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │
│                              │ SWR Hooks                             │
└──────────────────────────────┼───────────────────────────────────────┘
                               │ REST API
┌──────────────────────────────┼───────────────────────────────────────┐
│                           Backend (FastAPI)                          │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                        main.py (API Layer)                       │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                    │                          │                      │
│  ┌─────────────────▼────────┐  ┌──────────────▼──────────────────┐  │
│  │   telemetry.py           │  │      recovery.py                │  │
│  │   - Orbital mechanics    │  │   - Anomaly detection           │  │
│  │   - Thermal simulation   │  │   - Recovery strategies         │  │
│  │   - Fault injection      │  │   - Mode state machine          │  │
│  └──────────────────────────┘  └─────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
SURAKSHASat/
├── Backend/
│   ├── main.py              # FastAPI application
│   ├── telemetry.py         # Telemetry simulation
│   ├── recovery.py          # Recovery logic
│   └── requirements.txt     # Python dependencies
│
├── Frontend/
│   ├── app/                 # Next.js pages
│   │   ├── dashboard/       # Main dashboard
│   │   ├── logs/            # Event logs page
│   │   ├── recovery/        # Recovery status page
│   │   └── api-docs/        # API documentation
│   ├── components/          # React components
│   │   ├── cards/           # Card components
│   │   ├── charts/          # Chart components
│   │   └── ui/              # UI primitives (shadcn/ui)
│   ├── hooks/               # Custom React hooks
│   └── lib/                 # Utilities
│
└── README.md
```

---

## 🔬 Telemetry Parameters

### Power/EPS
| Parameter | Unit | Healthy Range |
|-----------|------|---------------|
| `battery_voltage_v` | V | 6.6 – 8.4 |
| `battery_soc_pct` | % | 20 – 100 |
| `bus_5v_v` | V | 4.9 – 5.1 |
| `bus_3v3_v` | V | 3.25 – 3.40 |

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
| `rad_cps` | cps | 0.1 – 5 (spikes to 80) |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | Next.js 15, TypeScript, Tailwind CSS, Radix UI, Recharts |
| **Backend** | Python 3.10+, FastAPI, Pydantic, Uvicorn |
| **State Management** | SWR (stale-while-revalidate) |
| **Styling** | Tailwind CSS, shadcn/ui components |

---

## 🚢 Deployment

### Frontend (Vercel)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/SURAKSHASat)

1. Connect your GitHub repository to Vercel
2. Set environment variable: `NEXT_PUBLIC_API_BASE=https://your-backend-url.com`
3. Deploy!

### Backend

The backend can be deployed to any Python hosting service:
- Railway
- Render
- Fly.io
- AWS Lambda (with Mangum adapter)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

Built with ❤️ for hackathon demonstration

---

<div align="center">

**[⬆ Back to Top](#-surakshasat---autonomous-self-healing-cubesat-simulation)**

</div>
