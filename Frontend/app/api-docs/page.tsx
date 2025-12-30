import Link from "next/link"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { API_BASE } from "@/lib/api"

export const metadata = { title: "API Docs • SURAKSHASat" }
const FASTAPI_DOCS = `${API_BASE || "http://localhost:8000"}/docs`

export default function ApiDocsPage() {
  return (
    <main className="mx-auto max-w-5xl px-4 py-8">
      <h1 className="mb-4 text-2xl font-semibold tracking-tight">API Documentation</h1>

      <Card>
        <CardHeader>
          <CardTitle>FastAPI Swagger UI</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <p className="text-sm text-muted-foreground">
            The backend exposes a Swagger UI at{" "}
            <Link href={FASTAPI_DOCS} className="text-cyan-300 underline-offset-4 hover:underline">
              {FASTAPI_DOCS}
            </Link>
            .
          </p>
          <div className="overflow-hidden rounded-md border border-border/40">
            <iframe src={FASTAPI_DOCS} title="FastAPI Docs" className="h-[60vh] w-full" />
          </div>
        </CardContent>
      </Card>

      <section className="mt-6 grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Endpoints</CardTitle>
          </CardHeader>
          <CardContent className="text-sm text-muted-foreground">
            <ul className="list-inside list-disc space-y-1">
              <li>/telemetry/latest</li>
              <li>/telemetry/logs</li>
              <li>/mode</li>
              <li>/downlink</li>
              <li>/recovery/status</li>
              <li>/recovery/history</li>
            </ul>
          </CardContent>
        </Card>
      </section>
    </main>
  )
}
