"use client"

import { ComposedChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Line } from "recharts"
import type { LogEvent } from "@/hooks/use-surakshasat"

function toPoint(e: LogEvent) {
  const t = new Date(e.timestamp).getTime()
  const y = e.type === "ANOMALY_DETECTED" ? 2 : 
           (e.type === "RECOVERY_APPLIED" || e.type === "RECOVERY_COMPLETE") ? 1 : 0
  return { x: t, y, type: e.type, message: e.description }
}
function formatTime(ts: number) {
  const d = new Date(ts)
  return isNaN(d.getTime()) ? String(ts) : d.toLocaleTimeString()
}

export function TimelineEvents({ events }: { events: LogEvent[] }) {
  const points = (events ?? []).map(toPoint)
  
  // Sort points by time for the connecting line
  const sortedPoints = points.sort((a, b) => a.x - b.x)
  
  return (
    <div className="h-64 w-full bg-slate-800/30 rounded-lg p-2">
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
          <CartesianGrid stroke="hsl(var(--border))" strokeOpacity={0.3} />
          <XAxis
            type="number"
            dataKey="x"
            domain={["dataMin", "dataMax"]}
            tickFormatter={formatTime}
            stroke="#ffffff"
            fontSize={12}
          />
          <YAxis
            type="number"
            dataKey="y"
            domain={[0, 2]}
            ticks={[0, 1, 2]}
            tickFormatter={(v) => (v === 2 ? "🔴" : v === 1 ? "🟢" : "ℹ️")}
            stroke="#ffffff"
            fontSize={12}
          />
          <Tooltip
            formatter={(value, _name, props) => [props.payload?.message || props.payload?.type, ""]}
            labelFormatter={(l) => `Time: ${formatTime(l as number)}`}
            contentStyle={{
              background: "hsl(var(--popover))",
              border: "1px solid hsl(var(--border))",
              borderRadius: 8,
              color: "white",
            }}
            labelStyle={{
              color: "white",
            }}
            itemStyle={{
              color: "white",
            }}
          />
          
          {/* Neon blue connecting line */}
          <Line
            type="monotone"
            dataKey="y"
            data={sortedPoints}
            stroke="#00bfff"
            strokeWidth={2}
            dot={false}
            connectNulls={false}
          />
          
          {/* Event points */}
          <Scatter name="Anomalies" data={points.filter((p) => p.type === "ANOMALY_DETECTED")} fill="#f59e0b" />
          <Scatter name="Recoveries" data={points.filter((p) => p.type === "RECOVERY_APPLIED" || p.type === "RECOVERY_COMPLETE")} fill="#10b981" />
          <Scatter
            name="Other"
            data={points.filter((p) => p.type !== "ANOMALY_DETECTED" && p.type !== "RECOVERY_APPLIED" && p.type !== "RECOVERY_COMPLETE")}
            fill="#94a3b8"
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  )
}
