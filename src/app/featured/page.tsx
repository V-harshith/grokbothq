import type { Metadata } from "next";
import Link from "next/link";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { pageMetadata, breadcrumbsJsonLd } from "@/lib/seo";
import { SITE } from "@/data/site";

export const metadata: Metadata = pageMetadata({
  title: "Get Featured — Put Your Grok Bot at the Top",
  description:
    "Featured placements on GrokBot Hub: the top slot on the directory, homepage featuring, and launch-week placement for builders who want maximum qualified opens.",
  path: "/featured",
});

const plans = [
  {
    name: "Featured Listing",
    price: "$29",
    period: "one-time · 4 weeks",
    features: [
      "Top of the directory for your category",
      "'Featured' badge on your listing",
      "Homepage featured slot rotation",
      "Included in the weekly newsletter mention",
      "Do-follow link to your X or landing page",
    ],
    cta: "Apply for featured",
    highlight: true,
  },
  {
    name: "Launch Sponsor",
    price: "$99",
    period: "one-time · launch week",
    features: [
      "Everything in Featured Listing",
      "Sponsored hero slot on the homepage for 7 days",
      "Dedicated post on our X account",
      "Combo placement — we'll feature a workflow using your bot",
      "Post-campaign stats: impressions + opens",
    ],
    cta: "Book launch week",
    highlight: false,
  },
  {
    name: "Category Sponsor",
    price: "$199",
    period: "per month",
    features: [
      "Exclusive sponsorship of one category page",
      "Your bot pinned at the top of the category",
      "A 'sponsor note' section with your pitch",
      "Newsletter mention every week of the month",
      "Best for tools with a Grok-adjacent product",
    ],
    cta: "Sponsor a category",
    highlight: false,
  },
];

export default function FeaturedPage() {
  return (
    <div className="container-x max-w-5xl py-12">
      <JsonLd data={[breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Get featured", path: "/featured" }])]} />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Get featured" }]} />
      <SectionHeader
        kicker="For builders"
        title="Get featured, get opened"
        description="Organic listings are free forever. Featured placements exist for builders who want launch-moment visibility in front of people already searching for a Grok bot like yours."
      />

      <div className="grid gap-4 lg:grid-cols-3">
        {plans.map((plan) => (
          <article key={plan.name} className={`card flex flex-col p-6 ${plan.highlight ? "border-accent" : ""}`}>
            {plan.highlight && <span className="badge badge-accent mb-3 self-start">Most popular</span>}
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
            <a href={`mailto:${SITE.email}?subject=${encodeURIComponent(`${plan.name} inquiry`)}`} className={`btn mt-5 ${plan.highlight ? "btn-accent" : "btn-ghost"}`}>
              {plan.cta}
            </a>
          </article>
        ))}
      </div>

      <section className="card mt-10 p-6 md:p-8">
        <h2 className="text-lg font-semibold">The fine print, up front</h2>
        <ul className="mt-3 space-y-2 text-sm leading-relaxed text-muted">
          <li>· Sponsored placements are always labeled — trust is the whole product.</li>
          <li>· Every sponsored bot still passes the same hand review; we decline anything that would embarrass the page it sits on.</li>
          <li>· One sponsor per category at a time. No bidding wars, no bait-and-switch.</li>
          <li>· Organic listings never lose position to sponsors — featured slots are additive, not cannibalizing.</li>
        </ul>
        <p className="mt-4 text-sm text-muted">
          Questions? Email <a href={`mailto:${SITE.email}`} className="text-accent hover:underline">{SITE.email}</a> or read{" "}
          <Link href="/submit" className="text-accent hover:underline">how free submissions work</Link>.
        </p>
      </section>
    </div>
  );
}
