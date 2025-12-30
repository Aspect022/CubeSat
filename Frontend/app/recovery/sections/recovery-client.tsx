"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useRecoveryHistory, useRecoveryStatus } from "@/hooks/use-surakshasat"

export default function RecoveryClient() {
  const { data: status } = useRecoveryStatus()
  const { data: history } = useRecoveryHistory()

  return (
    <div className="grid grid-cols-12 gap-4">
      <Card className="col-span-12 lg:col-span-5">
        <CardHeader>
          <CardTitle>Current Strategy</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <p className="text-sm text-muted-foreground">Active:</p>
          <p className="text-base font-medium">{status?.active ? "Yes" : status?.active === false ? "No" : "—"}</p>
          <p className="text-sm text-muted-foreground">Strategy:</p>
          <p className="text-base font-medium">{status?.strategy ?? "—"}</p>
        </CardContent>
      </Card>

      <Card className="col-span-12 lg:col-span-7">
        <CardHeader>
          <CardTitle>Recovery History</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-3">
            {(history ?? [])
              .slice()
              .reverse()
              .map((h, idx) => (
                <li key={idx} className="rounded-md border border-border/40 bg-muted/30 p-3">
                  <p className="text-sm">
                    <span className="mr-2 text-emerald-300">✅</span>
                    {h.message || "Recovery action"}
                  </p>
                  <p className="text-xs text-muted-foreground">{new Date(h.timestamp).toLocaleString()}</p>
                </li>
              ))}
            {(history ?? []).length === 0 && <p className="text-sm text-muted-foreground">No recovery events found.</p>}
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}
