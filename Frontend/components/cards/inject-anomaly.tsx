"use client"

import { Button } from "@/components/ui/button"
import { useToast } from "@/components/ui/use-toast"
import { api } from "@/lib/api"
import { useState, useEffect } from "react"

const FAULT_TYPES = ["LOW_VOLTAGE", "HIGH_TEMP", "RADIATION_SPIKE"] as const

export function InjectAnomalyButton() {
  const [isLoading, setIsLoading] = useState(false)
  const [isMounted, setIsMounted] = useState(false)
  const { toast } = useToast()

  // Ensure component is mounted on client side
  useEffect(() => {
    setIsMounted(true)
  }, [])

  const handleInjectAnomaly = async () => {
    if (isLoading || !isMounted) return

    setIsLoading(true)
    
    try {
      // Select a random fault type (only on client side)
      const randomFaultType = FAULT_TYPES[Math.floor(Math.random() * FAULT_TYPES.length)]
      
      // Call the fault injection API
      const response = await fetch(api("/simulate/fault"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          fault_type: randomFaultType,
          duration: 30.0 // 30 seconds duration
        }),
      })

      if (!response.ok) {
        throw new Error(`Failed to inject fault: ${response.status}`)
      }

      // Show success toast
      toast({
        title: "Anomaly Injected",
        description: `Anomaly injected: ${randomFaultType}`,
        variant: "default",
      })

    } catch (error) {
      console.error("Error injecting anomaly:", error)
      
      // Show error toast
      toast({
        title: "Error",
        description: "Failed to inject anomaly. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  // Don't render until mounted on client side
  if (!isMounted) {
    return (
      <Button 
        disabled
        className="w-full bg-red-600 hover:bg-red-700 text-white font-semibold"
      >
        Inject Anomaly
      </Button>
    )
  }

  return (
    <Button 
      onClick={handleInjectAnomaly}
      disabled={isLoading}
      className="w-full bg-red-600 hover:bg-red-700 text-white font-semibold"
    >
      {isLoading ? "Injecting..." : "Inject Anomaly"}
    </Button>
  )
}