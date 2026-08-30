import Link from "next/link";
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
        <a
          href={adsJson.url}
          target="_blank"
          rel="noopener noreferrer sponsored"
          className="ad-card"
        >
          <span className="ad-label">{adsJson.label || "Sponsored"}</span>
          <span className="ad-title">{adsJson.title}</span>
          <span className="ad-desc">{adsJson.description}</span>
          <span className="ad-cta">{adsJson.cta || "Learn more"} →</span>
        </a>
        <p className="ad-via">ads via GrokBot HQ</p>
      </aside>
    );
  }

  return (
    <aside className="ad-slot" aria-label="Get featured">
      <Link href="/featured" className="ad-card ad-card-open">
        <span className="ad-label">Sponsored</span>
        <span className="ad-title">This slot is open</span>
        <span className="ad-desc">Reach people at the moment they pick their next tool.</span>
        <span className="ad-cta">Get featured →</span>
      </Link>
      <p className="ad-via">ads via GrokBot HQ</p>
    </aside>
  );
}
