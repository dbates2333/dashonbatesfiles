import { useEffect, useState, useCallback, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  RefreshCw, Plus, Send, Loader2, Activity, AlertTriangle, Clock,
  X, ChevronLeft, ChevronRight, Zap, CheckSquare, Phone, Mail
} from 'lucide-react'
import type {
  Deal, Justification, AgentLogEntry, StreamChunk, AgentStatus
} from '../types'
import * as api from '../api/client'
import ArtifactPanel from '../components/ArtifactPanel'
import SignalFeed from '../components/SignalFeed'
import HealthScoreRing, { healthBg, healthLabel } from '../components/HealthScoreRing'
import AgentStatusBadge from '../components/AgentStatusBadge'
import StreamingArtifact from '../components/StreamingArtifact'
import DealCard from '../components/DealCard'
import clsx from 'clsx'

const STAGE_LABELS: Record<string, string> = {
  discovery: 'Discovery',
  technical_eval: 'Technical Eval',
  business_case: 'Business Case',
  legal: 'Legal',
  closed_won: 'Closed Won',
  closed_lost: 'Closed Lost'
}

interface AddSignalModal {
  type: 'call' | 'email' | 'meeting'
  content: string
}

export default function RepWorkspace() {
  const { dealId } = useParams()
  const navigate = useNavigate()

  const [deals, setDeals] = useState<Deal[]>([])
  const [selectedDeal, setSelectedDeal] = useState<Deal | null>(null)
  const [justification, setJustification] = useState<Justification | null>(null)
  const [agentLogs, setAgentLogs] = useState<AgentLogEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [loadingDeal, setLoadingDeal] = useState(false)

  // Streaming state
  const [isBuilding, setIsBuilding] = useState(false)
  const [streamChunks, setStreamChunks] = useState<StreamChunk[]>([])
  const [streamError, setStreamError] = useState<string | null>(null)
  const stopStreamRef = useRef<(() => void) | null>(null)

  // Signal modal
  const [showSignalModal, setShowSignalModal] = useState(false)
  const [signal, setSignal] = useState<AddSignalModal>({ type: 'call', content: '' })
  const [addingSignal, setAddingSignal] = useState(false)

  // Right panel toggle
  const [rightPanel, setRightPanel] = useState<'signals' | 'health' | 'log'>('signals')
  const [sidebarOpen, setSidebarOpen] = useState(true)

  // WebSocket
  const wsRef = useRef<WebSocket | null>(null)

  // Load all deals for sidebar
  useEffect(() => {
    api.getDeals().then((d) => {
      setDeals(d)
      setLoading(false)

      // If dealId in URL, select that deal
      if (dealId) {
        const found = d.find((deal) => deal.id === parseInt(dealId))
        if (found) selectDeal(found.id)
        else if (d.length > 0) selectDeal(d[0].id)
      } else if (d.length > 0) {
        selectDeal(d[0].id)
      }
    })
  }, [dealId])

  const selectDeal = async (id: number) => {
    if (loadingDeal) return
    setLoadingDeal(true)
    navigate(`/workspace/${id}`, { replace: true })

    // Disconnect old WS
    if (wsRef.current) {
      wsRef.current.close()
      wsRef.current = null
    }

    try {
      const deal = await api.getDeal(id)
      setSelectedDeal(deal)
      setJustification(deal.justification || null)

      const logs = await api.getAgentLog(id)
      setAgentLogs(logs)

      // Connect WS
      const ws = api.connectDealWebSocket(id, (msg) => {
        const msgType = msg.type as string
        if (msgType === 'justification_complete') {
          // Reload deal to get updated justification
          api.getDeal(id).then((updated) => {
            setSelectedDeal(updated)
            setJustification(updated.justification || null)
          })
          api.getAgentLog(id).then(setAgentLogs)
        } else if (msgType === 'health_updated') {
          api.getDeal(id).then((updated) => {
            setSelectedDeal(updated)
          })
        } else if (msgType === 'signal_analyzed') {
          api.getDeal(id).then((updated) => {
            setSelectedDeal(updated)
          })
          api.getAgentLog(id).then(setAgentLogs)
        }
      })
      wsRef.current = ws
    } catch (e) {
      console.error('Failed to load deal:', e)
    } finally {
      setLoadingDeal(false)
    }
  }

  const buildJustification = () => {
    if (!selectedDeal || isBuilding) return

    setIsBuilding(true)
    setStreamChunks([])
    setStreamError(null)

    // Update local agent status
    if (justification) {
      setJustification((j) => j ? { ...j, agent_status: 'building' as AgentStatus } : j)
    }

    const stop = api.buildJustificationStream(
      selectedDeal.id,
      (chunk) => {
        setStreamChunks((prev) => [...prev, chunk])
        if (chunk.type === 'section_complete' && chunk.data && chunk.section) {
          // Update justification sections as they complete
          setJustification((j) => {
            if (!j) return j
            const d = chunk.data as Record<string, unknown>
            if (chunk.section === 'roi_model') return { ...j, roi_model: d as Justification['roi_model'] }
            if (chunk.section === 'exec_summary') return { ...j, exec_summary: (d.exec_summary || '') as string }
            if (chunk.section === 'procurement_doc') return { ...j, procurement_doc: (d.procurement_doc || '') as string }
            if (chunk.section === 'objections') return { ...j, objection_responses: (d.objection_responses || []) as Justification['objection_responses'] }
            return j
          })
        }
      },
      () => {
        setIsBuilding(false)
        // Reload to get saved state
        if (selectedDeal) {
          api.getDeal(selectedDeal.id).then((updated) => {
            setSelectedDeal(updated)
            setJustification(updated.justification || null)
          })
          api.getAgentLog(selectedDeal.id).then(setAgentLogs)
        }
      },
      (err) => {
        setStreamError(err)
        setIsBuilding(false)
      }
    )

    stopStreamRef.current = stop
  }

  const refreshHealth = async () => {
    if (!selectedDeal) return
    try {
      await api.refreshHealth(selectedDeal.id)
      const updated = await api.getDeal(selectedDeal.id)
      setSelectedDeal(updated)
      // Also update deals list
      setDeals((prev) => prev.map((d) => d.id === updated.id ? { ...d, latest_health: updated.latest_health } : d))
      const logs = await api.getAgentLog(selectedDeal.id)
      setAgentLogs(logs)
    } catch (e) {
      console.error('Failed to refresh health:', e)
    }
  }

  const addSignal = async () => {
    if (!selectedDeal || !signal.content.trim()) return
    setAddingSignal(true)
    try {
      await api.addSignal(selectedDeal.id, signal)
      setShowSignalModal(false)
      setSignal({ type: 'call', content: '' })
      // Reload deal
      const updated = await api.getDeal(selectedDeal.id)
      setSelectedDeal(updated)
    } catch (e) {
      console.error('Failed to add signal:', e)
    } finally {
      setAddingSignal(false)
    }
  }

  const updateArtifact = async (updates: Partial<Justification>) => {
    if (!selectedDeal) return
    try {
      const updated = await api.updateArtifact(selectedDeal.id, updates)
      setJustification(updated)
    } catch (e) {
      console.error('Failed to update artifact:', e)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="flex items-center gap-3 text-slate-400">
          <Loader2 size={18} className="animate-spin" />
          <span>Loading workspace...</span>
        </div>
      </div>
    )
  }

  const health = selectedDeal?.latest_health
  const score = health?.overall_score ?? 0
  const justStatus = justification?.agent_status || selectedDeal?.justification_status?.agent_status || 'not_started'

  return (
    <div className="flex h-full overflow-hidden">
      {/* Left sidebar — deal list */}
      {sidebarOpen && (
        <div className="w-56 flex-shrink-0 border-r border-slate-800 flex flex-col overflow-hidden">
          <div className="p-3 border-b border-slate-800 flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">My Deals</span>
            <button onClick={() => setSidebarOpen(false)} className="text-slate-600 hover:text-slate-400">
              <ChevronLeft size={14} />
            </button>
          </div>
          <div className="flex-1 overflow-y-auto p-2 space-y-1">
            {deals.map((deal) => {
              const isActive = selectedDeal?.id === deal.id
              const dHealth = deal.latest_health?.overall_score ?? 0
              return (
                <button
                  key={deal.id}
                  onClick={() => selectDeal(deal.id)}
                  className={clsx(
                    'w-full text-left px-2.5 py-2.5 rounded-lg transition-colors flex items-center gap-2.5',
                    isActive ? 'bg-slate-800 border border-slate-700' : 'hover:bg-slate-800/60'
                  )}
                >
                  <HealthScoreRing score={dHealth} size="sm" />
                  <div className="min-w-0 flex-1">
                    <div className="text-xs font-medium text-slate-200 truncate">{deal.company}</div>
                    <div className="text-[10px] text-slate-500">${(deal.deal_value / 1000).toFixed(0)}K · {STAGE_LABELS[deal.stage] || deal.stage}</div>
                  </div>
                </button>
              )
            })}
          </div>
        </div>
      )}

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden min-w-0">
        {selectedDeal ? (
          <>
            {/* Deal header */}
            <div className="flex-shrink-0 border-b border-slate-800 px-5 py-3 flex items-center gap-4">
              {!sidebarOpen && (
                <button onClick={() => setSidebarOpen(true)} className="text-slate-600 hover:text-slate-400 mr-1">
                  <ChevronRight size={14} />
                </button>
              )}
              {loadingDeal && <Loader2 size={14} className="text-slate-500 animate-spin" />}

              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3">
                  <h2 className="text-base font-bold text-slate-100">{selectedDeal.company}</h2>
                  <span className="text-slate-500 text-sm">·</span>
                  <span className="text-sm text-slate-400">{selectedDeal.contact_name}</span>
                  <span className="text-xs text-slate-600">{selectedDeal.contact_title}</span>
                  <AgentStatusBadge status={justStatus as AgentStatus} size="sm" />
                </div>
                <div className="flex items-center gap-3 mt-0.5">
                  <span className="text-sm font-semibold text-indigo-400">${(selectedDeal.deal_value / 1000).toFixed(0)}K</span>
                  <span className="text-xs text-slate-500">{STAGE_LABELS[selectedDeal.stage] || selectedDeal.stage}</span>
                  <span className="text-xs text-slate-600">·</span>
                  <span className="text-xs text-slate-500">{selectedDeal.archetype?.replace(/_/g, ' ')}</span>
                  {selectedDeal.rep_name && (
                    <>
                      <span className="text-xs text-slate-600">·</span>
                      <span className="text-xs text-slate-500">Rep: {selectedDeal.rep_name}</span>
                    </>
                  )}
                </div>
              </div>

              {/* Health */}
              <HealthScoreRing score={score} size="md" showLabel />

              {/* Actions */}
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setShowSignalModal(true)}
                  className="btn-secondary text-xs flex items-center gap-1.5"
                >
                  <Plus size={13} /> Add Signal
                </button>
                <button
                  onClick={buildJustification}
                  disabled={isBuilding}
                  className="btn-primary text-xs flex items-center gap-1.5"
                >
                  {isBuilding ? (
                    <><Loader2 size={12} className="animate-spin" /> Building...</>
                  ) : (
                    <><Zap size={12} /> Build Justification</>
                  )}
                </button>
                <button
                  onClick={refreshHealth}
                  className="btn-ghost text-xs flex items-center gap-1.5"
                  title="Refresh health score"
                >
                  <Activity size={12} />
                </button>
              </div>
            </div>

            {/* Main workspace */}
            <div className="flex-1 flex overflow-hidden">
              {/* Artifact panel */}
              <div className="flex-1 flex flex-col overflow-hidden">
                {/* Streaming progress */}
                {(isBuilding || streamChunks.length > 0) && (
                  <div className="px-5 pt-4 flex-shrink-0">
                    <StreamingArtifact
                      chunks={streamChunks}
                      isStreaming={isBuilding}
                      error={streamError}
                    />
                  </div>
                )}

                {justification ? (
                  <ArtifactPanel
                    justification={justification}
                    onUpdate={updateArtifact}
                  />
                ) : (
                  <div className="flex-1 flex flex-col items-center justify-center p-10 text-center">
                    <div className="w-14 h-14 bg-indigo-500/10 rounded-2xl flex items-center justify-center mb-4">
                      <Zap size={24} className="text-indigo-400" />
                    </div>
                    <h3 className="text-base font-semibold text-slate-100 mb-2">No Justification Built Yet</h3>
                    <p className="text-sm text-slate-400 max-w-sm mb-5">
                      The agent will auto-build a complete ROI model, exec summary, procurement document, and objection responses from this deal's signals.
                    </p>
                    <button
                      onClick={buildJustification}
                      disabled={isBuilding}
                      className="btn-primary flex items-center gap-2"
                    >
                      {isBuilding ? <Loader2 size={14} className="animate-spin" /> : <Zap size={14} />}
                      Build Justification Package
                    </button>
                    {(selectedDeal.signals?.length ?? 0) === 0 && (
                      <p className="text-xs text-slate-500 mt-3">
                        Tip: Add call transcripts or emails as signals for richer output.
                      </p>
                    )}
                  </div>
                )}
              </div>

              {/* Right rail */}
              <div className="w-80 flex-shrink-0 border-l border-slate-800 flex flex-col overflow-hidden">
                {/* Right panel tabs */}
                <div className="flex border-b border-slate-800 flex-shrink-0">
                  {[
                    { id: 'signals', label: `Signals (${selectedDeal.signals?.length ?? 0})` },
                    { id: 'health', label: 'Health' },
                    { id: 'log', label: 'Agent Log' }
                  ].map((tab) => (
                    <button
                      key={tab.id}
                      onClick={() => setRightPanel(tab.id as typeof rightPanel)}
                      className={clsx(
                        'flex-1 py-2.5 text-xs font-medium transition-colors border-b-2 -mb-px',
                        rightPanel === tab.id
                          ? 'border-indigo-500 text-slate-100'
                          : 'border-transparent text-slate-400 hover:text-slate-300'
                      )}
                    >
                      {tab.label}
                    </button>
                  ))}
                </div>

                <div className="flex-1 overflow-y-auto p-4">
                  {/* Signals panel */}
                  {rightPanel === 'signals' && (
                    <div>
                      <div className="flex items-center justify-between mb-3">
                        <span className="text-xs font-semibold text-slate-400">Deal Signals</span>
                        <button
                          onClick={() => setShowSignalModal(true)}
                          className="text-[10px] text-indigo-400 hover:text-indigo-300 flex items-center gap-1"
                        >
                          <Plus size={10} /> Add
                        </button>
                      </div>
                      <SignalFeed signals={selectedDeal.signals || []} />
                    </div>
                  )}

                  {/* Health panel */}
                  {rightPanel === 'health' && health && (
                    <div className="space-y-4">
                      <div className="flex items-center gap-3">
                        <HealthScoreRing score={score} size="lg" showLabel />
                        <div>
                          <div className="text-xs text-slate-500 mb-0.5">Overall Health</div>
                          <div className="text-2xl font-bold text-slate-100">{score.toFixed(0)}/100</div>
                          <div className={clsx('text-xs font-medium', healthBg(score).split(' ')[1])}>
                            {healthLabel(score)}
                          </div>
                        </div>
                      </div>

                      {/* Dimension scores */}
                      <div className="space-y-2">
                        {Object.entries(health.dimensions).map(([key, dim]) => {
                          const labels: Record<string, string> = {
                            business_case_strength: 'Business Case',
                            procurement_readiness: 'Procurement',
                            objection_coverage: 'Objections',
                            champion_strength: 'Champion',
                            cfo_alignment: 'CFO Align'
                          }
                          return (
                            <div key={key}>
                              <div className="flex items-center justify-between mb-1">
                                <span className="text-[11px] text-slate-400">{labels[key]}</span>
                                <span className="text-[11px] font-semibold" style={{
                                  color: dim.score >= 75 ? '#4ade80' : dim.score >= 50 ? '#facc15' : '#f87171'
                                }}>
                                  {dim.score}
                                </span>
                              </div>
                              <div className="h-1.5 bg-slate-700 rounded-full overflow-hidden">
                                <div
                                  className="h-full rounded-full"
                                  style={{
                                    width: `${dim.score}%`,
                                    backgroundColor: dim.score >= 75 ? '#4ade80' : dim.score >= 50 ? '#facc15' : '#f87171'
                                  }}
                                />
                              </div>
                              <p className="text-[10px] text-slate-500 mt-1 leading-relaxed line-clamp-2">
                                {dim.rationale}
                              </p>
                            </div>
                          )
                        })}
                      </div>

                      {/* Risks */}
                      {health.risks.length > 0 && (
                        <div>
                          <div className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-2">Risks</div>
                          <div className="space-y-1.5">
                            {health.risks.map((risk, i) => (
                              <div key={i} className="flex items-start gap-2 bg-red-400/5 border border-red-400/10 rounded-lg p-2">
                                <AlertTriangle size={10} className="text-red-400 flex-shrink-0 mt-0.5" />
                                <p className="text-[11px] text-red-300 leading-relaxed">{risk}</p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Agent actions */}
                      {health.agent_actions.length > 0 && (
                        <div>
                          <div className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-2">Agent Actions</div>
                          <div className="space-y-1.5">
                            {health.agent_actions.map((action, i) => (
                              <div key={i} className="flex items-start gap-2 bg-indigo-500/5 border border-indigo-500/10 rounded-lg p-2">
                                <Zap size={10} className="text-indigo-400 flex-shrink-0 mt-0.5" />
                                <p className="text-[11px] text-indigo-300 leading-relaxed">{action}</p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      <button
                        onClick={refreshHealth}
                        className="w-full btn-secondary text-xs flex items-center justify-center gap-1.5"
                      >
                        <RefreshCw size={11} /> Refresh Health Score
                      </button>
                    </div>
                  )}

                  {rightPanel === 'health' && !health && (
                    <div className="text-center py-8">
                      <p className="text-sm text-slate-500 mb-3">No health score computed yet.</p>
                      <button onClick={refreshHealth} className="btn-primary text-xs">
                        Score Now
                      </button>
                    </div>
                  )}

                  {/* Agent log */}
                  {rightPanel === 'log' && (
                    <div className="space-y-2">
                      {agentLogs.length === 0 ? (
                        <p className="text-sm text-slate-500 text-center py-6">No agent activity yet.</p>
                      ) : (
                        agentLogs.map((log) => (
                          <div key={log.id} className="p-2.5 bg-slate-900 rounded-lg">
                            <div className="flex items-center gap-2 mb-0.5">
                              <span className="text-[10px] font-semibold text-indigo-400">
                                {log.action_type.replace(/_/g, ' ')}
                              </span>
                              <span className="text-[10px] text-slate-600">
                                {new Date(log.timestamp).toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                              </span>
                            </div>
                            <p className="text-[11px] text-slate-400 leading-relaxed">{log.description}</p>
                          </div>
                        ))
                      )}
                    </div>
                  )}
                </div>

                {/* Approve CTA */}
                {justification?.completeness_score && justification.completeness_score >= 70 && (
                  <div className="p-4 border-t border-slate-800 flex-shrink-0">
                    <button className="w-full btn-primary flex items-center justify-center gap-2">
                      <Send size={14} /> Approve & Send
                    </button>
                    <p className="text-[10px] text-slate-500 text-center mt-1.5">
                      {justification.completeness_score}% complete · Send to {selectedDeal.contact_name}
                    </p>
                  </div>
                )}
              </div>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-slate-500">
            Select a deal from the sidebar
          </div>
        )}
      </div>

      {/* Add Signal Modal */}
      {showSignalModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-slate-800 border border-slate-700 rounded-2xl w-full max-w-lg shadow-2xl">
            <div className="flex items-center justify-between p-5 border-b border-slate-700">
              <h3 className="text-base font-semibold text-slate-100">Add Deal Signal</h3>
              <button onClick={() => setShowSignalModal(false)} className="text-slate-500 hover:text-slate-300">
                <X size={18} />
              </button>
            </div>
            <div className="p-5 space-y-4">
              {/* Signal type */}
              <div>
                <label className="text-xs text-slate-400 mb-2 block">Signal Type</label>
                <div className="flex gap-2">
                  {[
                    { type: 'call', icon: <Phone size={13} />, label: 'Call Transcript' },
                    { type: 'email', icon: <Mail size={13} />, label: 'Email Thread' },
                    { type: 'meeting', icon: <CheckSquare size={13} />, label: 'Meeting Notes' }
                  ].map(({ type, icon, label }) => (
                    <button
                      key={type}
                      onClick={() => setSignal((s) => ({ ...s, type: type as AddSignalModal['type'] }))}
                      className={clsx(
                        'flex-1 flex items-center justify-center gap-1.5 py-2 rounded-lg text-xs font-medium border transition-colors',
                        signal.type === type
                          ? 'bg-indigo-500/20 border-indigo-500/40 text-indigo-300'
                          : 'bg-slate-900 border-slate-700 text-slate-400 hover:border-slate-600'
                      )}
                    >
                      {icon}{label}
                    </button>
                  ))}
                </div>
              </div>

              {/* Content */}
              <div>
                <label className="text-xs text-slate-400 mb-2 block">Content</label>
                <textarea
                  className="input w-full h-48 resize-none text-xs"
                  placeholder={signal.type === 'call'
                    ? "Paste call transcript here... Include attendees, key discussion points, objections raised, and next steps."
                    : signal.type === 'email'
                    ? "Paste email thread here... Include sender, recipient, subject, and full email content."
                    : "Paste meeting notes here... Include attendees, agenda, key decisions, and action items."
                  }
                  value={signal.content}
                  onChange={(e) => setSignal((s) => ({ ...s, content: e.target.value }))}
                />
                <p className="text-[10px] text-slate-500 mt-1">
                  The intelligence agent will analyze this signal and extract pain points, stakeholders, objections, and financial signals.
                </p>
              </div>
            </div>
            <div className="flex items-center justify-end gap-3 p-5 border-t border-slate-700">
              <button onClick={() => setShowSignalModal(false)} className="btn-ghost text-sm">Cancel</button>
              <button
                onClick={addSignal}
                disabled={!signal.content.trim() || addingSignal}
                className="btn-primary text-sm flex items-center gap-2"
              >
                {addingSignal ? <Loader2 size={14} className="animate-spin" /> : <Zap size={14} />}
                {addingSignal ? 'Analyzing...' : 'Add & Analyze'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
