import { useState } from 'react'
import type { Justification, ObjectionResponse } from '../types'
import ROIModel from './ROIModel'
import ObjectionHandler from './ObjectionHandler'
import AgentStatusBadge from './AgentStatusBadge'
import { Edit3, Save, X, FileText, TrendingUp, Shield, MessageSquare, BarChart2 } from 'lucide-react'
import clsx from 'clsx'

interface Props {
  justification: Justification
  onUpdate: (updates: Partial<Justification>) => void
}

const TABS = [
  { id: 'overview', label: 'Overview', icon: <BarChart2 size={13} /> },
  { id: 'roi', label: 'ROI Model', icon: <TrendingUp size={13} /> },
  { id: 'exec', label: 'Exec Summary', icon: <FileText size={13} /> },
  { id: 'procurement', label: 'Procurement', icon: <Shield size={13} /> },
  { id: 'objections', label: 'Objections', icon: <MessageSquare size={13} /> }
]

function MarkdownRenderer({ text }: { text: string }) {
  // Simple markdown-ish rendering
  const lines = text.split('\n')
  return (
    <div className="prose-custom">
      {lines.map((line, i) => {
        if (line.startsWith('## ')) return <h2 key={i} className="text-base font-bold text-slate-100 mt-4 mb-2 first:mt-0">{line.slice(3)}</h2>
        if (line.startsWith('### ')) return <h3 key={i} className="text-sm font-semibold text-slate-200 mt-3 mb-1.5">{line.slice(4)}</h3>
        if (line.startsWith('#### ')) return <h4 key={i} className="text-xs font-semibold text-slate-300 uppercase tracking-wide mt-2 mb-1">{line.slice(5)}</h4>
        if (line.startsWith('- ')) return <li key={i} className="text-[12px] text-slate-300 ml-4 mb-0.5 list-disc">{line.slice(2)}</li>
        if (line.startsWith('| ') && line.endsWith(' |')) {
          const cells = line.split('|').filter((c) => c.trim())
          const isHeader = lines[i + 1]?.includes('---')
          if (isHeader) return null
          if (lines[i - 1]?.includes('---')) {
            return (
              <table key={i} className="w-full text-[11px] mt-1 mb-2">
                <thead><tr>{cells.map((c, j) => <th key={j} className="text-left py-1 px-2 text-slate-400 bg-slate-900 font-medium border border-slate-700">{c.trim()}</th>)}</tr></thead>
              </table>
            )
          }
          return <tr key={i}>{cells.map((c, j) => <td key={j} className="py-1 px-2 text-slate-300 border border-slate-700">{c.trim()}</td>)}</tr>
        }
        if (line.startsWith('**') && line.endsWith('**')) return <p key={i} className="text-xs font-bold text-slate-200 mt-1">{line.slice(2, -2)}</p>
        if (line.trim() === '' || line === '---') return <div key={i} className="h-2" />
        return <p key={i} className="text-[12px] text-slate-300 leading-relaxed mb-1">{line}</p>
      })}
    </div>
  )
}

export default function ArtifactPanel({ justification, onUpdate }: Props) {
  const [activeTab, setActiveTab] = useState('overview')
  const [editingExec, setEditingExec] = useState(false)
  const [editingProcurement, setEditingProcurement] = useState(false)
  const [execDraft, setExecDraft] = useState(justification.exec_summary || '')
  const [procDraft, setProcDraft] = useState(justification.procurement_doc || '')

  const sections = {
    roi: !!justification.roi_model,
    exec: !!justification.exec_summary,
    procurement: !!justification.procurement_doc,
    objections: !!(justification.objection_responses && justification.objection_responses.length > 0)
  }

  return (
    <div className="flex flex-col h-full">
      {/* Tab bar */}
      <div className="flex items-center gap-0.5 border-b border-slate-700 px-4 flex-shrink-0">
        {TABS.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={clsx(
              'flex items-center gap-1.5 px-3 py-2.5 text-xs font-medium transition-colors border-b-2 -mb-px',
              activeTab === tab.id
                ? 'border-indigo-500 text-slate-100'
                : 'border-transparent text-slate-400 hover:text-slate-300'
            )}
          >
            {tab.icon}
            {tab.label}
            {tab.id !== 'overview' && (
              <span className={clsx(
                'w-1.5 h-1.5 rounded-full',
                sections[tab.id as keyof typeof sections] ? 'bg-green-400' : 'bg-slate-600'
              )} />
            )}
          </button>
        ))}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-5">
        {/* Overview tab */}
        {activeTab === 'overview' && (
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="flex-1">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-semibold text-slate-100">Justification Completeness</h3>
                  <AgentStatusBadge status={justification.agent_status} />
                </div>
                <div className="h-3 bg-slate-900 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-indigo-500 rounded-full transition-all"
                    style={{ width: `${justification.completeness_score}%` }}
                  />
                </div>
                <div className="flex items-center justify-between mt-1">
                  <span className="text-[10px] text-slate-500">
                    {justification.last_updated
                      ? `Last updated ${new Date(justification.last_updated).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}`
                      : 'Not yet built'}
                  </span>
                  <span className="text-xs font-bold text-indigo-400">{justification.completeness_score}%</span>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              {[
                { key: 'roi', label: 'ROI Model', tab: 'roi' },
                { key: 'exec', label: 'Exec Summary', tab: 'exec' },
                { key: 'procurement', label: 'Procurement Doc', tab: 'procurement' },
                { key: 'objections', label: 'Objection Responses', tab: 'objections' }
              ].map(({ key, label, tab }) => {
                const complete = sections[key as keyof typeof sections]
                return (
                  <button
                    key={key}
                    onClick={() => setActiveTab(tab)}
                    className={clsx(
                      'p-3 rounded-xl border text-left transition-colors',
                      complete
                        ? 'bg-green-400/5 border-green-400/20 hover:bg-green-400/10'
                        : 'bg-slate-900 border-slate-700 hover:bg-slate-800'
                    )}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <div className={clsx('w-2 h-2 rounded-full', complete ? 'bg-green-400' : 'bg-slate-600')} />
                      <span className="text-xs font-medium text-slate-200">{label}</span>
                    </div>
                    <span className={clsx('text-[10px]', complete ? 'text-green-400' : 'text-slate-500')}>
                      {complete ? 'Complete — click to view' : 'Not built yet'}
                    </span>
                  </button>
                )
              })}
            </div>

            {/* Objection status summary */}
            {justification.objection_responses && justification.objection_responses.length > 0 && (
              <div>
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Objection Status</h4>
                <div className="space-y-1">
                  {justification.objection_responses.map((o, i) => (
                    <div key={i} className="flex items-center gap-2 p-2 bg-slate-900 rounded-lg">
                      <span className={clsx(
                        'w-1.5 h-1.5 rounded-full flex-shrink-0',
                        o.status === 'addressed' ? 'bg-green-400' :
                        o.status === 'needs_follow_up' ? 'bg-yellow-400' : 'bg-red-400'
                      )} />
                      <p className="text-[11px] text-slate-300 flex-1 truncate">{o.objection}</p>
                      <span className={clsx(
                        'text-[10px]',
                        o.status === 'addressed' ? 'text-green-400' :
                        o.status === 'needs_follow_up' ? 'text-yellow-400' : 'text-red-400'
                      )}>
                        {o.status.replace('_', ' ')}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* ROI tab */}
        {activeTab === 'roi' && (
          justification.roi_model
            ? <ROIModel roi={justification.roi_model} />
            : <EmptySection title="ROI Model" message="Build the justification to generate the ROI model with conservative, base, and optimistic scenarios." />
        )}

        {/* Exec Summary tab */}
        {activeTab === 'exec' && (
          <div>
            {justification.exec_summary ? (
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-semibold text-slate-100">Executive Summary</h3>
                  {!editingExec ? (
                    <button
                      onClick={() => { setEditingExec(true); setExecDraft(justification.exec_summary || '') }}
                      className="flex items-center gap-1.5 text-xs text-slate-400 hover:text-slate-200"
                    >
                      <Edit3 size={12} /> Edit
                    </button>
                  ) : (
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => { onUpdate({ exec_summary: execDraft }); setEditingExec(false) }}
                        className="flex items-center gap-1.5 text-xs text-green-400 hover:text-green-300"
                      >
                        <Save size={12} /> Save
                      </button>
                      <button onClick={() => setEditingExec(false)} className="text-slate-500 hover:text-slate-300">
                        <X size={14} />
                      </button>
                    </div>
                  )}
                </div>
                {editingExec ? (
                  <textarea
                    className="input w-full h-96 resize-none text-xs font-mono"
                    value={execDraft}
                    onChange={(e) => setExecDraft(e.target.value)}
                  />
                ) : (
                  <div className="bg-slate-900 rounded-xl p-5">
                    <MarkdownRenderer text={justification.exec_summary} />
                  </div>
                )}
              </div>
            ) : (
              <EmptySection title="Executive Summary" message="Build the justification to generate a C-suite-ready executive summary." />
            )}
          </div>
        )}

        {/* Procurement tab */}
        {activeTab === 'procurement' && (
          <div>
            {justification.procurement_doc ? (
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-sm font-semibold text-slate-100">Procurement Document</h3>
                  {!editingProcurement ? (
                    <button
                      onClick={() => { setEditingProcurement(true); setProcDraft(justification.procurement_doc || '') }}
                      className="flex items-center gap-1.5 text-xs text-slate-400 hover:text-slate-200"
                    >
                      <Edit3 size={12} /> Edit
                    </button>
                  ) : (
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => { onUpdate({ procurement_doc: procDraft }); setEditingProcurement(false) }}
                        className="flex items-center gap-1.5 text-xs text-green-400 hover:text-green-300"
                      >
                        <Save size={12} /> Save
                      </button>
                      <button onClick={() => setEditingProcurement(false)} className="text-slate-500 hover:text-slate-300">
                        <X size={14} />
                      </button>
                    </div>
                  )}
                </div>
                {editingProcurement ? (
                  <textarea
                    className="input w-full h-96 resize-none text-xs font-mono"
                    value={procDraft}
                    onChange={(e) => setProcDraft(e.target.value)}
                  />
                ) : (
                  <div className="bg-slate-900 rounded-xl p-5">
                    <MarkdownRenderer text={justification.procurement_doc} />
                  </div>
                )}
              </div>
            ) : (
              <EmptySection title="Procurement Document" message="Build the justification to generate a procurement readiness document with security, compliance, and vendor due diligence." />
            )}
          </div>
        )}

        {/* Objections tab */}
        {activeTab === 'objections' && (
          <div>
            <h3 className="text-sm font-semibold text-slate-100 mb-4">Objection Responses</h3>
            <ObjectionHandler
              objections={justification.objection_responses || []}
              onUpdate={(updated) => onUpdate({ objection_responses: updated })}
            />
          </div>
        )}
      </div>
    </div>
  )
}

function EmptySection({ title, message }: { title: string; message: string }) {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <div className="w-10 h-10 bg-slate-800 rounded-full flex items-center justify-center mb-3">
        <FileText size={18} className="text-slate-500" />
      </div>
      <p className="text-sm font-medium text-slate-300 mb-1">{title} Not Built</p>
      <p className="text-[12px] text-slate-500 max-w-xs">{message}</p>
    </div>
  )
}
