/**
 * Deterministic per-bot face: a glossy gradient "bot head" SVG whose hue and
 * blink rhythm are derived from the bot's slug - every bot gets its own
 * identity, rendered server-side with zero randomness and zero JS.
 */
function hashString(s: string): number {
  let h = 7;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
  return Math.abs(h);
}

export function BotFace({ slug, name, size = 40 }: { slug: string; name: string; size?: number }) {
  const h = hashString(slug);
  const hue = h % 360;
  const dur = `${(3.6 + (h % 320) / 100).toFixed(2)}s`;
  const del = `${((h % 280) / 100).toFixed(2)}s`;
  const gid = `bf-${slug}`;

  return (
    <svg width={size} height={size} viewBox="0 0 40 40" className="block shrink-0" role="img" aria-label={`${name} bot face`}>
      <defs>
        <linearGradient id={`${gid}-fill`} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor={`hsl(${hue} 72% 58%)`} />
          <stop offset="100%" stopColor={`hsl(${(hue + 40) % 360} 78% 34%)`} />
        </linearGradient>
        <radialGradient id={`${gid}-shine`} cx="0.28" cy="0.14" r="0.9">
          <stop offset="0%" stopColor="#fff" stopOpacity="0.5" />
          <stop offset="42%" stopColor="#fff" stopOpacity="0.08" />
          <stop offset="55%" stopColor="#fff" stopOpacity="0" />
        </radialGradient>
      </defs>
      <rect x="4" y="6" width="32" height="28" rx="9" fill={`hsl(${hue} 30% 12%)`} />
      <rect x="4" y="6" width="32" height="28" rx="9" fill={`url(#${gid}-fill)`} opacity="0.92" />
      <rect width="40" height="40" fill={`url(#${gid}-shine)`} />
      <g>
        <rect className="bot-eye" style={{ "--bd": dur, "--bdel": del } as React.CSSProperties} x="12.4" y="14.6" width="4.2" height="10.8" rx="2.1" fill="#fff" />
        <rect className="bot-eye" style={{ "--bd": dur, "--bdel": del } as React.CSSProperties} x="23.4" y="14.6" width="4.2" height="10.8" rx="2.1" fill="#fff" />
      </g>
    </svg>
  );
}
