/**
 * Quiet dot-matrix divider: a strip of dim dots with one traveling highlight.
 * Pure SVG + one keyframe + per-dot delays (no JS), reduced-motion aware.
 */
export function DotDivider({ count = 64 }: { count?: number }) {
  return (
    <div className="dot-divider" aria-hidden>
      <svg width="100%" height="12" viewBox={`0 0 ${count * 16} 12`} preserveAspectRatio="xMidYMid meet">
        {Array.from({ length: count }, (_, i) => (
          <circle
            key={i}
            cx={i * 16 + 8}
            cy={6}
            r={2}
            fill="currentColor"
            style={{ animationDelay: `${(i * 0.075).toFixed(2)}s` }}
          />
        ))}
      </svg>
    </div>
  );
}
