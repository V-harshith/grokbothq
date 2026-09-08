import Link from "next/link";
import { TrackedLink } from "./tracked-link";
import { sponsorHref, sponsorId } from "@/lib/ads";
import adsJson from "../../content/ads.json";

/**
 * In-grid variant: same footprint as a bot card, highlighted with the accent
 * ring. Lives inside content grids (e.g. This week's standouts) so the sponsor
 * reads as a featured pick rather than an interruption.
 */
export function AdSlotCard() {
  if (adsJson.active && adsJson.title && adsJson.url) {
    return (
      <article className="card ad-surface relative flex flex-col p-5" aria-label="Sponsored">
        <span className="badge badge-accent w-fit">Sponsored</span>
        <h3 className="mt-2 text-base font-semibold">{adsJson.title}</h3>
        <p className="mt-1.5 flex-1 text-sm leading-relaxed text-muted">{adsJson.description}</p>
        <div className="mt-4 flex items-center justify-between gap-3">
          <TrackedLink href={sponsorHref(adsJson.url)} external event="sponsor-click" data={{ placement: "grid", sponsor: sponsorId(adsJson.url) }} className="text-xs font-semibold text-accent hover:underline">
            {adsJson.cta || "Learn more"} →
          </TrackedLink>
          <span className="font-mono text-[10px] text-muted opacity-70">ads via GrokBot HQ</span>
        </div>
      </article>
    );
  }

  return (
    <article className="card ad-surface relative flex flex-col border-dashed p-5" aria-label="Sponsored slot available">
      <span className="badge badge-accent w-fit">Sponsored</span>
      <h3 className="mt-2 text-base font-semibold">Your product here</h3>
      <p className="mt-1.5 flex-1 text-sm leading-relaxed text-muted">
        This slot sits inside the listings people are browsing right now. Any product that fits the audience.
      </p>
      <div className="mt-4 flex items-center justify-between gap-3">
        <Link href="/featured" className="text-xs font-semibold text-accent hover:underline">
          Reserve it →
        </Link>
        <span className="font-mono text-[10px] text-muted opacity-70">ads via GrokBot HQ</span>
      </div>
    </article>
  );
}
