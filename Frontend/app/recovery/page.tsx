import RecoveryClient from "./sections/recovery-client"

export const metadata = { title: "Recovery • SURAKSHASat" }

export default function RecoveryPage() {
  return (
    <main className="mx-auto max-w-6xl px-4 py-6">
      <h1 className="mb-4 text-2xl font-semibold tracking-tight">Recovery Status</h1>
      <RecoveryClient />
    </main>
  )
}
