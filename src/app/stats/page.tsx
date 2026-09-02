import type { Metadata } from "next";
import Link from "next/link";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { siteStats } from "@/lib/site-stats";
import { pageMetadata, breadcrumbsJsonLd, absUrl } from "@/lib/seo";
import { SITE } from "@/data/site";

export const metadata: Metadata = pageMetadata({
  title: "State of Grok Bots - Original Directory Statistics",
  description:
    "Original data from the GrokBot HQ directory: how many Grok bots exist, category distribution, builder counts, install numbers, and weekly growth - updated daily, citable under CC BY.",
  path: "/stats",
});

function MeasureBar({ count, max }: { count: number; max: number }) {
  const pct = Math.max(4, Math.round((count / Math.max(max, 1)) * 100));
  return (
    <div className="h-1.5 w-full rounded-full bg-elevated" role="presentation">
      <div className="h-full rounded-full bg-accent transition-[width] duration-700" style={{ width: `${pct}%` }} />
    </div>
  );
}

export default function StatsPage() {
  const s = siteStats();
  const maxCategory = Math.max(...s.perCategory.map((c) => c.count));
  const maxWeek = Math.max(...s.weeks.map((w) => w.count), 1);
  const maxIntegration = Math.max(...s.integrations.map((i) => i.count), 1);

  const dataset = {
    "@context": "https://schema.org",
    "@type": "Dataset",
    name: "State of Grok Bots - GrokBot HQ directory statistics",
    description: `Daily-computed statistics of the GrokBot HQ directory: ${s.totals.bots} hand-reviewed Grok bots by ${s.totals.builders} builders across ${s.totals.categories} categories, with install counts and weekly growth.`,
    url: absUrl("/stats"),
    dateModified: SITE.lastUpdated,
    creator: { "@type": "Organization", name: SITE.name, url: SITE.url },
    license: "https://creativecommons.org/licenses/by/4.0/",
    keywords: ["Grok bots", "Grok directory statistics", "xAI ecosystem"],
  };

  return (
    <div className="container-x max-w-4xl py-12">
      <JsonLd
        data={[
          dataset,
          breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "State of Grok Bots", path: "/stats" }]),
        ]}
      />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "State of Grok Bots" }]} />
      <SectionHeader
        kicker="Original data"
        title="State of Grok Bots"
        description={`Computed daily from the GrokBot HQ directory itself - every number traces back to verified listings. Last updated ${new Date(SITE.lastUpdated).toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })}.`}
      />

      {/* headline numbers */}
      <dl className="grid grid-cols-2 gap-4 md:grid-cols-4">
        {[
          { label: "bots listed", value: s.totals.bots },
          { label: "builders", value: s.totals.builders },
          { label: "categories", value: s.totals.categories },
          { label: "reported installs", value: s.totals.installs },
        ].map((n) => (
          <div key={n.label} className="card p-4 text-center">
            <dd className="tnum font-mono text-2xl font-semibold text-accent">{n.value}</dd>
            <dt className="mt-1 text-xs text-muted">{n.label}</dt>
          </div>
        ))}
      </dl>

      {/* growth */}
      <section className="mt-12" data-reveal>
        <h2 className="text-2xl font-semibold tracking-tight">Weekly additions</h2>
        <p className="mt-2 text-sm text-muted">
          {s.totals.last7} bots were added in the last 7 days; {s.totals.last30} in the last 30.
        </p>
        <div className="mt-5 flex items-end justify-between gap-2">
          {s.weeks.map((w) => (
            <div key={w.label} className="flex flex-1 flex-col items-center gap-1.5">
              <span className="tnum font-mono text-xs text-accent">{w.count}</span>
              <div className="flex w-full flex-col-reverse items-center gap-1">
                {Array.from({ length: Math.max(w.count, 1) }, (_, i) => (
                  <span key={i} className="block h-1.5 w-1.5 rounded-full bg-accent" style={{ opacity: 0.4 + (i / Math.max(w.count, 1)) * 0.6 }} />
                ))}
              </div>
              <span className="text-[10px] text-muted">{w.label}</span>
            </div>
          ))}
        </div>
      </section>


      {/* categories */}
      <section className="mt-10" data-reveal>
        <h2 className="text-2xl font-semibold tracking-tight">Bots by category</h2>
        <div className="mt-5 space-y-4">
          {s.perCategory.map((c) => (
            <div key={c.slug}>
              <div className="flex items-baseline justify-between text-sm">
                <span className="font-medium capitalize">{c.slug}</span>
                <span className="tnum font-mono text-muted">{c.count}</span>
              </div>
              <div className="text-accent">
                <MeasureBar count={c.count} max={maxCategory} />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* integrations */}
      <section className="mt-12" data-reveal>
        <h2 className="text-2xl font-semibold tracking-tight">Most connected tools</h2>
        <div className="mt-5 space-y-4">
          {s.integrations.slice(0, 6).map((i) => (
            <div key={i.slug}>
              <div className="flex items-baseline justify-between text-sm">
                <Link href={`/integrations/${i.slug}`} className="font-medium hover:text-accent">
                  {i.name}
                </Link>
                <span className="tnum font-mono text-muted">{i.count}</span>
              </div>
              <div className="text-accent">
                <MeasureBar count={i.count} max={maxIntegration} />
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* leaderboard */}
      {s.topInstalled.length > 0 && (
        <section className="mt-12" data-reveal>
          <h2 className="text-2xl font-semibold tracking-tight">Most installed bots</h2>
          <ol className="mt-5 divide-y divide-border">
            {s.topInstalled.map((b, i) => (
              <li key={b.slug} className="flex items-center justify-between gap-4 py-3">
                <span className="flex items-baseline gap-3">
                  <span className="tnum font-mono text-sm text-accent">{String(i + 1).padStart(2, "0")}</span>
                  <Link href={`/bots/${b.slug}`} className="font-medium hover:text-accent">
                    {b.name}
                  </Link>
                </span>
                <span className="tnum font-mono text-sm text-muted">{b.installs} installs</span>
              </li>
            ))}
          </ol>
        </section>
      )}

      {/* methodology */}
      <section className="card mt-14 p-6" aria-label="Methodology">
        <h2 className="text-lg font-semibold">Methodology</h2>
        <p className="mt-2 text-sm leading-relaxed text-muted">
          Every number on this page is computed at build time from the GrokBot HQ directory itself: {s.totals.bots}{" "}
          listings, each opened and tested before publication. Install counts are reported by each bot&apos;s public
          source listing where available. The data refreshes daily and is licensed{" "}
          <a href="https://creativecommons.org/licenses/by/4.0/" target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">
            CC BY 4.0
          </a>{" "}
          - cite it as <span className="font-mono text-xs">Source: GrokBot HQ ({SITE.url}/stats)</span>. Limitation: bot
          behavior depends on xAI&apos;s platform and each builder&apos;s instructions.
        </p>
      </section>
    </div>
  );
}
