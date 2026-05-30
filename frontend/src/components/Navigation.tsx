import { Link, useLocation } from 'react-router-dom'
import { BarChart3, Briefcase, Zap } from 'lucide-react'
import clsx from 'clsx'

export default function Navigation() {
  const { pathname } = useLocation()

  return (
    <nav className="h-14 bg-slate-900 border-b border-slate-800 flex items-center px-6 gap-8 flex-shrink-0">
      {/* Logo */}
      <div className="flex items-center gap-2.5 mr-4">
        <div className="w-7 h-7 bg-indigo-500 rounded-lg flex items-center justify-center">
          <Zap size={15} className="text-white fill-white" />
        </div>
        <span className="font-semibold text-slate-100 text-sm tracking-tight">DealFlow AI</span>
      </div>

      {/* Nav Links */}
      <Link
        to="/command"
        className={clsx(
          'flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
          pathname === '/command'
            ? 'bg-slate-800 text-slate-100'
            : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
        )}
      >
        <BarChart3 size={15} />
        CRO Command
      </Link>

      <Link
        to="/workspace"
        className={clsx(
          'flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
          pathname.startsWith('/workspace')
            ? 'bg-slate-800 text-slate-100'
            : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
        )}
      >
        <Briefcase size={15} />
        Rep Workspace
      </Link>

      {/* Right side */}
      <div className="ml-auto flex items-center gap-3">
        <div className="flex items-center gap-1.5 bg-slate-800 border border-slate-700 px-3 py-1 rounded-full">
          <div className="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse" />
          <span className="text-xs text-slate-400">Agents active</span>
        </div>
        <div className="w-7 h-7 bg-indigo-600 rounded-full flex items-center justify-center text-xs font-semibold text-white">
          M
        </div>
      </div>
    </nav>
  )
}
