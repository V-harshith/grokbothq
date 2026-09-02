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

export function BotFace({
  slug,
  name,
  size = 40,
  hue: hueProp,
}: {
  slug: string;
  name: string;
  size?: number;
  hue?: number;
}) {
  const h = hashString(slug);
  const hue = hueProp ?? h % 360;
  const dur = `${(3.6 + (h % 320) / 100).toFixed(2)}s`;
  const del = `${((h % 280) / 100).toFixed(2)}s`;
  const gid = `bf-${slug}`;

  return (
    <svg width={size} height={size} viewBox="0 0 40 40" className="bot-face block shrink-0 transition-transform duration-300" role="img" aria-label={`${name} bot face`}>
      <defs>
        <clipPath id={`${gid}-clip`}><circle cx="20" cy="20" r="16" /></clipPath>
        <linearGradient id={`${gid}-fill`} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor={`hsl(${hue} 28% 42%)`} />
          <stop offset="100%" stopColor={`hsl(${(hue + 40) % 360} 30% 22%)`} />
        </linearGradient>
        <radialGradient id={`${gid}-shine`} cx="0.28" cy="0.14" r="0.9">
          <stop offset="0%" stopColor="#fff" stopOpacity="0.4" />
          <stop offset="42%" stopColor="#fff" stopOpacity="0.06" />
          <stop offset="55%" stopColor="#fff" stopOpacity="0" />
        </radialGradient>
      </defs>
      <circle cx="20" cy="20" r="16" fill={`hsl(${hue} 15% 11%)`} />
      <circle cx="20" cy="20" r="16" fill={`url(#${gid}-fill)`} opacity="0.9" />
      <circle cx="20" cy="20" r="16" fill={`url(#${gid}-shine)`} />
      <g>
        <rect className="bot-eye" style={{ "--bd": dur, "--bdel": del } as React.CSSProperties} x="12" y="13.6" width="5.2" height="12.8" rx="2.6" fill="#fff" />
        <rect className="bot-eye" style={{ "--bd": dur, "--bdel": del } as React.CSSProperties} x="22.8" y="13.6" width="5.2" height="12.8" rx="2.6" fill="#fff" />
      </g>
    </svg>
  );
}
