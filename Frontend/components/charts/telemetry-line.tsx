"use client"

import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from "recharts"
import type { TelemetryPoint } from "@/hooks/use-surakshasat"

function formatTime(x: string | number) {
  const d = new Date(x)
  return isNaN(d.getTime()) ? String(x) : d.toLocaleTimeString()
}

export function TelemetryLineChart({ data }: { data: TelemetryPoint[] }) {
  return (
    <div className="h-64 w-full bg-slate-800/30 rounded-lg p-2">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data ?? []} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
          <CartesianGrid stroke="hsl(var(--border))" strokeDasharray="1 3" strokeOpacity={0.3} />
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
          <Line type="monotone" dataKey="battery_voltage_v" name="Battery V" stroke="#00bfff" dot={false} strokeWidth={2} />
          <Line
            type="monotone"
            dataKey="battery_temp_c"
            name="Battery Temp °C"
            stroke="#0080ff"
            strokeDasharray="5 5"
            dot={false}
            strokeWidth={2}
          />
          <Line type="monotone" dataKey="rad_cps" name="Radiation cps" stroke="#0066cc" dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
