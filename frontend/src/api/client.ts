import type {
  Deal,
  PipelineDeal,
  PipelineAlert,
  PipelineStats,
  Justification,
  HealthScore,
  AgentLogEntry,
  StreamChunk
} from '../types'

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const WS_URL = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options?.headers },
    ...options
  })
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(error.detail || `Request failed: ${res.status}`)
  }
  return res.json()
}

// ---- Deals ----

export async function getDeals(): Promise<Deal[]> {
  return request<Deal[]>('/deals')
}

export async function getDeal(id: number): Promise<Deal> {
  return request<Deal>(`/deals/${id}`)
}

export interface CreateDealPayload {
  company: string
  contact_name: string
  contact_title: string
  deal_value: number
  stage: string
  archetype: string
  rep_name?: string
}

export async function createDeal(payload: CreateDealPayload): Promise<Deal> {
  return request<Deal>('/deals', { method: 'POST', body: JSON.stringify(payload) })
}

export async function updateDeal(id: number, payload: Partial<CreateDealPayload>): Promise<Deal> {
  return request<Deal>(`/deals/${id}`, { method: 'PUT', body: JSON.stringify(payload) })
}

export interface AddSignalPayload {
  signal_type: 'call' | 'email' | 'meeting'
  content: string
  timestamp?: string
}

export async function addSignal(dealId: number, payload: AddSignalPayload): Promise<{ id: number; status: string }> {
  return request(`/deals/${dealId}/signals`, { method: 'POST', body: JSON.stringify(payload) })
}

export async function refreshHealth(dealId: number): Promise<HealthScore> {
  return request<HealthScore>(`/deals/${dealId}/refresh-health`, { method: 'POST' })
}

export async function getAgentLog(dealId: number): Promise<AgentLogEntry[]> {
  return request<AgentLogEntry[]>(`/deals/${dealId}/agent-log`)
}

// ---- Artifacts ----

export async function getArtifact(dealId: number): Promise<Justification> {
  return request<Justification>(`/artifacts/${dealId}`)
}

export async function updateArtifact(dealId: number, payload: Partial<Justification>): Promise<Justification> {
  return request<Justification>(`/artifacts/${dealId}`, { method: 'PUT', body: JSON.stringify(payload) })
}

export async function updateSection(
  dealId: number,
  section: string,
  content: unknown
): Promise<Justification> {
  return request<Justification>(`/artifacts/${dealId}/section`, {
    method: 'PUT',
    body: JSON.stringify({ section, content })
  })
}

// ---- Command ----

export async function getPipeline(): Promise<PipelineDeal[]> {
  return request<PipelineDeal[]>('/command/pipeline')
}

export async function getAlerts(): Promise<PipelineAlert[]> {
  return request<PipelineAlert[]>('/command/alerts')
}

export async function getStats(): Promise<PipelineStats> {
  return request<PipelineStats>('/command/stats')
}

// ---- Streaming: Build Justification ----

export function buildJustificationStream(
  dealId: number,
  onChunk: (chunk: StreamChunk) => void,
  onComplete: () => void,
  onError: (err: string) => void
): () => void {
  const controller = new AbortController()

  fetch(`${BASE_URL}/deals/${dealId}/build-justification`, {
    method: 'POST',
    signal: controller.signal
  })
    .then(async (res) => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      if (!res.body) throw new Error('No response body')

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const chunk = JSON.parse(line.slice(6)) as StreamChunk
              onChunk(chunk)
              if (chunk.type === 'complete') {
                onComplete()
              }
            } catch (e) {
              // skip malformed lines
            }
          }
        }
      }
    })
    .catch((err) => {
      if (err.name !== 'AbortError') {
        onError(err.message)
      }
    })

  return () => controller.abort()
}

// ---- WebSocket ----

export function connectDealWebSocket(
  dealId: number,
  onMessage: (msg: Record<string, unknown>) => void
): WebSocket {
  const ws = new WebSocket(`${WS_URL}/ws/${dealId}`)

  ws.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data)
      onMessage(msg)
    } catch {
      // ignore
    }
  }

  ws.onerror = (e) => {
    console.warn('WebSocket error:', e)
  }

  // Heartbeat every 25s
  const heartbeat = setInterval(() => {
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: 'ping' }))
    }
  }, 25000)

  ws.onclose = () => {
    clearInterval(heartbeat)
  }

  return ws
}
