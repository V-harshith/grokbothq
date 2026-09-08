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

export function RotatingAdSlot() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (UNITS.length < 2) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const id = window.setInterval(() => setIndex((i) => (i + 1) % UNITS.length), 7000);
    return () => window.clearInterval(id);
  }, []);

  if (UNITS.length === 0) {
    return (
      <aside className="ad-slot" aria-label="Get featured">
        <TrackedLink href="/featured" event="sponsor-slot-open" className="ad-card ad-card-open">
          <span className="ad-label">Sponsored</span>
          <span className="ad-title">This slot is open</span>
          <span className="ad-desc">Reach people at the moment they pick their next tool.</span>
          <span className="ad-cta">Get featured →</span>
        </TrackedLink>
        <p className="ad-via">ads via GrokBot HQ</p>
      </aside>
    );
  }

  const unit = UNITS[index % UNITS.length];

  return (
    <aside className="ad-slot" aria-label="Sponsored">
      <TrackedLink
        key={unit.url}
        href={sponsorHref(unit.url)}
        external
        event="sponsor-click"
        data={{ placement: "rotating" }}
        className="ad-card"
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
