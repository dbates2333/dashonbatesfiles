import { useNavigate } from 'react-router-dom'
import type { PipelineDeal } from '../types'
import { healthColor } from './HealthScoreRing'
import clsx from 'clsx'

interface Props {
  deals: PipelineDeal[]
}

const STAGE_ORDER = ['discovery', 'technical_eval', 'business_case', 'legal', 'closed_won']

export default function PipelineHealthMap({ deals }: Props) {
  const navigate = useNavigate()

  // Sort by deal value descending
  const sorted = [...deals].sort((a, b) => b.deal_value - a.deal_value)
  const totalValue = sorted.reduce((sum, d) => sum + d.deal_value, 0)

  return (
    <div className="card p-5">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-sm font-semibold text-slate-100">Pipeline Health Map</h2>
          <p className="text-xs text-slate-500 mt-0.5">All deals · sized by deal value · colored by health score</p>
        </div>
        <div className="flex items-center gap-4 text-xs text-slate-500">
          <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-green-400" />≥75 Healthy</span>
          <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-yellow-400" />50–74 At Risk</span>
          <span className="flex items-center gap-1.5"><span className="w-2 h-2 rounded-full bg-red-400" />&lt;50 Exposed</span>
        </div>
      </div>

      {/* Horizontal bar layout */}
      <div className="flex gap-1 h-16 rounded-lg overflow-hidden">
        {sorted.map((deal) => {
          const health = deal.health || deal.latest_health
          const score = health?.overall_score ?? 0
          const widthPct = (deal.deal_value / totalValue) * 100
          const color = healthColor(score)

          return (
            <button
              key={deal.id}
              onClick={() => navigate(`/workspace/${deal.id}`)}
              className="relative flex-shrink-0 group h-full rounded-sm overflow-hidden transition-opacity hover:opacity-90"
              style={{
                width: `${widthPct}%`,
                backgroundColor: color + '22',
                borderLeft: `3px solid ${color}`
              }}
              title={`${deal.company}: ${score.toFixed(0)}/100 · $${(deal.deal_value / 1000).toFixed(0)}K`}
            >
              <div className="absolute inset-0 flex flex-col justify-end p-1.5">
                <div className="text-[9px] font-semibold leading-none truncate" style={{ color }}>
                  {deal.company.split(' ')[0]}
                </div>
                <div className="text-[8px] text-slate-400 mt-0.5">
                  {score.toFixed(0)}
                </div>
              </div>
              {/* Hover tooltip */}
              <div className="absolute inset-0 bg-slate-900/90 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center p-1">
                <span className="text-[10px] font-semibold text-white truncate w-full text-center">{deal.company}</span>
                <span className="text-[9px] text-slate-300">${(deal.deal_value / 1000).toFixed(0)}K</span>
                <span className="text-[9px] font-bold mt-0.5" style={{ color }}>{score.toFixed(0)}/100</span>
              </div>
            </button>
          )
        })}
      </div>

      {/* Stage pipeline below */}
      <div className="mt-4 grid grid-cols-5 gap-2">
        {STAGE_ORDER.map((stage) => {
          const stageDeals = sorted.filter((d) => d.stage === stage)
          const stageValue = stageDeals.reduce((s, d) => s + d.deal_value, 0)
          const labels: Record<string, string> = {
            discovery: 'Discovery',
            technical_eval: 'Technical Eval',
            business_case: 'Business Case',
            legal: 'Legal',
            closed_won: 'Closed Won'
          }
          return (
            <div key={stage} className="bg-slate-900 rounded-lg p-2.5">
              <div className="text-[10px] text-slate-500 mb-1">{labels[stage]}</div>
              <div className="text-sm font-semibold text-slate-200">{stageDeals.length} deal{stageDeals.length !== 1 ? 's' : ''}</div>
              <div className="text-[11px] text-slate-400">${(stageValue / 1000).toFixed(0)}K</div>
              <div className="mt-1.5 space-y-0.5">
                {stageDeals.map((d) => {
                  const h = d.health || d.latest_health
                  const s = h?.overall_score ?? 0
                  return (
                    <div key={d.id} className="flex items-center gap-1">
                      <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ backgroundColor: healthColor(s) }} />
                      <span className="text-[9px] text-slate-400 truncate">{d.company.split(' ')[0]}</span>
                    </div>
                  )
                })}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
