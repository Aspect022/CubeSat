"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TelemetryLineChart } from "@/components/charts/telemetry-line"
import { DigitalTwinOverlay } from "@/components/charts/digital-twin-overlay"
import { DigitalTwinComparisonChart } from "@/components/charts/digital-twin-comparison"
import { TimelineEvents } from "@/components/charts/timeline-events"
import { AnomalyFlags } from "@/components/cards/anomaly-flags"
import { ModeDownlinkCard } from "@/components/cards/mode-downlink"
import { SimpleInjectAnomalyButton } from "@/components/cards/simple-inject-anomaly"
import { useTelemetryLatest, useTelemetryLogs } from "@/hooks/use-surakshasat"

export default function ClientDashboard() {
  const { data: latest } = useTelemetryLatest()
  const { data: logs } = useTelemetryLogs()

  return (
    <div className="grid grid-cols-12 gap-6 space-y-6">
      <Card className="col-span-12 lg:col-span-5 bg-slate-900/50 border-slate-700 shadow-2xl rounded-xl">
        <CardHeader className="pb-4">
          <CardTitle className="text-white text-xl font-bold">Live Telemetry</CardTitle>
        </CardHeader>
        <CardContent>
          <TelemetryLineChart data={latest ? [latest] : []} />
        </CardContent>
      </Card>

      <Card className="col-span-12 lg:col-span-4 bg-slate-900/50 border-slate-700 shadow-2xl rounded-xl">
        <CardHeader className="pb-4">
          <CardTitle className="text-white text-xl font-bold">Digital Twin (Pred vs Actual)</CardTitle>
        </CardHeader>
        <CardContent>
          <DigitalTwinOverlay data={latest} />
        </CardContent>
      </Card>

      <div className="col-span-12 lg:col-span-3 space-y-6">
        <div className="relative">
          <AnomalyFlags logs={logs} />
          <div className="absolute top-3 right-3">
            <SimpleInjectAnomalyButton />
          </div>
        </div>
      </div>

      <Card className="col-span-12 bg-slate-900/50 border-slate-700 shadow-2xl rounded-xl">
        <CardHeader className="pb-4">
          <CardTitle className="text-white text-xl font-bold">Digital Twin Comparison - Key Parameters</CardTitle>
        </CardHeader>
        <CardContent>
          <DigitalTwinComparisonChart />
        </CardContent>
      </Card>

      <Card className="col-span-12 lg:col-span-7 bg-slate-900/50 border-slate-700 shadow-2xl rounded-xl">
        <CardHeader className="pb-4">
          <CardTitle className="text-white text-xl font-bold">Event Timeline</CardTitle>
        </CardHeader>
        <CardContent>
          <TimelineEvents events={logs ?? []} />
        </CardContent>
      </Card>

      <div className="col-span-12 lg:col-span-5">
        <ModeDownlinkCard />
      </div>
    </div>
  )
}
