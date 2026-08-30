import Link from "next/link";
import adsJson from "../../content/ads.json";

/**
 * The site's single ad slot. When a sponsor is active in content/ads.json it
 * renders their card (labeled "Sponsored"); otherwise it renders the quiet
 * house ad pointing at the Get featured page. Managed without code - edit
 * content/ads.json (or let the agent do it via a management task).
 */
export function AdSlot() {
  if (adsJson.active && adsJson.title && adsJson.url) {
    return (
      <aside className="container-x my-10" aria-label="Sponsored">
        <a
          href={adsJson.url}
          target="_blank"
          rel="noopener noreferrer sponsored"
          className="card card-hover flex flex-col gap-2 p-5 md:flex-row md:items-center md:justify-between md:gap-6"
        >
          <div className="min-w-0">
            <p className="text-[11px] font-semibold uppercase tracking-widest text-muted">{adsJson.label}</p>
            <p className="mt-1 font-semibold">{adsJson.title}</p>
            <p className="text-sm leading-relaxed text-muted">{adsJson.description}</p>
          </div>
          <span className="btn btn-ghost shrink-0 self-start md:self-center">{adsJson.cta}</span>
        </a>
      </aside>
    );
  }

  return (
    <aside className="container-x my-10" aria-label="Get featured">
      <Link
        href="/featured"
        className="group flex flex-wrap items-center justify-between gap-3 rounded-xl border border-dashed border-border px-5 py-4 transition-colors hover:border-accent"
      >
        <p className="text-sm text-muted">
          <span className="font-medium text-foreground">This slot is open.</span> Put your product here for launch
          week.
        </p>
        <span className="text-xs font-semibold text-accent group-hover:underline">Get featured →</span>
      </Link>
    </aside>
  );
}
