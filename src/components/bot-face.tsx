/**
 * Dot-matrix bot face: a round LED-style display where each bot gets its own
 * deterministic lit-dot pattern (derived from the slug + optional hue from
 * the source listing). Two SVG paths total - the dim grid and the lit dots -
 * so hundreds of cards stay lightweight. Eyes blink via the shared bot-blink
 * keyframe; the whole face glances on card hover.
 */
function hashString(s: string): number {
  let h = 7;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
  return Math.abs(h);
}

const GRID = 5; // 5x5 dot matrix
const RADIUS = 1.7;
const STEP = 7.6;
const ORIGIN = 4.2;

function dotPath(cols: number[][]): string {
  let d = "";
  for (const [cx, cy] of cols) {
    d += `M ${cx - RADIUS} ${cy} a ${RADIUS} ${RADIUS} 0 1 0 ${RADIUS * 2} 0 a ${RADIUS} ${RADIUS} 0 1 0 -${RADIUS * 2} 0 `;
  }
  return d;
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

  // grid center positions, clipped to the round display
  const centers: [number, number][] = [];
  for (let r = 0; r < GRID; r++) {
    for (let c = 0; c < GRID; c++) {
      const cx = ORIGIN + c * STEP;
      const cy = ORIGIN + r * STEP;
      const dx = cx - 20;
      const dy = cy - 20;
      if (dx * dx + dy * dy <= 15.5 * 15.5) centers.push([cx, cy]);
    }
  }

  // lit dots: two eye columns + a deterministic per-bot scatter
  const eyeDots: [number, number][] = [];
  const litDots: [number, number][] = [];
  const on = new Set<string>();
  for (const [cx, cy] of centers) {
    const isEye = (Math.abs(cx - 13.5) < 0.1 || Math.abs(cx - 26.5) < 0.1) && cy <= 18 && cy >= 12;
    if (isEye) {
      eyeDots.push([cx, cy]);
      on.add(`${cx},${cy}`);
    }
  }
  const extra = (h % 7) + 3;
  for (let i = 0; i < extra; i++) {
    const cx = ORIGIN + ((h >> (i * 2)) % GRID) * STEP;
    const cy = ORIGIN + ((h >> (i * 3 + 1)) % GRID) * STEP;
    const dx = cx - 20;
    const dy = cy - 20;
    if (dx * dx + dy * dy > 15.5 * 15.5) continue;
    if (on.has(`${cx},${cy}`)) continue;
    on.add(`${cx},${cy}`);
    litDots.push([cx, cy]);
  }

  const gridPath = dotPath(centers);
  const litPath = dotPath(litDots);
  const eyePath = dotPath(eyeDots);
  const tint = `hsl(${hue} 30% 62%)`;

  return (
    <svg width={size} height={size} viewBox="0 0 40 40" className="bot-face block shrink-0" role="img" aria-label={`${name} bot face`}>
      <defs>
        <radialGradient id={`${gid}-shine`} cx="0.3" cy="0.15" r="1">
          <stop offset="0%" stopColor="#fff" stopOpacity="0.16" />
          <stop offset="55%" stopColor="#fff" stopOpacity="0.03" />
          <stop offset="70%" stopColor="#fff" stopOpacity="0" />
        </radialGradient>
        <clipPath id={`${gid}-clip`}>
          <circle cx="20" cy="20" r="17.4" />
        </clipPath>
      </defs>
      {/* display bezel */}
      <circle cx="20" cy="20" r="17.4" fill={`hsl(${hue} 12% 9%)`} stroke={`hsl(${hue} 12% 22%)`} strokeWidth="1" />
      <g clipPath={`url(#${gid}-clip)`}>
        <circle cx="20" cy="20" r="17.4" fill={`url(#${gid}-shine)`} />
        {/* unlit grid */}
        <path d={gridPath} fill={`hsl(${hue} 10% 26%)`} opacity="0.55" />
        {/* lit identity dots */}
        <path d={litPath} fill={tint} opacity="0.85" />
        {/* eyes */}
        <path d={eyePath} className="bot-eye" style={{ "--bd": dur, "--bdel": del } as React.CSSProperties} fill="#ffffff" />
      </g>
    </svg>
  );
}
