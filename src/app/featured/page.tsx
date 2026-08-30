import type { Metadata } from "next";
import Link from "next/link";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { pageMetadata, breadcrumbsJsonLd } from "@/lib/seo";
import { SITE } from "@/data/site";
import { bots } from "@/data/bots";
import metricsJson from "../../../content/metrics.json";

export const metadata: Metadata = pageMetadata({
  title: "Sponsor GrokBot HQ - Reach People Choosing Their Next Tool",
  description:
    "Sponsor the top slots on GrokBot HQ. Not just bots: any product that fits people actively exploring Grok. Transparent pricing, always labeled, one sponsor per slot.",
  path: "/featured",
});

const plans = [
  {
    name: "Featured listing",
    price: "$29",
    period: "4 weeks",
    features: [
      "Pinned to the top of one category page",
      "Always labeled, so it reads as a pick, not an ad",
      "Rotates through the homepage ad slot",
      "Direct do-follow link to your site or X profile",
    ],
    subject: "Featured listing",
  },
  {
    name: "Launch week",
    price: "$99",
    period: "7 days",
    features: [
      "The homepage ad slot, exclusively yours for 7 days",
      "Top placement on the /bots directory page",
      "A pinned spot at the top of New this week",
      "Direct do-follow link",
    ],
    subject: "Launch week",
  },
  {
    name: "Category takeover",
    price: "$199",
    period: "per month",
    features: [
      "Your card pinned above every listing on one category page",
      "Homepage ad-slot rotation for the whole month",
      "One sponsor per category, never shared",
      "Direct do-follow link",
    ],
    subject: "Category takeover",
  },
];

export default function FeaturedPage() {
  const m = metricsJson as unknown as { sponsorClicks?: number };const sponsorClicks = typeof m.sponsorClicks === "number" ? m.sponsorClicks : 0;
  return (
    <div className="container-x max-w-5xl py-12">
      <JsonLd data={[breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Sponsor", path: "/featured" }])]} />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Sponsor" }]} />
      <SectionHeader
        kicker="Sponsorship"
        title="Be there at the moment of choice"
        description="People browsing this site are actively picking a bot to open. If your product helps them work smarter, a slot here puts you inside that decision. Sponsors are not limited to bots: developer tools, productivity apps, learning platforms - if it fits the audience, it fits."
      />

      <div className="grid gap-4 lg:grid-cols-3">
        {plans.map((plan) => (
          <article key={plan.name} className="card flex flex-col p-6">
            <h2 className="text-lg font-semibold">{plan.name}</h2>
            <p className="mt-2">
              <span className="font-mono text-3xl font-semibold">{plan.price}</span>{" "}
              <span className="text-xs text-muted">{plan.period}</span>
            </p>
            <ul className="mt-4 flex-1 space-y-2">
              {plan.features.map((f) => (
                <li key={f.slice(0, 24)} className="flex items-start gap-2 text-sm leading-relaxed text-muted">
                  <svg className="mt-1.5 shrink-0 text-accent" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
                    <path d="M20 6 9 17l-5-5" />
                  </svg>
                  {f}
                </li>
              ))}
            </ul>
            <a href={`mailto:${SITE.email}?subject=${encodeURIComponent(plan.subject)}`} className="btn btn-ghost mt-5">
              Reserve this slot
            </a>
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
            { page: "Homepage", where: "Directly below the hero and stats", detail: "First content block every visitor sees" },
            { page: "This week's standouts", where: "Inside the featured grid", detail: "Styled like a listing, labeled as sponsored" },
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
            <p className="tnum font-mono text-2xl font-semibold text-accent">5</p>
            <p className="text-xs text-muted">surfaces carry the sponsored unit (home, directory, categories, new)</p>
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
          email <a href={`mailto:${SITE.email}`} className="text-accent hover:underline">{SITE.email}</a> with what you’d like to run.
        </p>
      </section>
    </div>
  );
}
