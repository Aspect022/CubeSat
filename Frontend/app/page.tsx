import Link from "next/link"
import { Button } from "@/components/ui/button"
import { StarfieldCanvas } from "@/components/home/starfield-canvas"

export default function HomePage() {
  return (
    <main className="relative">
      <StarfieldCanvas />
      <section className="mx-auto flex min-h-[calc(100vh-6rem)] max-w-5xl flex-col items-center justify-center gap-6 px-4 text-center">
        <div className="space-y-2">
          <h1 className="text-balance text-4xl font-semibold tracking-tight sm:text-5xl">SURAKSHASat</h1>
          <p className="text-pretty text-muted-foreground sm:text-lg">Autonomous Self-Healing CubeSat Simulation</p>
        </div>
        <div className="flex items-center gap-4">
          <Button asChild className="bg-cyan-600 hover:bg-cyan-500">
            <Link href="/dashboard">Launch Dashboard</Link>
          </Button>
          <Link href="/about" className="text-sm text-muted-foreground underline-offset-4 hover:underline">
            Learn more
          </Link>
        </div>
      </section>
    </main>
  )
}
