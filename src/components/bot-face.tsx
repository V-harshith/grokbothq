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
  void slug;
  void hueProp;
  const initial = name.trim().charAt(0).toUpperCase() || "G";

  return (
    <svg width={size} height={size} viewBox="0 0 40 40" className="block shrink-0" role="img" aria-label={`${name} monogram`}>
      <rect x="1" y="1" width="38" height="38" rx="8" fill="var(--surface)" stroke="var(--border-c)" />
      <text x="20" y="21" textAnchor="middle" dominantBaseline="central" fontFamily="var(--font-sans), sans-serif" fontSize="18" fontWeight="500" fill="var(--foreground)">
        {initial}
      </text>
    </svg>
  );
}
