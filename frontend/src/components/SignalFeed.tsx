import { useState } from 'react'
import { Phone, Mail, Users, ChevronDown, ChevronUp, AlertCircle, User, TrendingUp } from 'lucide-react'
import type { DealSignal } from '../types'
import clsx from 'clsx'

interface Props {
  signals: DealSignal[]
}

const SIGNAL_ICONS: Record<string, React.ReactNode> = {
  call: <Phone size={12} />,
  email: <Mail size={12} />,
  meeting: <Users size={12} />
}

function formatDate(ts: string): string {
  const d = new Date(ts)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

function truncate(text: string, len: number): string {
  return text.length > len ? text.slice(0, len) + '...' : text
}

export default function SignalFeed({ signals }: Props) {
  const [expanded, setExpanded] = useState<number | null>(null)

  if (signals.length === 0) {
    return (
      <div className="text-sm text-slate-500 text-center py-8">
        No signals yet. Add a call transcript or email to get started.
      </div>
    )
  }

  return (
    <div className="space-y-2">
      {signals.map((sig) => {
        const isExpanded = expanded === sig.id
        const insights = sig.extracted_insights
        const urgentObjns = insights?.objections?.filter((o) => o.severity === 'blocking') || []
        const champScore = insights?.champion_strength_signal?.score

        return (
          <div
            key={sig.id}
            className={clsx(
              'card-sm overflow-hidden transition-all',
              urgentObjns.length > 0 ? 'border-yellow-500/20' : ''
            )}
          >
            <button
              className="w-full text-left p-3 flex items-start gap-3"
              onClick={() => setExpanded(isExpanded ? null : sig.id)}
            >
              <div className={clsx(
                'flex-shrink-0 w-6 h-6 rounded-md flex items-center justify-center mt-0.5',
                sig.signal_type === 'call' ? 'bg-green-400/10 text-green-400' :
                sig.signal_type === 'email' ? 'bg-blue-400/10 text-blue-400' :
                'bg-purple-400/10 text-purple-400'
              )}>
                {SIGNAL_ICONS[sig.signal_type]}
              </div>

              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-0.5">
                  <span className="text-xs font-medium text-slate-300 capitalize">{sig.signal_type}</span>
                  <span className="text-[10px] text-slate-500">{formatDate(sig.timestamp)}</span>
                  {urgentObjns.length > 0 && (
                    <span className="badge bg-yellow-400/10 text-yellow-400 border border-yellow-400/20">
                      {urgentObjns.length} blocker
                    </span>
                  )}
                </div>
                <p className="text-[11px] text-slate-400 leading-relaxed">
                  {truncate(sig.content, 120)}
                </p>

                {/* Insights preview */}
                {insights && (
                  <div className="mt-1.5 flex items-center gap-2 flex-wrap">
                    {insights.pain_points && insights.pain_points.length > 0 && (
                      <span className="text-[10px] text-slate-500 flex items-center gap-1">
                        <TrendingUp size={9} />{insights.pain_points.length} pain pts
                      </span>
                    )}
                    {insights.stakeholders && insights.stakeholders.length > 0 && (
                      <span className="text-[10px] text-slate-500 flex items-center gap-1">
                        <User size={9} />{insights.stakeholders.length} stakeholders
                      </span>
                    )}
                    {insights.objections && insights.objections.length > 0 && (
                      <span className="text-[10px] text-yellow-500 flex items-center gap-1">
                        <AlertCircle size={9} />{insights.objections.length} objections
                      </span>
                    )}
                    {champScore !== undefined && (
                      <span className="text-[10px] text-slate-500">Champion: {champScore}/10</span>
                    )}
                  </div>
                )}
              </div>

              <div className="flex-shrink-0 text-slate-600">
                {isExpanded ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
              </div>
            </button>

            {isExpanded && (
              <div className="px-3 pb-3 border-t border-slate-700/50">
                {/* Full content preview */}
                <div className="mt-3 mb-3 bg-slate-900 rounded-lg p-3">
                  <p className="text-[11px] text-slate-300 leading-relaxed whitespace-pre-wrap font-mono">
                    {sig.content.slice(0, 800)}{sig.content.length > 800 ? '\n...' : ''}
                  </p>
                </div>

                {insights && (
                  <div className="space-y-3">
                    {/* Pain points */}
                    {insights.pain_points && insights.pain_points.length > 0 && (
                      <div>
                        <div className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Pain Points</div>
                        <div className="space-y-1">
                          {insights.pain_points.map((p, i) => (
                            <div key={i} className="flex items-start gap-2">
                              <span className={clsx(
                                'badge flex-shrink-0 mt-0.5',
                                p.urgency === 'critical' ? 'bg-red-400/10 text-red-400' :
                                p.urgency === 'high' ? 'bg-yellow-400/10 text-yellow-400' :
                                'bg-slate-700 text-slate-400'
                              )}>
                                {p.urgency}
                              </span>
                              <p className="text-[11px] text-slate-300">{p.description}</p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Objections */}
                    {insights.objections && insights.objections.length > 0 && (
                      <div>
                        <div className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Objections</div>
                        <div className="space-y-1">
                          {insights.objections.map((o, i) => (
                            <div key={i} className="flex items-start gap-2">
                              <span className={clsx(
                                'badge flex-shrink-0 mt-0.5',
                                o.severity === 'blocking' ? 'bg-red-400/10 text-red-400' :
                                o.severity === 'significant' ? 'bg-yellow-400/10 text-yellow-400' :
                                'bg-slate-700 text-slate-400'
                              )}>
                                {o.severity}
                              </span>
                              <div>
                                <p className="text-[11px] text-slate-300">{o.objection}</p>
                                {o.raised_by && <p className="text-[10px] text-slate-500">— {o.raised_by}</p>}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Stakeholders */}
                    {insights.stakeholders && insights.stakeholders.length > 0 && (
                      <div>
                        <div className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Stakeholders</div>
                        <div className="space-y-1">
                          {insights.stakeholders.map((s, i) => (
                            <div key={i} className="flex items-center gap-2">
                              <span className={clsx(
                                'badge',
                                s.role === 'champion' ? 'bg-green-400/10 text-green-400' :
                                s.role === 'economic_buyer' ? 'bg-indigo-400/10 text-indigo-400' :
                                s.role === 'blocker' ? 'bg-red-400/10 text-red-400' :
                                'bg-slate-700 text-slate-400'
                              )}>
                                {s.role.replace('_', ' ')}
                              </span>
                              <span className="text-[11px] text-slate-300">{s.name} · {s.title}</span>
                              <span className={clsx(
                                'text-[10px]',
                                s.sentiment === 'positive' ? 'text-green-400' :
                                s.sentiment === 'negative' ? 'text-red-400' :
                                'text-slate-500'
                              )}>
                                {s.sentiment}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
