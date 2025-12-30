"use client"

import { useEffect, useRef } from "react"

export function StarfieldCanvas() {
  const ref = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = ref.current!
    const ctx = canvas.getContext("2d")!
    let raf = 0
    const DPR = Math.min(2, window.devicePixelRatio || 1)
    let w = (canvas.width = Math.floor(window.innerWidth * DPR))
    let h = (canvas.height = Math.floor(window.innerHeight * DPR))
    const stars = Array.from({ length: 120 }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      z: Math.random() * 1 + 0.2,
    }))

    function resize() {
      w = canvas.width = Math.floor(window.innerWidth * DPR)
      h = canvas.height = Math.floor(window.innerHeight * DPR)
    }
    window.addEventListener("resize", resize)

    function step() {
      ctx.fillStyle = "rgba(3,6,12,0.9)"
      ctx.fillRect(0, 0, w, h)
      for (const s of stars) {
        ctx.fillStyle = "rgba(34,211,238,0.9)"
        const r = s.z * 1.2
        ctx.beginPath()
        ctx.arc(s.x, s.y, r, 0, Math.PI * 2)
        ctx.fill()
        s.y += s.z * 0.6
        if (s.y > h) {
          s.y = 0
          s.x = Math.random() * w
        }
      }
      raf = requestAnimationFrame(step)
    }
    raf = requestAnimationFrame(step)
    return () => {
      cancelAnimationFrame(raf)
      window.removeEventListener("resize", resize)
    }
  }, [])

  return <canvas ref={ref} aria-hidden="true" className="pointer-events-none fixed inset-0 -z-10 opacity-60" />
}
