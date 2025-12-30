"use client"

import { Button } from "@/components/ui/button"
import { useToast } from "@/components/ui/use-toast"
import { api } from "@/lib/api"
import { useState, useEffect } from "react"

const FAULT_TYPES = ["LOW_VOLTAGE", "HIGH_TEMP", "RADIATION_SPIKE", "POWER_FAILURE"] as const

export function SimpleInjectAnomalyButton() {
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
      // Select a random fault type
      const randomFaultType = FAULT_TYPES[Math.floor(Math.random() * FAULT_TYPES.length)]
      
      console.log("Injecting anomaly:", randomFaultType)
      
      // Call the fault injection API with correct field name
      const response = await fetch(api("/simulate/fault"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          type: randomFaultType,  // Changed from fault_type to type
          duration: 30.0
        }),
      })

      console.log("API response:", response.status)

      if (!response.ok) {
        const errorText = await response.text()
        console.error("API error:", errorText)
        throw new Error(`Failed to inject fault: ${response.status} - ${errorText}`)
      }

      const result = await response.json()
      console.log("API result:", result)

      // Show success toast
      toast({
        title: "Anomaly Injected",
        description: `Anomaly injected: ${randomFaultType}`,
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
        size="sm"
        className="bg-red-600 hover:bg-red-700 text-white"
      >
        Inject Anomaly
      </Button>
    )
  }

  return (
    <Button 
      onClick={handleInjectAnomaly}
      disabled={isLoading}
      size="sm"
      className="bg-red-600 hover:bg-red-700 text-white"
    >
      {isLoading ? "Injecting..." : "Inject Anomaly"}
    </Button>
  )
}