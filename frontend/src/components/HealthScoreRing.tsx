import clsx from 'clsx'

interface Props {
  score: number
  size?: 'sm' | 'md' | 'lg'
  showLabel?: boolean
}

export function healthColor(score: number): string {
  if (score >= 75) return '#4ade80' // green-400
  if (score >= 50) return '#facc15' // yellow-400
  return '#f87171' // red-400
}

export function healthBg(score: number): string {
  if (score >= 75) return 'bg-green-400/10 text-green-400 border-green-400/20'
  if (score >= 50) return 'bg-yellow-400/10 text-yellow-400 border-yellow-400/20'
  return 'bg-red-400/10 text-red-400 border-red-400/20'
}

export function healthLabel(score: number): string {
  if (score >= 75) return 'Healthy'
  if (score >= 50) return 'At Risk'
  return 'Exposed'
}

export default function HealthScoreRing({ score, size = 'md', showLabel = false }: Props) {
  const sizes = {
    sm: { outer: 40, stroke: 4, r: 16, fontSize: 9 },
    md: { outer: 60, stroke: 5, r: 24, fontSize: 13 },
    lg: { outer: 88, stroke: 7, r: 36, fontSize: 18 }
  }

  const cfg = sizes[size]
  const circumference = 2 * Math.PI * cfg.r
  const offset = circumference - (score / 100) * circumference
  const color = healthColor(score)

  return (
    <div className="flex flex-col items-center gap-1">
      <svg width={cfg.outer} height={cfg.outer} viewBox={`0 0 ${cfg.outer} ${cfg.outer}`}>
        {/* Track */}
        <circle
          cx={cfg.outer / 2}
          cy={cfg.outer / 2}
          r={cfg.r}
          fill="none"
          stroke="#334155"
          strokeWidth={cfg.stroke}
        />
        {/* Progress */}
        <circle
          cx={cfg.outer / 2}
          cy={cfg.outer / 2}
          r={cfg.r}
          fill="none"
          stroke={color}
          strokeWidth={cfg.stroke}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          transform={`rotate(-90 ${cfg.outer / 2} ${cfg.outer / 2})`}
          style={{ transition: 'stroke-dashoffset 1s ease-out' }}
        />
        {/* Score text */}
        <text
          x={cfg.outer / 2}
          y={cfg.outer / 2}
          textAnchor="middle"
          dominantBaseline="central"
          fill={color}
          fontSize={cfg.fontSize}
          fontWeight="700"
          fontFamily="Inter, system-ui, sans-serif"
        >
          {score.toFixed(0)}
        </text>
      </svg>
      {showLabel && (
        <span className={clsx('text-xs font-medium', score >= 75 ? 'text-green-400' : score >= 50 ? 'text-yellow-400' : 'text-red-400')}>
          {healthLabel(score)}
        </span>
      )}
    </div>
  )
}
