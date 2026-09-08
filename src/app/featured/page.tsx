import type { Metadata } from "next";
import Link from "next/link";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { pageMetadata, breadcrumbsJsonLd } from "@/lib/seo";
import { SITE } from "@/data/site";
import { EmailLink } from "@/components/email-link";
import { bots } from "@/data/bots";
import metricsJson from "../../../content/metrics.json";

export const metadata: Metadata = pageMetadata({
  title: "Sponsor GrokBot HQ - Reach People Choosing Their Next Tool",
  description:
    "Sponsor the top slots on GrokBot HQ. Not just bots: any product that fits people actively exploring Grok. Always labeled, one sponsor per slot. Contact us to reserve.",
  path: "/featured",
  keywords: ["sponsor grokbot hq", "advertise to grok users", "grok bot directory sponsorship"],
});

const slots = [
  {
    name: "Homepage",
    detail: "A rotating cell inside the Most installed grid plus a closing slot after the guides.",
    subject: "Homepage sponsorship",
  },
  {
    name: "Directory",
    detail: "Compact slot beside the /bots header and in-grid cards on category and New pages.",
    subject: "Directory sponsorship",
  },
  {
    name: "Detail pages",
    detail: "Inside all 700+ bot pages and every guide, beside the content being read.",
    subject: "Detail page sponsorship",
  },
  {
    name: "Desktop rails",
    detail: "Fixed gutter cards on very wide screens, visible across the whole site.",
    subject: "Rail sponsorship",
  },
];

export default function FeaturedPage() {
  const m = metricsJson as unknown as { sponsorClicks?: number; sponsors?: Record<string, number> };const sponsorClicks = typeof m.sponsorClicks === "number" ? m.sponsorClicks : 0;
  const sponsorRows = Object.entries(m.sponsors ?? {}).sort((a, b) => b[1] - a[1]).slice(0, 8);
  return (
    <div className="container-x max-w-5xl py-12">
      <JsonLd data={[breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Sponsor", path: "/featured" }])]} />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Sponsor" }]} />
      <SectionHeader
        kicker="Sponsorship"
        title="Be there at the moment of choice"
        description="People browsing this site are actively picking a bot to open. If your product helps them work smarter, a slot here puts you inside that decision. Sponsors are not limited to bots: developer tools, productivity apps, learning platforms - if it fits the audience, it fits."
      />

      <div className="grid gap-4 sm:grid-cols-2">
        {slots.map((slot) => (
          <article key={slot.name} className="card flex flex-col p-6">
            <h2 className="text-lg font-semibold">{slot.name}</h2>
            <p className="mt-2 flex-1 text-sm leading-relaxed text-muted">{slot.detail}</p>
            <EmailLink subject={slot.subject} className="btn btn-ghost mt-5">
              Contact to reserve
            </EmailLink>
          </article>
        ))}
      </div>

      {/* Visibility proof */}
      <section className="mt-14">
        <SectionHeader
          kicker="Visibility"
          title="Where your slot appears - and how it's measured"
          description="Sponsors don't buy a mention, they buy placement. Here is the exact map of where the unit renders, and the numbers that prove it."
        />
        <div className="grid gap-4 md:grid-cols-3">
          {[
            { page: "Homepage", where: "In the Most installed grid and page end", detail: "Beside the top picks, plus a closing slot after the guides" },
            { page: "Directory", where: "Compact slot beside the /bots header", detail: "Beside the filters every browser uses" },
            { page: "Category & New pages", where: "Pinned inside the listings", detail: "Among the cards people are actively picking from" },
          ].map((s) => (
            <div key={s.page} className="card p-5">
              <p className="font-mono text-[10px] uppercase tracking-[0.14em] text-accent">{s.page}</p>
              <p className="mt-2 text-sm font-semibold">{s.where}</p>
              <p className="mt-1 text-sm leading-relaxed text-muted">{s.detail}</p>
            </div>
          ))}
        </div>

        <div className="card mt-4 grid gap-4 p-6 sm:grid-cols-3">
          <div>
            <p className="tnum font-mono text-2xl font-semibold text-accent">{bots.length}</p>
            <p className="text-xs text-muted">listing pages your unit rotates across</p>
          </div>
          <div>
            <p className="tnum font-mono text-2xl font-semibold text-accent">7</p>
            <p className="text-xs text-muted">surfaces carry the sponsored unit (home, directory, categories, new, detail pages, guides, rails)</p>
          </div>
          <div>
            <p className="tnum font-mono text-2xl font-semibold text-accent">
              {sponsorClicks > 0 ? sponsorClicks : "live"}
            </p>
            <p className="text-xs text-muted">
              {sponsorClicks > 0
                ? "sponsor-unit clicks tracked in the last 30 days"
                : "click measurement once analytics are connected - every sponsor gets their count at the end of the run"}
            </p>
          </div>
        </div>
        {sponsorRows.length > 0 && (
          <ul className="mt-4 space-y-1.5">
            {sponsorRows.map(([id, count]) => (
              <li key={id} className="flex items-baseline justify-between gap-4 border-b border-border pb-1.5 text-sm">
                <span className="font-mono text-xs text-muted">{id}</span>
                <span className="tnum font-mono text-sm font-semibold">{count} clicks</span>
              </li>
            ))}
          </ul>
        )}
        <p className="mt-3 text-xs text-muted">
          Measurement is cookieless (Umami). Clicks on your unit are counted per placement and reported at the end of
          the run. No personal data, ever.
        </p>
      </section>

      <section className="card mt-10 p-6 md:p-8">
        <h2 className="text-lg font-semibold">The rules, up front</h2>
        <ul className="mt-3 space-y-2 text-sm leading-relaxed text-muted">
          <li>Every sponsor passes the same hand review as organic listings. If it would embarrass the page it sits on, we decline it.</li>
          <li>Sponsorships are always labeled. The directory’s only asset is trust; we do not sell it quietly.</li>
          <li>One sponsor per slot at a time. No bidding wars, no bait-and-switch.</li>
          <li>Organic listings never lose position to sponsors. Featured slots are additive.</li>
          <li>You’ll get a confirmation screenshot of your placement the day it goes live.</li>
        </ul>
        <p className="mt-4 text-sm text-muted">
          Want to see the slots first? <Link href="/bots" className="text-accent hover:underline">Browse the directory</Link>, or
          email <EmailLink className="text-accent hover:underline">{SITE.email}</EmailLink> with what you’d like to run.
        </p>
      </section>
    </div>
  );
}
