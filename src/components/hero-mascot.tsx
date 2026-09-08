"use client";

import { useEffect, useRef, useState } from "react";

type Pose = { x: number; y: number; tiltL: number; tiltR: number };

const REST: Pose = { x: 0, y: 0, tiltL: 0, tiltR: 0 };

export function HeroMascot({ className = "" }: { className?: string }) {
  const [pose, setPose] = useState<Pose>(REST);
  const svgRef = useRef<SVGSVGElement>(null);
  const mouse = useRef({ x: 0, y: 0, active: false });
  const busy = useRef(false);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    const onMove = (e: MouseEvent) => {
      const r = svgRef.current?.getBoundingClientRect();
      if (!r || r.width === 0) return;
      mouse.current = {
        x: (e.clientX - (r.left + r.width / 2)) / r.width,
        y: (e.clientY - (r.top + r.height / 2)) / r.height,
        active: true,
      };
    };
    window.addEventListener("mousemove", onMove, { passive: true });

    const glanceUp = () => {
      if (busy.current) return;
      busy.current = true;
      setPose({ x: 0, y: -14, tiltL: -10, tiltR: 12 });
      window.setTimeout(() => {
        setPose(REST);
        busy.current = false;
      }, 1400);
    };

    const follow = () => {
      if (busy.current || !mouse.current.active) return;
      busy.current = true;
      const start = Date.now();
      const tick = () => {
        const m = mouse.current;
        setPose({
          x: Math.max(-10, Math.min(10, m.x * 22)),
          y: Math.max(-8, Math.min(10, m.y * 18)),
          tiltL: 0,
          tiltR: 0,
        });
        if (Date.now() - start < 2600) {
          requestAnimationFrame(tick);
        } else {
          setPose(REST);
          busy.current = false;
        }
      };
      tick();
    };

    const initial = window.setTimeout(glanceUp, 2500);
    const glanceTimer = window.setInterval(glanceUp, 11000);
    const followTimer = window.setInterval(follow, 7000);
    return () => {
      window.removeEventListener("mousemove", onMove);
      window.clearTimeout(initial);
      window.clearInterval(glanceTimer);
      window.clearInterval(followTimer);
    };
  }, []);

  const poseStyle = (tilt: number): React.CSSProperties => ({
    transform: `translate(${pose.x}px, ${pose.y}px) rotate(${tilt}deg)`,
    transformBox: "fill-box",
    transformOrigin: "center",
  });

  return (
    <svg ref={svgRef} viewBox="0 0 320 320" fill="none" className={className} role="img" aria-label="GrokBot HQ mascot">
      <ellipse cx="160" cy="284" rx="78" ry="10" fill="#141416" />
      <circle cx="160" cy="165" r="105" fill="#0b0b0d" stroke="#2e2e34" strokeWidth="2" />
      <g transform="rotate(-8 136 151)">
        <g className="mascot-pose" style={poseStyle(pose.tiltL)}>
          <rect className="mascot-eye" x="118" y="118" width="36" height="66" rx="18" fill="#f5f5f5" />
        </g>
      </g>
      <g transform="rotate(9 192 142)">
        <g className="mascot-pose" style={poseStyle(pose.tiltR)}>
          <rect className="mascot-eye mascot-eye-late" x="176" y="112" width="32" height="60" rx="16" fill="#f5f5f5" />
        </g>
      </g>
    </svg>
  );
}
