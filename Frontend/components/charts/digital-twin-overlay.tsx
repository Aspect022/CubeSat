"use client"

import { ComposedChart, Line, XAxis, YAxis, Tooltip, Area, ResponsiveContainer, CartesianGrid, Legend } from "recharts"
import type { TelemetryPoint } from "@/hooks/use-surakshasat"

const HEALTHY = { battery_v: { min: 7.2, max: 8.4 } }

function formatTime(x: string | number) {
  const d = new Date(x)
  return isNaN(d.getTime()) ? String(x) : d.toLocaleTimeString()
}

export function DigitalTwinOverlay({ data }: { data: TelemetryPoint | null }) {
  // For now, we'll create a simple chart with the single data point
  // In a real implementation, you might want to maintain a history of data points
  const prepared = data ? [{
    ...data,
    predicted_battery_v: data.battery_voltage_v || 0, // Simple prediction for demo
  }] : []

  return (
    <div className="h-64 w-full bg-slate-800/30 rounded-lg p-2">
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart data={prepared} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
          <CartesianGrid stroke="hsl(var(--border))" strokeDasharray="3 3" />
          <XAxis dataKey="timestamp" tickFormatter={formatTime} stroke="#ffffff" />
          <YAxis stroke="#ffffff" />
          <Tooltip
            contentStyle={{
              background: "hsl(var(--popover))",
              border: "1px solid hsl(var(--border))",
              borderRadius: 8,
            }}
            labelFormatter={(l) => `Time: ${formatTime(l as any)}`}
          />
          <Legend />
          <Area
            name="Healthy Range (Battery)"
            type="monotone"
            dataKey="battery_voltage_v"
            stroke="transparent"
            fill="rgba(34,211,238,0.12)"
            isAnimationActive={false}
            baseValue={HEALTHY.battery_v.min}
          />
          <Line
            type="monotone"
            dataKey="battery_voltage_v"
            name="Actual Battery"
            stroke="#22d3ee"
            dot={false}
            strokeWidth={2}
          />
          <Line
            type="monotone"
            dataKey="predicted_battery_v"
            name="Pred Battery"
            stroke="#94a3b8"
            dot={false}
            strokeDasharray="5 5"
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  )
}
