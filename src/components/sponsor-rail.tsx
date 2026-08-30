import Link from "next/link";
import { TrackedLink } from "./tracked-link";
import adsJson from "../../content/ads.json";

/**
 * Desktop sponsor rail (xl+ screens, fixed in the right gutter so content is
 * never squished). Shows up to two paid cards, or the "Become a sponsor"
 * house card when the rail is unsold. Mobile/tablet never sees it - the
 * in-grid and header units carry sponsorship there.
 */
export function SponsorRail() {
  const sponsors = (adsJson.rails ?? []).filter((s) => s.title && s.url).slice(0, 2);
  const paid = adsJson.active && sponsors.length > 0;

  return (
    <aside className="fixed right-4 top-20 z-40 hidden w-44 space-y-3 2xl:block" aria-label="Partners">
      {sponsors.map((s, i) => (
        <div key={i} className="card p-4">
          <p className="font-mono text-[9px] uppercase tracking-[0.14em] text-muted">
            {paid ? "Sponsored" : "Sponsored"}
          </p>
          <p className="mt-1.5 text-sm font-semibold leading-snug">{s.title}</p>
          {s.description && <p className="mt-1 text-xs leading-relaxed text-muted">{s.description}</p>}
          <TrackedLink
            href={s.url}
            external={Boolean(s.url.startsWith("http"))}
            event="sponsor-click"
            data={{ placement: "rail" }}
            className="mt-2 inline-block text-xs font-semibold text-accent hover:underline"
          >
            {s.cta || "Learn more"} →
          </TrackedLink>
        </div>
      ))}
      <Link
        href="/featured"
        className="block rounded-xl border border-dashed border-border p-4 transition-colors hover:border-accent"
      >
        <p className="text-sm font-semibold">Become a sponsor</p>
        <p className="mt-1 text-xs leading-relaxed text-muted">
          Get your tool in front of Grok bot builders.
        </p>
      </Link>
    </aside>
  );
}
