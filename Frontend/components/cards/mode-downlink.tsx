"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { useMode, useDownlink } from "@/hooks/use-surakshasat"

function ModeBadge({ mode }: { mode?: string }) {
  const color =
    mode === "NORMAL"
      ? "bg-emerald-500/20 text-emerald-300 border-emerald-500/30"
      : mode === "SAFE"
        ? "bg-orange-500/20 text-orange-300 border-orange-500/30"
        : mode === "RECOVERED"
          ? "bg-cyan-500/20 text-cyan-300 border-cyan-500/30"
          : "bg-slate-500/20 text-slate-300 border-slate-500/30"
  return <Badge className={color}>{mode ?? "UNKNOWN"}</Badge>
}

function getModeStyles(mode?: string) {
  switch (mode) {
    case "NORMAL":
      return {
        borderColor: "border-green-500",
        indicatorColor: "bg-green-500",
        indicatorGlow: "shadow-green-500/50"
      }
    case "SAFE":
      return {
        borderColor: "border-red-500",
        indicatorColor: "bg-red-500",
        indicatorGlow: "shadow-red-500/50"
      }
    case "RECOVERED":
      return {
        borderColor: "border-cyan-500",
        indicatorColor: "bg-cyan-500",
        indicatorGlow: "shadow-cyan-500/50"
      }
    default:
      return {
        borderColor: "border-gray-500",
        indicatorColor: "bg-gray-500",
        indicatorGlow: "shadow-gray-500/50"
      }
  }
}

export function ModeDownlinkCard() {
  const { data: modeData } = useMode()
  const { data: downlink } = useDownlink()
  
  const modeStyles = getModeStyles(modeData?.mode)
  
  return (
    <Card className={`h-full relative border-2 ${modeStyles.borderColor} overflow-hidden bg-slate-900/50 border-slate-700 shadow-2xl rounded-xl`}>
      {/* Glowing indicator dot */}
      <div className={`absolute top-3 right-3 w-3 h-3 rounded-full ${modeStyles.indicatorColor} shadow-lg ${modeStyles.indicatorGlow} animate-pulse`} />
      
      <CardHeader className="flex flex-row items-center justify-between pb-4">
        <CardTitle className="text-white text-xl font-bold">Mode & Downlink</CardTitle>
        <ModeBadge mode={modeData?.mode} />
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <p className="text-xs text-white">Current Mode</p>
          <p className="text-2xl font-bold text-white">{modeData?.mode ?? "—"}</p>
        </div>
        <div>
          <p className="text-xs text-white">Downlink Data</p>
          <pre className="mt-1 max-h-40 overflow-auto rounded-md border border-border/40 bg-muted/30 p-3 text-xs text-white">
            {JSON.stringify(downlink ?? {}, null, 2)}
          </pre>
        </div>
      </CardContent>
    </Card>
  )
}
