import { useNavigate } from 'react-router-dom'
import { AlertTriangle, AlertCircle, ChevronRight } from 'lucide-react'
import type { PipelineAlert } from '../types'
import clsx from 'clsx'

interface Props {
  alerts: PipelineAlert[]
}

export default function AlertPanel({ alerts }: Props) {
  const navigate = useNavigate()

  if (alerts.length === 0) {
    return (
      <div className="card p-5">
        <h2 className="text-sm font-semibold text-slate-100 mb-3">Active Alerts</h2>
        <div className="text-sm text-slate-500 text-center py-6">No critical alerts — pipeline is healthy.</div>
      </div>
    )
  }

  return (
    <div className="card p-5">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-semibold text-slate-100">Active Alerts</h2>
        <span className="badge bg-red-400/10 text-red-400 border border-red-400/20">{alerts.length} deals need attention</span>
      </div>

      <div className="space-y-2">
        {alerts.map((alertDeal) => {
          const hasEscalation = alertDeal.alerts.some((a) => a.severity === 'critical')
          return (
            <div
              key={alertDeal.deal_id}
              className={clsx(
                'rounded-lg border p-3 cursor-pointer hover:border-slate-500 transition-colors',
                hasEscalation
                  ? 'bg-red-950/30 border-red-500/20'
                  : 'bg-yellow-950/20 border-yellow-500/20'
              )}
              onClick={() => navigate(`/workspace/${alertDeal.deal_id}`)}
            >
              <div className="flex items-center justify-between gap-2 mb-2">
                <div className="flex items-center gap-2">
                  {hasEscalation
                    ? <AlertTriangle size={14} className="text-red-400 flex-shrink-0" />
                    : <AlertCircle size={14} className="text-yellow-400 flex-shrink-0" />
                  }
                  <span className="text-sm font-medium text-slate-100">{alertDeal.company}</span>
                  <span className={clsx(
                    'badge border text-[10px]',
                    hasEscalation
                      ? 'bg-red-400/10 text-red-400 border-red-400/20'
                      : 'bg-yellow-400/10 text-yellow-400 border-yellow-400/20'
                  )}>
                    {alertDeal.overall_score.toFixed(0)}/100
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-400">${(alertDeal.deal_value / 1000).toFixed(0)}K</span>
                  <ChevronRight size={13} className="text-slate-500" />
                </div>
              </div>

              <div className="space-y-1">
                {alertDeal.alerts.slice(0, 3).map((alert, i) => (
                  <div key={i} className="flex items-start gap-1.5">
                    <span className={clsx(
                      'w-1 h-1 rounded-full flex-shrink-0 mt-1.5',
                      alert.severity === 'critical' ? 'bg-red-400' :
                      alert.severity === 'high' ? 'bg-yellow-400' : 'bg-slate-500'
                    )} />
                    <p className="text-[11px] text-slate-300 leading-relaxed line-clamp-2">{alert.message}</p>
                  </div>
                ))}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
