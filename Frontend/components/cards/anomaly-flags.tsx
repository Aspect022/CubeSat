"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"
import type { LogEvent } from "@/hooks/use-surakshasat"

export function AnomalyFlags({ logs }: { logs: LogEvent[] | undefined }) {
  const anomalies = (logs ?? [])
    .filter((e) => e.type === "ANOMALY_DETECTED")
    .slice(-6)
    .reverse()

  return (
    <Card className="h-full bg-slate-900/50 border-slate-700 shadow-2xl rounded-xl">
      <CardHeader className="pb-4">
        <CardTitle className="text-pretty text-white text-xl font-bold">Anomaly Flags & Recovery</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {anomalies.length === 0 && <p className="text-sm text-white">No recent anomalies detected.</p>}
        {anomalies.map((a, idx) => (
          <Alert key={idx} className="bg-orange-500/10 border-orange-500/30">
            <AlertTitle>⚠️ Warning</AlertTitle>
            <AlertDescription className="text-sm">
              {a.description || "Anomaly detected"} • {new Date(a.timestamp).toLocaleTimeString()}
            </AlertDescription>
          </Alert>
        ))}
        {(logs ?? [])
          .filter((e) => e.type === "RECOVERY_APPLIED" || e.type === "RECOVERY_COMPLETE")
          .slice(-4)
          .reverse()
          .map((r, idx) => (
            <Alert key={`r-${idx}`} className="bg-emerald-500/10">
              <AlertTitle>✅ Recovery {r.type === "RECOVERY_COMPLETE" ? "Complete" : "Applied"}</AlertTitle>
              <AlertDescription className="text-sm">
                {r.description || "System recovered"} • {new Date(r.timestamp).toLocaleTimeString()}
              </AlertDescription>
            </Alert>
          ))}
      </CardContent>
    </Card>
  )
}
