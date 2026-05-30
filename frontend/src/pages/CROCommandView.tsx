import { useEffect, useState, useCallback } from 'react'
import { RefreshCw, DollarSign, Activity, AlertTriangle, Cpu } from 'lucide-react'
import type { PipelineDeal, PipelineAlert, PipelineStats } from '../types'
import * as api from '../api/client'
import PipelineHealthMap from '../components/PipelineHealthMap'
import AlertPanel from '../components/AlertPanel'
import DealCard from '../components/DealCard'
import { healthColor } from '../components/HealthScoreRing'
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer, Tooltip } from 'recharts'
import clsx from 'clsx'

function StatCard({ icon, label, value, sub, accent }: {
  icon: React.ReactNode
  label: string
  value: string | number
  sub?: string
  accent?: 'green' | 'yellow' | 'red' | 'indigo'
}) {
  const colors = {
    green: 'text-green-400',
    yellow: 'text-yellow-400',
    red: 'text-red-400',
    indigo: 'text-indigo-400'
  }
  return (
    <div className="card p-4">
      <div className="flex items-center gap-2 mb-2">
        <div className="text-slate-500">{icon}</div>
        <span className="text-xs text-slate-500">{label}</span>
      </div>
      <div className={clsx('text-2xl font-bold', accent ? colors[accent] : 'text-slate-100')}>{value}</div>
      {sub && <div className="text-[11px] text-slate-500 mt-0.5">{sub}</div>}
    </div>
  )
}

function fmt(n: number): string {
  if (n >= 1_000_000) return `$${(n / 1_000_000).toFixed(2)}M`
  if (n >= 1_000) return `$${(n / 1_000).toFixed(0)}K`
  return `$${n}`
}

export default function CROCommandView() {
  const [deals, setDeals] = useState<PipelineDeal[]>([])
  const [alerts, setAlerts] = useState<PipelineAlert[]>([])
  const [stats, setStats] = useState<PipelineStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [expandedDeal, setExpandedDeal] = useState<number | null>(null)

  const load = useCallback(async () => {
    try {
      const [d, a, s] = await Promise.all([api.getPipeline(), api.getAlerts(), api.getStats()])
      setDeals(d)
      setAlerts(a)
      setStats(s)
    } catch (e) {
      console.error('Failed to load pipeline data:', e)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  const refresh = async () => {
    setRefreshing(true)
    await load()
    setRefreshing(false)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="flex items-center gap-3 text-slate-400">
          <RefreshCw size={18} className="animate-spin" />
          <span>Loading pipeline data...</span>
        </div>
      </div>
    )
  }

  const buildingDeals = deals.filter((d) => d.justification_status?.agent_status === 'building')

  return (
    <div className="h-full overflow-y-auto">
      <div className="max-w-screen-2xl mx-auto px-6 py-5 space-y-5">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-lg font-bold text-slate-100">CRO Command View</h1>
            <p className="text-sm text-slate-400">Real-time pipeline health · {deals.length} active deals</p>
          </div>
          <div className="flex items-center gap-3">
            {buildingDeals.length > 0 && (
              <div className="flex items-center gap-2 bg-indigo-500/10 border border-indigo-500/20 px-3 py-1.5 rounded-full">
                <Cpu size={12} className="text-indigo-400 animate-pulse" />
                <span className="text-xs text-indigo-400">Agent working on {buildingDeals.length} deal{buildingDeals.length > 1 ? 's' : ''}</span>
              </div>
            )}
            <button
              onClick={refresh}
              disabled={refreshing}
              className="btn-ghost text-sm flex items-center gap-1.5"
            >
              <RefreshCw size={13} className={refreshing ? 'animate-spin' : ''} />
              Refresh
            </button>
          </div>
        </div>

        {/* Stats row */}
        {stats && (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
            <StatCard
              icon={<DollarSign size={15} />}
              label="Total Pipeline"
              value={fmt(stats.total_pipeline_value)}
              sub={`${stats.total_deals} deals`}
              accent="indigo"
            />
            <StatCard
              icon={<Activity size={15} />}
              label="Avg Health"
              value={`${stats.avg_health_score.toFixed(0)}/100`}
              sub="across all deals"
              accent={stats.avg_health_score >= 75 ? 'green' : stats.avg_health_score >= 50 ? 'yellow' : 'red'}
            />
            <StatCard
              icon={<Activity size={15} />}
              label="Healthy Deals"
              value={stats.healthy_count}
              sub="score ≥ 75"
              accent="green"
            />
            <StatCard
              icon={<AlertTriangle size={15} />}
              label="At Risk"
              value={stats.at_risk_count}
              sub="score < 60"
              accent={stats.at_risk_count > 0 ? 'red' : 'green'}
            />
            <StatCard
              icon={<Cpu size={15} />}
              label="Agent Building"
              value={stats.building_count}
              sub="actively generating"
              accent="indigo"
            />
            {Object.entries(stats.completeness_distribution).map(([bucket, count]) => (
              bucket === '91-100' ? (
                <StatCard
                  key={bucket}
                  icon={<Activity size={15} />}
                  label="Fully Built"
                  value={count}
                  sub="completeness >90%"
                  accent="green"
                />
              ) : null
            ))}
          </div>
        )}

        {/* Pipeline health map */}
        <PipelineHealthMap deals={deals} />

        {/* Alerts + deal grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
          <div className="lg:col-span-1">
            <AlertPanel alerts={alerts} />
          </div>
          <div className="lg:col-span-2 space-y-3">
            <h2 className="text-sm font-semibold text-slate-100">All Deals</h2>
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-3">
              {deals.map((deal) => (
                <div key={deal.id}>
                  <DealCard deal={deal} />
                  {/* Expanded radar chart */}
                  {expandedDeal === deal.id && deal.health?.dimensions && (
                    <div className="mt-2 card p-4 fade-in">
                      <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Dimension Breakdown</h4>
                      <ResponsiveContainer width="100%" height={180}>
                        <RadarChart data={Object.entries(deal.health.dimensions).map(([key, val]) => ({
                          subject: key.split('_').map((w) => w[0].toUpperCase() + w.slice(1)).join(' '),
                          score: val.score
                        }))}>
                          <PolarGrid stroke="#334155" />
                          <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 10 }} />
                          <Radar name="Score" dataKey="score" stroke="#6366f1" fill="#6366f1" fillOpacity={0.15} />
                          <Tooltip
                            contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '8px' }}
                            labelStyle={{ color: '#94a3b8', fontSize: 11 }}
                            itemStyle={{ color: '#a5b4fc', fontSize: 11 }}
                          />
                        </RadarChart>
                      </ResponsiveContainer>
                      <div className="space-y-1.5 mt-2">
                        {Object.entries(deal.health.dimensions).map(([key, dim]) => (
                          <div key={key} className="text-[11px] text-slate-400 line-clamp-2">
                            <span className="font-medium text-slate-300">{key.split('_').map((w) => w[0].toUpperCase() + w.slice(1)).join(' ')}:</span>{' '}
                            {dim.rationale.slice(0, 100)}...
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  <button
                    className="w-full text-[10px] text-slate-600 hover:text-slate-400 mt-1 transition-colors"
                    onClick={() => setExpandedDeal(expandedDeal === deal.id ? null : deal.id)}
                  >
                    {expandedDeal === deal.id ? 'Collapse' : 'Show dimensions'}
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
