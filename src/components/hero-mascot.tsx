export function HeroMascot({ className = "" }: { className?: string }) {
  return (
    <svg viewBox="0 0 320 300" fill="none" className={className} role="img" aria-label="GrokBot HQ mascot">
      <ellipse cx="160" cy="274" rx="72" ry="10" fill="#1f1f1f" />
      <line x1="160" y1="52" x2="160" y2="30" stroke="#6e6e73" strokeWidth="5" strokeLinecap="round" />
      <circle cx="160" cy="22" r="7" fill="#f5f5f5" />
      <polygon points="78,96 128,58 192,58 242,96 232,196 188,244 132,244 88,196" fill="#161617" stroke="#3d3d3d" strokeWidth="2" strokeLinejoin="round" />
      <polygon points="78,96 116,96 104,180 88,196" fill="#e9e9ec" />
      <polygon points="204,96 242,96 232,196 216,180" fill="#55555a" />
      <polygon points="116,96 204,96 216,180 190,224 130,224 104,180" fill="#232326" />
      <polygon points="130,224 190,224 178,244 142,244" fill="#2c2c30" />
      <polygon points="126,138 158,133 156,157 124,161" fill="#050505" stroke="#55555a" strokeWidth="1.5" strokeLinejoin="round" />
      <polygon points="162,133 194,138 196,161 164,157" fill="#050505" stroke="#55555a" strokeWidth="1.5" strokeLinejoin="round" />
      <line x1="112" y1="190" x2="132" y2="188" stroke="#55555a" strokeWidth="3" strokeLinecap="round" />
      <line x1="112" y1="200" x2="130" y2="199" stroke="#55555a" strokeWidth="3" strokeLinecap="round" />
      <line x1="188" y1="188" x2="208" y2="190" stroke="#55555a" strokeWidth="3" strokeLinecap="round" />
      <line x1="190" y1="199" x2="208" y2="200" stroke="#55555a" strokeWidth="3" strokeLinecap="round" />
      <polygon points="147,197 173,197 169,207 151,207" fill="#050505" stroke="#55555a" strokeWidth="1.5" strokeLinejoin="round" />
    </svg>
  );
}
