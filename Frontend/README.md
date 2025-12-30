# SURAKSHASat Frontend

Next.js 15 dashboard for the CubeSat telemetry simulation system.

## 🚀 Quick Start

### Prerequisites

- Node.js 18 or higher
- npm or yarn

### Installation

```bash
# Navigate to frontend directory
cd Frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The dashboard will be available at http://localhost:3000

---

## 📁 Project Structure

```
Frontend/
├── app/                      # Next.js App Router pages
│   ├── page.tsx              # Home page with starfield animation
│   ├── layout.tsx            # Root layout with theme provider
│   ├── dashboard/            # Main telemetry dashboard
│   │   ├── page.tsx
│   │   └── sections/
│   │       └── client-dashboard.tsx
│   ├── logs/                 # Event logs page
│   ├── recovery/             # Recovery status page
│   ├── api-docs/             # API documentation page
│   └── about/                # About page
│
├── components/
│   ├── cards/                # Card components
│   │   ├── anomaly-flags.tsx
│   │   ├── inject-anomaly.tsx
│   │   └── mode-downlink.tsx
│   ├── charts/               # Chart components
│   │   ├── digital-twin-comparison.tsx
│   │   ├── digital-twin-overlay.tsx
│   │   ├── telemetry-line.tsx
│   │   └── timeline-events.tsx
│   ├── home/                 # Home page components
│   │   └── starfield-canvas.tsx
│   ├── ui/                   # shadcn/ui components
│   ├── site-header.tsx       # Navigation header
│   ├── site-footer.tsx       # Footer
│   └── theme-provider.tsx    # Theme context
│
├── hooks/
│   ├── use-surakshasat.ts    # API hooks (SWR)
│   ├── use-toast.ts          # Toast notifications
│   └── use-mobile.ts         # Mobile detection
│
├── lib/
│   ├── api.ts                # API utilities
│   └── utils.ts              # General utilities
│
└── styles/
    └── globals.css           # Global styles
```

---

## 🎨 Pages

### Home (`/`)
Landing page with animated starfield background and navigation to dashboard.

### Dashboard (`/dashboard`)
Main telemetry monitoring dashboard featuring:
- **Live Telemetry Chart** - Real-time parameter visualization
- **Digital Twin Overlay** - Predicted vs actual values
- **Digital Twin Comparison** - Key parameter comparison charts
- **Anomaly Flags** - Current anomaly status
- **Event Timeline** - Chronological event log
- **Mode & Downlink Status** - Current satellite mode

### Logs (`/logs`)
Complete event log with filtering and search capabilities.

### Recovery (`/recovery`)
Recovery engine status and history.

### API Docs (`/api-docs`)
Embedded FastAPI Swagger documentation.

### About (`/about`)
Project information and team credits.

---

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file in the Frontend directory:

```bash
# Backend API URL
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

For production (Vercel):
```bash
NEXT_PUBLIC_API_BASE=https://your-backend-url.com
```

---

## 📦 Tech Stack

| Technology | Purpose |
|------------|---------|
| Next.js 15 | React framework with App Router |
| TypeScript | Type safety |
| Tailwind CSS 4 | Utility-first styling |
| Radix UI | Accessible component primitives |
| shadcn/ui | Pre-built UI components |
| Recharts | Data visualization |
| SWR | Data fetching with caching |
| Geist | Typography (font) |

---

## 🚢 Deployment

### Vercel (Recommended)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/SURAKSHASat&root-directory=Frontend)

1. Connect your GitHub repository
2. Set the **Root Directory** to `Frontend`
3. Add environment variable: `NEXT_PUBLIC_API_BASE`
4. Deploy!

### Manual Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

---

## 🧪 Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build for production |
| `npm start` | Start production server |
| `npm run lint` | Run ESLint |

---

## 🎯 API Integration

The frontend uses SWR hooks for data fetching with automatic revalidation:

```typescript
import { useTelemetryLatest, useTelemetryLogs } from "@/hooks/use-surakshasat"

function MyComponent() {
  const { data: telemetry } = useTelemetryLatest()  // Auto-refreshes every 2s
  const { data: logs } = useTelemetryLogs()
  
  // Use data...
}
```

Available hooks:
- `useTelemetryLatest()` - Latest telemetry reading
- `useTelemetryLogs()` - Event log
- `useMode()` - Current satellite mode
- `useDownlink()` - Downlink data
- `useRecoveryStatus()` - Recovery engine status
- `useRecoveryHistory()` - Recovery history

---

## 📜 License

MIT License - see [LICENSE](../LICENSE) for details.
