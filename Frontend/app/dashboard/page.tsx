import { Suspense } from "react"
import ClientDashboard from "./sections/client-dashboard"

export const metadata = { title: "Dashboard • SURAKSHASat" }

export default function DashboardPage() {
  return (
    <main className="mx-auto max-w-7xl px-4 py-6">
      <h1 className="mb-4 text-2xl font-semibold tracking-tight">Mission Dashboard</h1>
      <Suspense fallback={<p className="text-sm text-muted-foreground">Loading…</p>}>
        <ClientDashboard />
      </Suspense>
    </main>
  )
}
