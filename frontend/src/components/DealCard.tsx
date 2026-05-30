import { useNavigate } from 'react-router-dom'
import { DollarSign, ChevronRight, TrendingUp, AlertTriangle } from 'lucide-react'
import type { PipelineDeal } from '../types'
import HealthScoreRing, { healthBg, healthLabel } from './HealthScoreRing'
import AgentStatusBadge from './AgentStatusBadge'
import clsx from 'clsx'

const STAGE_LABELS: Record<string, string> = {
  discovery: 'Discovery',
  technical_eval: 'Technical Eval',
  business_case: 'Business Case',
  legal: 'Legal',
  closed_won: 'Closed Won',
  closed_lost: 'Closed Lost'
}

const STAGE_COLORS: Record<string, string> = {
  discovery: 'bg-slate-600/60 text-slate-300',
  technical_eval: 'bg-blue-500/15 text-blue-400',
  business_case: 'bg-indigo-500/15 text-indigo-400',
  legal: 'bg-purple-500/15 text-purple-400',
  closed_won: 'bg-green-500/15 text-green-400',
  closed_lost: 'bg-red-500/15 text-red-400'
}

interface Props {
  deal: PipelineDeal
  compact?: boolean
}

export default function DealCard({ deal, compact = false }: Props) {
  const navigate = useNavigate()
  const health = deal.health || deal.latest_health
  const score = health?.overall_score ?? 0

  if (compact) {
    return (
      <button
        onClick={() => navigate(`/workspace/${deal.id}`)}
        className="w-full text-left card-sm p-3 hover:bg-slate-800 transition-colors flex items-center gap-3"
      >
        <HealthScoreRing score={score} size="sm" />
        <div className="flex-1 min-w-0">
          <div className="text-sm font-medium text-slate-100 truncate">{deal.company}</div>
          <div className="text-xs text-slate-400">${(deal.deal_value / 1000).toFixed(0)}K · {STAGE_LABELS[deal.stage] || deal.stage}</div>
        </div>
        <ChevronRight size={14} className="text-slate-500 flex-shrink-0" />
      </button>
    )
  }

  return (
    <div
      onClick={() => navigate(`/workspace/${deal.id}`)}
      className="card p-5 hover:border-slate-600 transition-colors cursor-pointer group"
    >
      <div className="flex items-start justify-between gap-3 mb-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-0.5">
            <h3 className="font-semibold text-slate-100 text-base group-hover:text-indigo-400 transition-colors truncate">
              {deal.company}
            </h3>
            {deal.justification_status && (
              <AgentStatusBadge status={deal.justification_status.agent_status} size="sm" />
            )}
          </div>
          <p className="text-sm text-slate-400 truncate">{deal.contact_name} · {deal.contact_title}</p>
        </div>
        <HealthScoreRing score={score} size="md" showLabel />
      </div>

      {/* Metrics row */}
      <div className="flex items-center gap-4 mb-4">
        <div className="flex items-center gap-1.5">
          <DollarSign size={13} className="text-slate-500" />
          <span className="text-sm font-semibold text-slate-200">
            ${(deal.deal_value / 1000).toFixed(0)}K
          </span>
        </div>
        <span className={clsx('badge border', STAGE_COLORS[deal.stage] || 'bg-slate-700 text-slate-400')}>
          {STAGE_LABELS[deal.stage] || deal.stage}
        </span>
        <span className="text-xs text-slate-500">{deal.signal_count || 0} signals</span>
      </div>

      {/* Health dimensions mini bar */}
      {health?.dimensions && (
        <div className="space-y-1.5 mb-4">
          {Object.entries(health.dimensions).map(([key, dim]) => {
            const labels: Record<string, string> = {
              business_case_strength: 'Business Case',
              procurement_readiness: 'Procurement',
              objection_coverage: 'Objections',
              champion_strength: 'Champion',
              cfo_alignment: 'CFO Align'
            }
            return (
              <div key={key} className="flex items-center gap-2">
                <span className="text-[10px] text-slate-500 w-20 flex-shrink-0">{labels[key]}</span>
                <div className="flex-1 h-1.5 bg-slate-700 rounded-full overflow-hidden">
                  <div
                    className="h-full rounded-full transition-all"
                    style={{
                      width: `${dim.score}%`,
                      backgroundColor: dim.score >= 75 ? '#4ade80' : dim.score >= 50 ? '#facc15' : '#f87171'
                    }}
                  />
                </div>
                <span className="text-[10px] text-slate-500 w-6 text-right">{dim.score}</span>
              </div>
            )
          })}
        </div>
      )}

      {/* Top risk */}
      {health?.risks?.[0] && (
        <div className="flex items-start gap-2 bg-red-400/5 border border-red-400/10 rounded-lg px-3 py-2">
          <AlertTriangle size={12} className="text-red-400 flex-shrink-0 mt-0.5" />
          <p className="text-[11px] text-red-300 leading-relaxed line-clamp-2">{health.risks[0]}</p>
        </div>
      )}

      {/* Completeness bar */}
      {deal.justification_status && (
        <div className="mt-3 flex items-center gap-2">
          <TrendingUp size={12} className="text-slate-500" />
          <div className="flex-1 h-1 bg-slate-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-indigo-500 rounded-full transition-all"
              style={{ width: `${deal.justification_status.completeness_score}%` }}
            />
          </div>
          <span className="text-[10px] text-slate-500">{deal.justification_status.completeness_score}% complete</span>
        </div>
      )}
    </div>
  )
}
