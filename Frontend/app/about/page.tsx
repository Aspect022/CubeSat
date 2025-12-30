export const metadata = { title: "About • SURAKSHASat" }

export default function AboutPage() {
  return (
    <main className="mx-auto max-w-3xl px-4 py-10">
      <h1 className="text-balance text-3xl font-semibold tracking-tight">About SURAKSHASat</h1>
      <p className="mt-4 text-pretty text-muted-foreground">
        SURAKSHASat is an autonomous, self-healing CubeSat simulation built for a hackathon MVP. This frontend showcases
        live telemetry, a digital twin overlay, anomaly detection, and recovery status.
      </p>

      <section className="mt-8">
        <h2 className="text-xl font-semibold">Team Credits</h2>
        <ul className="mt-2 list-inside list-disc text-muted-foreground">
          <li>Systems & Telemetry</li>
          <li>Recovery Algorithms</li>
          <li>Frontend & UX</li>
          <li>Backend (FastAPI)</li>
        </ul>
      </section>
    </main>
  )
}
