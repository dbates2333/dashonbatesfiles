import { useState } from 'react'
import type { ObjectionResponse } from '../types'
import { CheckCircle2, AlertCircle, Clock, ChevronDown, ChevronUp, User } from 'lucide-react'
import clsx from 'clsx'

interface Props {
  objections: ObjectionResponse[]
  onUpdate?: (updated: ObjectionResponse[]) => void
}

const STATUS_CONFIG = {
  addressed: { icon: <CheckCircle2 size={13} />, label: 'Addressed', className: 'bg-green-400/10 text-green-400 border-green-400/20' },
  needs_follow_up: { icon: <AlertCircle size={13} />, label: 'Needs Follow-Up', className: 'bg-yellow-400/10 text-yellow-400 border-yellow-400/20' },
  escalated: { icon: <Clock size={13} />, label: 'Escalated', className: 'bg-red-400/10 text-red-400 border-red-400/20' }
}

const CATEGORY_COLORS: Record<string, string> = {
  price: 'text-red-400',
  roi: 'text-yellow-400',
  integration: 'text-blue-400',
  security: 'text-orange-400',
  timeline: 'text-purple-400',
  vendor_risk: 'text-red-400',
  procurement: 'text-indigo-400',
  competitive: 'text-pink-400',
  technical: 'text-cyan-400'
}

export default function ObjectionHandler({ objections, onUpdate }: Props) {
  const [expanded, setExpanded] = useState<number | null>(null)
  const [editing, setEditing] = useState<number | null>(null)
  const [editText, setEditText] = useState('')

  if (!objections || objections.length === 0) {
    return (
      <div className="text-sm text-slate-500 text-center py-8">
        No objections identified yet. Add signals with call transcripts to extract objections.
      </div>
    )
  }

  const statusOrder = { addressed: 0, needs_follow_up: 1, escalated: 2 }
  const sorted = [...objections].sort((a, b) => (statusOrder[a.status] ?? 3) - (statusOrder[b.status] ?? 3))

  return (
    <div className="space-y-2">
      {/* Summary */}
      <div className="flex items-center gap-3 mb-4">
        {(['addressed', 'needs_follow_up', 'escalated'] as const).map((status) => {
          const count = objections.filter((o) => o.status === status).length
          const cfg = STATUS_CONFIG[status]
          return (
            <div key={status} className={clsx('flex items-center gap-1.5 badge border text-xs', cfg.className)}>
              {cfg.icon}
              <span>{count} {cfg.label}</span>
            </div>
          )
        })}
      </div>

      {sorted.map((obj, i) => {
        const isExpanded = expanded === i
        const isEditing = editing === i
        const cfg = STATUS_CONFIG[obj.status] || STATUS_CONFIG['needs_follow_up']

        return (
          <div key={i} className={clsx(
            'card-sm overflow-hidden',
            obj.status === 'needs_follow_up' && 'border-yellow-500/20',
            obj.status === 'escalated' && 'border-red-500/20'
          )}>
            <button
              className="w-full text-left p-3 flex items-start gap-3"
              onClick={() => setExpanded(isExpanded ? null : i)}
            >
              <span className={clsx('badge border flex-shrink-0 mt-0.5', cfg.className)}>
                {cfg.icon}
              </span>
              <div className="flex-1 min-w-0">
                <p className="text-sm text-slate-100 leading-snug">{obj.objection}</p>
                <div className="flex items-center gap-2 mt-1">
                  {obj.raised_by && (
                    <span className="flex items-center gap-1 text-[10px] text-slate-500">
                      <User size={9} />{obj.raised_by}
                    </span>
                  )}
                  {obj.category && (
                    <span className={clsx('text-[10px] font-medium', CATEGORY_COLORS[obj.category] || 'text-slate-500')}>
                      {obj.category.replace('_', ' ')}
                    </span>
                  )}
                </div>
              </div>
              {isExpanded ? <ChevronUp size={13} className="text-slate-500 flex-shrink-0 mt-1" /> : <ChevronDown size={13} className="text-slate-500 flex-shrink-0 mt-1" />}
            </button>

            {isExpanded && (
              <div className="px-3 pb-3 border-t border-slate-700/50 space-y-3">
                {/* Response */}
                <div className="mt-3">
                  <div className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Agent Response</div>
                  {isEditing ? (
                    <div>
                      <textarea
                        className="input w-full h-32 resize-none text-[12px]"
                        value={editText}
                        onChange={(e) => setEditText(e.target.value)}
                      />
                      <div className="flex gap-2 mt-2">
                        <button
                          className="btn-primary text-xs py-1"
                          onClick={() => {
                            if (onUpdate) {
                              const updated = objections.map((o, idx) =>
                                idx === i ? { ...o, response: editText } : o
                              )
                              onUpdate(updated)
                            }
                            setEditing(null)
                          }}
                        >
                          Save
                        </button>
                        <button className="btn-ghost text-xs" onClick={() => setEditing(null)}>Cancel</button>
                      </div>
                    </div>
                  ) : (
                    <div>
                      <p className="text-[12px] text-slate-300 leading-relaxed">{obj.response}</p>
                      <button
                        className="text-[10px] text-indigo-400 hover:text-indigo-300 mt-1.5"
                        onClick={(e) => { e.stopPropagation(); setEditing(i); setEditText(obj.response) }}
                      >
                        Edit response
                      </button>
                    </div>
                  )}
                </div>

                {/* Supporting data */}
                {obj.supporting_data && (
                  <div>
                    <div className="text-[10px] font-semibold text-slate-500 uppercase tracking-wider mb-1">Supporting Data</div>
                    <p className="text-[11px] text-slate-400 bg-slate-900 rounded-lg p-2">{obj.supporting_data}</p>
                  </div>
                )}

                {/* Follow-up action */}
                {obj.follow_up_action && (
                  <div className="flex items-start gap-2 bg-indigo-500/5 border border-indigo-500/15 rounded-lg p-2.5">
                    <Clock size={11} className="text-indigo-400 flex-shrink-0 mt-0.5" />
                    <p className="text-[11px] text-indigo-300">{obj.follow_up_action}</p>
                  </div>
                )}

                {/* Status control */}
                {onUpdate && (
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] text-slate-500">Status:</span>
                    {(['addressed', 'needs_follow_up', 'escalated'] as const).map((s) => (
                      <button
                        key={s}
                        onClick={() => {
                          const updated = objections.map((o, idx) =>
                            idx === i ? { ...o, status: s } : o
                          )
                          onUpdate(updated)
                        }}
                        className={clsx(
                          'badge border text-[10px] cursor-pointer hover:opacity-80',
                          STATUS_CONFIG[s].className,
                          obj.status === s ? 'opacity-100' : 'opacity-40'
                        )}
                      >
                        {STATUS_CONFIG[s].label}
                      </button>
                    ))}
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
