import { Loader2, CheckCircle2, AlertCircle, Clock } from 'lucide-react'
import type { AgentStatus } from '../types'
import clsx from 'clsx'

interface Props {
  status: AgentStatus
  size?: 'sm' | 'md'
}

export default function AgentStatusBadge({ status, size = 'md' }: Props) {
  const cfg = {
    building: {
      icon: <Loader2 size={size === 'sm' ? 11 : 13} className="animate-spin" />,
      label: 'Building...',
      className: 'bg-indigo-500/15 text-indigo-400 border-indigo-500/20'
    },
    complete: {
      icon: <CheckCircle2 size={size === 'sm' ? 11 : 13} />,
      label: 'Complete',
      className: 'bg-green-400/10 text-green-400 border-green-400/20'
    },
    needs_review: {
      icon: <AlertCircle size={size === 'sm' ? 11 : 13} />,
      label: 'Needs Review',
      className: 'bg-yellow-400/10 text-yellow-400 border-yellow-400/20'
    },
    not_started: {
      icon: <Clock size={size === 'sm' ? 11 : 13} />,
      label: 'Not Started',
      className: 'bg-slate-700 text-slate-400 border-slate-600'
    }
  }

  const { icon, label, className } = cfg[status] || cfg['not_started']

  return (
    <span className={clsx(
      'inline-flex items-center gap-1 border rounded-full font-medium',
      size === 'sm' ? 'px-1.5 py-0.5 text-[10px]' : 'px-2 py-1 text-xs',
      className
    )}>
      {icon}
      {label}
    </span>
  )
}
