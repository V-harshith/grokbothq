export function HeroMascot({ className = "" }: { className?: string }) {
  return (
    <svg viewBox="0 0 320 320" fill="none" className={className} role="img" aria-label="GrokBot HQ mascot">
      <ellipse cx="160" cy="284" rx="78" ry="10" fill="#141416" />
      <circle cx="160" cy="165" r="105" fill="#0b0b0d" stroke="#2e2e34" strokeWidth="2" />
      <g transform="rotate(-8 136 151)">
        <rect className="mascot-eye" x="118" y="118" width="36" height="66" rx="18" fill="#f5f5f5" />
      </g>
      <g transform="rotate(9 192 142)">
        <rect className="mascot-eye mascot-eye-late" x="176" y="112" width="32" height="60" rx="16" fill="#f5f5f5" />
      </g>
    </svg>
  );
}
