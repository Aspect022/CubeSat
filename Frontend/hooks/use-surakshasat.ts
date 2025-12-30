"use client"

import useSWR from "swr"
import { api, fetcher } from "@/lib/api"

export type TelemetryPoint = {
  timestamp: string | number
  battery_voltage_v?: number
  battery_current_a?: number
  battery_soc_pct?: number
  bus_5v_v?: number
  bus_3v3_v?: number
  solar_array_power_w?: number
  payload_power_w?: number
  eps_mode?: string
  battery_temp_c?: number
  obc_board_temp_c?: number
  payload_temp_c?: number
  panel_temp_c?: number
  rad_cps?: number
  mode?: string
  fault_injected?: boolean
  [key: string]: any
}

export type LogEvent = {
  timestamp: string | number
  type: "ANOMALY_DETECTED" | "RECOVERY_APPLIED" | "MODE_CHANGE" | "FAULT_INJECTED" | "RECOVERY_ACTION" | "RECOVERY_COMPLETE" | string
  description: string
  data?: Record<string, any>
}

export function useTelemetryLatest() {
  return useSWR<TelemetryPoint>(api("/telemetry/latest"), fetcher, { refreshInterval: 2000 })
}
export function useTelemetryLogs() {
  return useSWR<LogEvent[]>(api("/telemetry/logs"), fetcher, { refreshInterval: 2000 })
}
export function useMode() {
  return useSWR<{ mode: "NORMAL" | "SAFE" | "RECOVERED" | string }>(api("/mode"), fetcher, {
    refreshInterval: 2000,
  })
}
export function useDownlink() {
  return useSWR<any>(api("/downlink"), fetcher, { refreshInterval: 2000 })
}
export function useRecoveryStatus() {
  return useSWR<{ strategy?: string; active?: boolean }>(api("/recovery/status"), fetcher, {
    refreshInterval: 2000,
  })
}
export function useRecoveryHistory() {
  return useSWR<LogEvent[]>(api("/recovery/history"), fetcher)
}
