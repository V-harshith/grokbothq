"use client";

import { useEffect, useState } from "react";
import { TrackedLink } from "./tracked-link";
import { sponsorHref, sponsorId } from "@/lib/ads";
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
    title: "Your buyers are already here",
    description: "Bot builders browse this directory while deciding what to open next.",
    cta: "Claim this slot",
    url: "/featured",
  },
  {
    title: "Advertise without tricking anyone",
    description: "Every placement is labeled sponsored. Readers trust the directory because ads never pretend to be picks.",
    cta: "See open slots",
    url: "/featured",
  },
  {
    title: "Launching something?",
    description: "Put it where Grok bot builders are already looking.",
    cta: "Reserve your slot",
    url: "/featured",
  },
];

function activeUnits(): Unit[] {
  return UNITS.length > 0 ? UNITS : DEMO;
}

function isExternal(url: string): boolean {
  return /^https?:\/\//i.test(url);
}

function useRotation(length: number, offset: number): number {
  const [index, setIndex] = useState(offset % length);
  useEffect(() => {
    if (length < 2) return;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const id = window.setInterval(() => setIndex((i) => (i + 1) % length), 7000);
    return () => window.clearInterval(id);
  }, [length]);
  return index % length;
}

export function RotatingAdSlot({ offset = 0 }: { offset?: number }) {
  const units = activeUnits();
  const unit = units[useRotation(units.length, offset)];

  return (
    <aside className="ad-slot" aria-label="Sponsored">
      <TrackedLink
        key={unit.url + unit.title}
        href={sponsorHref(unit.url)}
        external={isExternal(unit.url)}
        event="sponsor-click"
        data={{ placement: "rotating", sponsor: sponsorId(unit.url) }}
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

export function RotatingAdSlotCard({ offset = 0 }: { offset?: number }) {
  const units = activeUnits();
  const unit = units[useRotation(units.length, offset)];

  return (
    <article className="card card-hover ad-card-live ad-surface relative flex flex-col p-5" aria-label="Sponsored">
      <span className="badge badge-accent w-fit">Sponsored</span>
      <h3 className="mt-2 text-base font-semibold">{unit.title}</h3>
      <p className="mt-1.5 flex-1 text-sm leading-relaxed text-muted">{unit.description}</p>
      <div className="mt-4 flex items-center justify-between gap-3">
        <TrackedLink
          key={unit.url + unit.title}
          href={sponsorHref(unit.url)}
          external={isExternal(unit.url)}
          event="sponsor-click"
          data={{ placement: "grid", sponsor: sponsorId(unit.url) }}
          className="text-xs font-semibold text-accent hover:underline"
        >
          {unit.cta} →
        </TrackedLink>
        <span className="font-mono text-[10px] text-muted opacity-70">ads via GrokBot HQ</span>
      </div>
    </article>
  );
}
