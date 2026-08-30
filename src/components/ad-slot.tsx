import Link from "next/link";
import { TrackedLink } from "./tracked-link";
import adsJson from "../../content/ads.json";

/**
 * The site's single ad unit, Carbon-ads style: a small, tidy card that lives
 * near the top of a page (never buried at the bottom). Callers position it;
 * this renders only the card.
 *
 * With a sponsor active in content/ads.json it renders their unit labeled
 * "Sponsored"; otherwise it renders the quiet house ad pointing at the
 * sponsor page. Managed without code.
 */
export function AdSlot() {
  if (adsJson.active && adsJson.title && adsJson.url) {
    return (
      <aside className="ad-slot" aria-label="Sponsored">
        <TrackedLink
          href={adsJson.url}
          external
          event="sponsor-click"
          data={{ placement: "compact" }}
          className="ad-card"
        >
          <span className="ad-label">{adsJson.label || "Sponsored"}</span>
          <span className="ad-title">{adsJson.title}</span>
          <span className="ad-desc">{adsJson.description}</span>
          <span className="ad-cta">{adsJson.cta || "Learn more"} →</span>
        </TrackedLink>
        <p className="ad-via">ads via GrokBot HQ</p>
      </aside>
    );
  }

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

/**
 * In-grid variant: same footprint as a bot card, highlighted with the accent
 * ring. Lives inside content grids (e.g. This week's standouts) so the sponsor
 * reads as a featured pick rather than an interruption.
 */
export function AdSlotCard() {
  if (adsJson.active && adsJson.title && adsJson.url) {
    return (
      <article className="card relative flex flex-col border-accent/50 bg-accent-soft p-5" aria-label="Sponsored">
        <span className="badge badge-accent w-fit">Sponsored</span>
        <h3 className="mt-2 text-base font-semibold">{adsJson.title}</h3>
        <p className="mt-1.5 flex-1 text-sm leading-relaxed text-muted">{adsJson.description}</p>
        <div className="mt-4 flex items-center justify-between gap-3">
          <TrackedLink href={adsJson.url} external event="sponsor-click" data={{ placement: "grid" }} className="text-xs font-semibold text-accent hover:underline">
            {adsJson.cta || "Learn more"} →
          </TrackedLink>
          <span className="font-mono text-[10px] text-muted opacity-70">ads via GrokBot HQ</span>
        </div>
      </article>
    );
  }

  return (
    <article className="card relative flex flex-col border-dashed border-accent/40 bg-accent-soft p-5" aria-label="Sponsored slot available">
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
