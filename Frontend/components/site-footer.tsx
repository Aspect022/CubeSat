import Link from "next/link"

export function SiteFooter() {
  return (
    <footer className="border-t border-border/40">
      <div className="mx-auto max-w-7xl px-4 py-6 text-sm text-muted-foreground">
        <div className="flex items-center justify-between">
          <p>© {new Date().getFullYear()} SURAKSHASat</p>
          <p>
            Built by Jayesh and Rajath 
            <Link href="/about" className="text-cyan-300 underline-offset-4 hover:underline">
              Credits
            </Link>
          </p>
        </div>
      </div>
    </footer>
  )
}
