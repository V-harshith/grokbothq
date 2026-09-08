"use client";

import { useEffect, useState } from "react";
import { TrackedLink } from "./tracked-link";
import { sponsorHref } from "@/lib/ads";
import adsJson from "../../content/ads.json";

type Unit = { title: string; description: string; cta: string; url: string };

function paidUnits(): Unit[] {
  const units: Unit[] = [];
  if (adsJson.active && adsJson.title && adsJson.url && /^https?:\/\//i.test(adsJson.url)) {
    units.push({
      title: adsJson.title,
      description: adsJson.description ?? "",
      cta: adsJson.cta || "Learn more",
      url: adsJson.url,
    });
  }
  for (const s of adsJson.rails ?? []) {
    if (s.title && s.url && /^https?:\/\//i.test(s.url)) {
      units.push({
        title: s.title,
        description: s.description ?? "",
        cta: s.cta || "Learn more",
        url: s.url,
      });
    }
  }
  return units;
}

const UNITS = paidUnits();

const DEMO: Unit[] = [
  {
    title: "Your product here",
    description: "Reach people at the moment they pick their next tool.",
    cta: "Get featured",
    url: "/featured",
  },
  {
    title: "Sponsor the directory",
    description: "Developer tools, productivity apps, learning platforms - if it fits the audience, it fits.",
    cta: "See plans",
    url: "/featured",
  },
  {
    title: "Launch week slot",
    description: "The homepage slot, exclusively yours for 7 days. $99.",
    cta: "Reserve it",
    url: "/featured",
  },
];

export function RotatingAdSlot({ offset = 0 }: { offset?: number }) {
  const units = UNITS.length > 0 ? UNITS : DEMO;
  const [index, setIndex] = useState(offset % units.length);

  useEffect(() => {
    if (units.length < 2) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const id = window.setInterval(() => setIndex((i) => (i + 1) % units.length), 7000);
    return () => window.clearInterval(id);
  }, [units.length]);

  const unit = units[index % units.length];

  return (
    <aside className="ad-slot" aria-label="Sponsored">
      <TrackedLink
        key={unit.url + unit.title}
        href={sponsorHref(unit.url)}
        external={/^https?:\/\//i.test(unit.url)}
        event="sponsor-click"
        data={{ placement: "rotating" }}
        className="ad-card ad-card-live"
      >
        <span className="ad-label">Sponsored</span>
        <span className="ad-title">{unit.title}</span>
        {unit.description && <span className="ad-desc">{unit.description}</span>}
        <span className="ad-cta">{unit.cta} →</span>
      </TrackedLink>
      <p className="ad-via">ads via GrokBot HQ</p>
    </aside>
  );
}
