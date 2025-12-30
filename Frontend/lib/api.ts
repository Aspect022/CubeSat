export const API_BASE =
  (typeof window !== "undefined" ? process.env.NEXT_PUBLIC_API_BASE : process.env.NEXT_PUBLIC_API_BASE) || ""

export function api(path: string) {
  if (!path.startsWith("/")) return `${API_BASE}/${path}`
  return `${API_BASE}${path}`
}

export const fetcher = async (url: string) => {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`Request failed: ${res.status}`)
  return res.json()
}
