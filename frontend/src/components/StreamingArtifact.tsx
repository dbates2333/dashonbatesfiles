import { useEffect, useRef } from 'react'
import { Loader2, CheckCircle2, AlertCircle } from 'lucide-react'
import type { StreamChunk } from '../types'
import clsx from 'clsx'

interface Props {
  chunks: StreamChunk[]
  isStreaming: boolean
  error?: string | null
}

const SECTION_LABELS: Record<string, string> = {
  roi_model: 'ROI Model',
  exec_summary: 'Executive Summary',
  procurement_doc: 'Procurement Document',
  objections: 'Objection Responses'
}

const TOOL_LABELS: Record<string, string> = {
  build_roi_model: 'Building ROI Model with 3 scenarios...',
  write_exec_summary: 'Writing executive summary...',
  create_procurement_doc: 'Creating procurement document...',
  generate_objection_responses: 'Generating objection responses...'
}

export default function StreamingArtifact({ chunks, isStreaming, error }: Props) {
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [chunks.length])

  const completedSections = chunks
    .filter((c) => c.type === 'section_complete')
    .map((c) => c.section as string)

  const currentTool = chunks
    .filter((c) => c.type === 'tool_progress')
    .at(-1)?.tool

  return (
    <div className="bg-slate-900 rounded-xl p-4 space-y-3">
      <div className="flex items-center gap-2 mb-3">
        {isStreaming ? (
          <>
            <Loader2 size={14} className="text-indigo-400 animate-spin" />
            <span className="text-sm font-medium text-indigo-400">Agent building justification...</span>
          </>
        ) : error ? (
          <>
            <AlertCircle size={14} className="text-red-400" />
            <span className="text-sm font-medium text-red-400">Build failed</span>
          </>
        ) : (
          <>
            <CheckCircle2 size={14} className="text-green-400" />
            <span className="text-sm font-medium text-green-400">Build complete</span>
          </>
        )}
      </div>

      {/* Section progress */}
      {['roi_model', 'exec_summary', 'procurement_doc', 'objections'].map((section) => {
        const isComplete = completedSections.includes(section)
        const isCurrent = isStreaming &&
          currentTool === Object.entries(TOOL_LABELS).find(([k]) => {
            const map: Record<string, string> = {
              'build_roi_model': 'roi_model',
              'write_exec_summary': 'exec_summary',
              'create_procurement_doc': 'procurement_doc',
              'generate_objection_responses': 'objections'
            }
            return map[k] === section
          })?.[0]

        return (
          <div key={section} className={clsx(
            'flex items-center gap-3 p-2.5 rounded-lg transition-all',
            isComplete ? 'bg-green-400/5 border border-green-400/15' :
            isCurrent ? 'bg-indigo-500/10 border border-indigo-500/20' :
            'bg-slate-800/60 border border-transparent'
          )}>
            {isComplete ? (
              <CheckCircle2 size={14} className="text-green-400 flex-shrink-0" />
            ) : isCurrent ? (
              <Loader2 size={14} className="text-indigo-400 animate-spin flex-shrink-0" />
            ) : (
              <div className="w-3.5 h-3.5 rounded-full border-2 border-slate-600 flex-shrink-0" />
            )}
            <span className={clsx(
              'text-sm',
              isComplete ? 'text-green-300' :
              isCurrent ? 'text-indigo-300' :
              'text-slate-500'
            )}>
              {SECTION_LABELS[section]}
            </span>
            {isCurrent && (
              <span className="text-[11px] text-indigo-400 ml-auto agent-pulse">
                {TOOL_LABELS[currentTool || ''] || 'Working...'}
              </span>
            )}
            {isComplete && (
              <span className="text-[10px] text-green-400 ml-auto">Done</span>
            )}
          </div>
        )
      })}

      {/* Error message */}
      {error && (
        <div className="flex items-start gap-2 bg-red-400/5 border border-red-400/15 rounded-lg p-3">
          <AlertCircle size={13} className="text-red-400 flex-shrink-0 mt-0.5" />
          <p className="text-[12px] text-red-300">{error}</p>
        </div>
      )}

      {/* Live log */}
      <div className="mt-2 space-y-1 max-h-32 overflow-y-auto">
        {chunks.filter((c) => c.type === 'tool_progress').map((c, i) => (
          <div key={i} className="flex items-center gap-2">
            <div className="w-1 h-1 bg-indigo-400 rounded-full flex-shrink-0" />
            <span className="text-[10px] text-slate-400">
              {TOOL_LABELS[c.tool || ''] || c.message || c.tool}
            </span>
          </div>
        ))}
      </div>

      <div ref={bottomRef} />
    </div>
  )
}
