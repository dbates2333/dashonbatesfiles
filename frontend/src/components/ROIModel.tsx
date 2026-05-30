import type { ROIModel as ROIModelType } from '../types'
import { TrendingUp, DollarSign, Clock, AlertCircle } from 'lucide-react'
import clsx from 'clsx'

interface Props {
  roi: ROIModelType
}

function fmt(n: number): string {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(2)}M`
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`
  return `$${n.toFixed(0)}`
}

function confBadge(conf: string) {
  return clsx(
    'badge text-[9px]',
    conf === 'high' ? 'bg-green-400/10 text-green-400' :
    conf === 'medium' ? 'bg-yellow-400/10 text-yellow-400' :
    'bg-red-400/10 text-red-400'
  )
}

export default function ROIModel({ roi }: Props) {
  const base = roi.scenarios?.base
  const conservative = roi.scenarios?.conservative
  const optimistic = roi.scenarios?.optimistic

  return (
    <div className="space-y-5">
      {/* Scenario cards */}
      {base && (
        <div className="grid grid-cols-3 gap-3">
          {[
            { label: 'Conservative', s: conservative, dim: true },
            { label: 'Base Case', s: base, dim: false },
            { label: 'Optimistic', s: optimistic, dim: true }
          ].filter(({ s }) => s).map(({ label, s, dim }) => (
            <div key={label} className={clsx(
              'rounded-xl p-4 border',
              !dim
                ? 'bg-indigo-500/10 border-indigo-500/30'
                : 'bg-slate-800/60 border-slate-700/60'
            )}>
              <div className="text-xs text-slate-400 mb-3 font-medium">{label}</div>
              <div className="space-y-2">
                <div>
                  <div className="text-[10px] text-slate-500">3-Year ROI</div>
                  <div className={clsx('text-xl font-bold', !dim ? 'text-indigo-400' : 'text-slate-200')}>
                    {s!.three_year_roi_percent.toFixed(0)}%
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <div className="text-[10px] text-slate-500">Payback</div>
                    <div className="text-sm font-semibold text-slate-200">{s!.payback_months.toFixed(1)}mo</div>
                  </div>
                  <div>
                    <div className="text-[10px] text-slate-500">3-Yr NPV</div>
                    <div className="text-sm font-semibold text-slate-200">{fmt(s!.three_year_npv)}</div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Investment summary */}
      <div className="grid grid-cols-3 gap-3">
        <div className="bg-slate-900 rounded-lg p-3">
          <div className="flex items-center gap-1.5 mb-1">
            <DollarSign size={12} className="text-slate-500" />
            <span className="text-[10px] text-slate-500">Total Investment</span>
          </div>
          <div className="text-base font-bold text-slate-100">{fmt(roi.total_investment)}</div>
        </div>
        <div className="bg-slate-900 rounded-lg p-3">
          <div className="flex items-center gap-1.5 mb-1">
            <TrendingUp size={12} className="text-slate-500" />
            <span className="text-[10px] text-slate-500">Annual Contract</span>
          </div>
          <div className="text-base font-bold text-slate-100">{fmt(roi.annual_contract_value)}</div>
        </div>
        <div className="bg-slate-900 rounded-lg p-3">
          <div className="flex items-center gap-1.5 mb-1">
            <Clock size={12} className="text-slate-500" />
            <span className="text-[10px] text-slate-500">Implementation</span>
          </div>
          <div className="text-base font-bold text-slate-100">{fmt(roi.implementation_cost)}</div>
        </div>
      </div>

      {/* Annual savings waterfall */}
      {base && (
        <div>
          <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Projected Annual Savings (Base)</h4>
          <div className="space-y-2">
            {[
              { label: 'Year 1', value: base.annual_savings_year1, note: 'Implementation year' },
              { label: 'Year 2', value: base.annual_savings_year2 },
              { label: 'Year 3', value: base.annual_savings_year3 }
            ].map(({ label, value, note }) => {
              const max = base.annual_savings_year3
              return (
                <div key={label} className="flex items-center gap-3">
                  <span className="text-xs text-slate-400 w-10">{label}</span>
                  <div className="flex-1 h-6 bg-slate-900 rounded-md overflow-hidden">
                    <div
                      className="h-full bg-indigo-500/40 rounded-md flex items-center px-2 transition-all"
                      style={{ width: `${(value / max) * 100}%` }}
                    >
                      <span className="text-[11px] font-semibold text-indigo-300 whitespace-nowrap">{fmt(value)}</span>
                    </div>
                  </div>
                  {note && <span className="text-[10px] text-slate-500 w-24">{note}</span>}
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Benefit components */}
      {roi.benefit_components && roi.benefit_components.length > 0 && (
        <div>
          <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Value Drivers</h4>
          <div className="space-y-2">
            {roi.benefit_components.map((b, i) => (
              <div key={i} className="flex items-start justify-between gap-3 p-2.5 bg-slate-900 rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-0.5">
                    <span className="text-xs font-medium text-slate-200">{b.category}</span>
                    <span className={confBadge(b.confidence)}>{b.confidence}</span>
                  </div>
                  <p className="text-[11px] text-slate-400">{b.description}</p>
                </div>
                <div className="text-sm font-bold text-green-400 whitespace-nowrap">{fmt(b.annual_value)}/yr</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Cost components */}
      {roi.cost_components && roi.cost_components.length > 0 && (
        <div>
          <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Cost Structure</h4>
          <div className="space-y-2">
            {roi.cost_components.map((c, i) => (
              <div key={i} className="flex items-start justify-between gap-3 p-2.5 bg-slate-900 rounded-lg">
                <div className="flex-1">
                  <span className="text-xs font-medium text-slate-200">{c.category}</span>
                  {c.description && <p className="text-[11px] text-slate-400 mt-0.5">{c.description}</p>}
                </div>
                <div className="text-sm font-bold text-red-400 whitespace-nowrap">{fmt(c.annual_cost)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Assumptions */}
      {roi.assumptions && roi.assumptions.length > 0 && (
        <div>
          <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Key Assumptions</h4>
          <div className="space-y-1.5">
            {roi.assumptions.map((a, i) => (
              <div key={i} className="flex items-start gap-2.5 p-2 bg-slate-900 rounded-lg">
                <span className={confBadge(a.confidence)}>{a.confidence}</span>
                <div className="flex-1">
                  <span className="text-xs text-slate-300">{a.label}: </span>
                  <span className="text-xs font-medium text-slate-100">{a.value}</span>
                  <p className="text-[10px] text-slate-500 mt-0.5">{a.source}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {roi.assumptions && roi.assumptions.some((a) => a.confidence === 'low') && (
        <div className="flex items-start gap-2 bg-yellow-400/5 border border-yellow-400/15 rounded-lg p-3">
          <AlertCircle size={13} className="text-yellow-400 flex-shrink-0 mt-0.5" />
          <p className="text-[11px] text-yellow-300">Some assumptions have low confidence. Validate with the customer before presenting this model to CFO.</p>
        </div>
      )}
    </div>
  )
}
