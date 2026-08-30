import Link from "next/link";
import type { Metadata } from "next";
import { BotCard } from "@/components/bot-card";
import { ComboCard } from "@/components/combo-card";
import { GuideCard } from "@/components/guide-card";
import { FaqList } from "@/components/faq-list";
import { SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { categories } from "@/data/categories";
import { featuredBots, latestBots, stats } from "@/data/bots";
import { combos } from "@/data/combos";
import { guides } from "@/data/guides";
import { faqs } from "@/data/faqs";
import { SITE } from "@/data/site";
import { botsByCategory } from "@/data/bots";
import { pageMetadata, faqJsonLd, absUrl } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: "GrokBot Hub — The Hand-Reviewed Directory of Grok Bots",
  description:
    "Find a Grok bot worth opening. Hand-reviewed directory of the best Grok bots on xAI's platform — browse by category, learn bot combos, and master bot instructions with free guides.",
  path: "/",
});

const homeFaqs = faqs.slice(0, 8);

export default function HomePage() {
  const featured = featuredBots();
  const fresh = latestBots(4);

  return (
    <>
      <JsonLd data={[faqJsonLd(homeFaqs), { "@context": "https://schema.org", "@type": "WebPage", name: "GrokBot Hub — Grok bot directory", url: absUrl("/"), description: SITE.description }]} />

      {/* Hero */}
      <section className="relative overflow-hidden border-b border-border">
        <div className="grid-bg absolute inset-0" aria-hidden />
        <div className="container-x relative py-20 text-center md:py-28">
          <p className="kicker">Independent · Hand-reviewed · Free forever</p>
          <h1 className="mx-auto mt-4 max-w-3xl text-4xl font-semibold tracking-tight md:text-6xl">
            Find a Grok bot <span className="text-accent">worth opening</span>
          </h1>
          <p className="mx-auto mt-5 max-w-2xl text-base leading-relaxed text-muted md:text-lg">
            {stats.bots} hand-reviewed Grok bots from {stats.builders} builders — assistants, coding agents, money hunters,
            and more. One click opens any bot in Grok. No duds, no prompt wrappers.
          </p>
          <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
            <Link href="/bots" className="btn btn-accent !px-6 !py-3 !text-base">
              Browse the directory
            </Link>
            <Link href="/guides/what-are-grok-bots" className="btn btn-ghost !px-6 !py-3 !text-base">
              New to Grok bots?
            </Link>
          </div>
          <dl className="mx-auto mt-12 grid max-w-2xl grid-cols-3 gap-4 text-center">
            {[
              { label: "Bots listed", value: `${stats.bots}` },
              { label: "Builders", value: `${stats.builders}` },
              { label: "Categories", value: `${stats.categories}` },
            ].map((s) => (
              <div key={s.label} className="card px-4 py-3">
                <dt className="order-2 text-xs text-muted">{s.label}</dt>
                <dd className="order-1 font-mono text-2xl font-semibold text-accent">{s.value}</dd>
              </div>
            ))}
          </dl>
        </div>
      </section>

      {/* Featured */}
      <section className="container-x py-16">
        <SectionHeader
          kicker="Featured"
          title="Bots our reviewers keep coming back to"
          description="Featured bots pass a higher bar: they survive real weekly use by the review team, not just the submission test."
          link="/bots"
          linkLabel="All bots"
        />
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {featured.map((bot) => (
            <BotCard key={bot.slug} bot={bot} />
          ))}
        </div>
      </section>

      {/* New this week */}
      <section className="border-y border-border bg-surface">
        <div className="container-x py-16">
          <SectionHeader
            kicker="Fresh"
            title="New this week"
            description="Recently reviewed and added — the freshest additions to the directory."
            link="/new"
            linkLabel="See all new bots"
          />
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {fresh.map((bot) => (
              <BotCard key={bot.slug} bot={bot} />
            ))}
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="container-x py-16">
        <SectionHeader
          kicker="Browse"
          title="Every category, curated"
          description="Eight categories, each with its own hand-tested shortlist."
        />
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {categories.map((cat) => {
            const count = botsByCategory(cat.slug).length;
            return (
              <Link key={cat.slug} href={`/bots/category/${cat.slug}`} className="card card-hover p-5">
                <h3 className="font-semibold">
                  {cat.name} <span className="font-mono text-sm text-accent">{count}</span>
                </h3>
                <p className="mt-2 text-sm leading-relaxed text-muted">{cat.short}</p>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Combos */}
      <section className="border-y border-border bg-surface">
        <div className="container-x py-16">
          <SectionHeader
            kicker="Combos"
            title="Bots that work better together"
            description="Starting pipelines where each bot hands its output to the next — tested, not theoretical."
            link="/groups"
            linkLabel="All combos"
          />
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {combos.slice(0, 3).map((combo) => (
              <ComboCard key={combo.slug} combo={combo} />
            ))}
          </div>
        </div>
      </section>

      {/* Guides + compare */}
      <section className="container-x py-16">
        <SectionHeader
          kicker="Learn"
          title="Master the Grok bot ecosystem"
          description="Free, practical guides — from your first bot to chaining bots into daily workflows."
          link="/guides"
          linkLabel="All guides"
        />
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {guides.slice(0, 4).map((guide) => (
            <GuideCard key={guide.slug} guide={guide} />
          ))}
        </div>
        <div className="mt-8 flex flex-wrap gap-2">
          <span className="text-sm text-muted">Compare:</span>
          <Link href="/compare/grok-bots-vs-custom-gpts" className="text-sm text-accent hover:underline">
            Grok bots vs Custom GPTs
          </Link>
          <span className="text-muted">·</span>
          <Link href="/compare/grok-bots-vs-claude-skills" className="text-sm text-accent hover:underline">
            vs Claude Skills
          </Link>
          <span className="text-muted">·</span>
          <Link href="/compare/grok-bots-vs-gemini-gems" className="text-sm text-accent hover:underline">
            vs Gemini Gems
          </Link>
          <span className="text-muted">·</span>
          <Link href="/compare" className="text-sm text-muted hover:text-foreground hover:underline">
            all comparisons
          </Link>
        </div>
      </section>

      {/* FAQ */}
      <section className="border-t border-border bg-surface">
        <div className="container-x max-w-3xl py-16">
          <SectionHeader
            kicker="FAQ"
            title="Grok bot questions, answered"
            description="The questions we get most — answered plainly. More on the full FAQ page."
            link="/faq"
          />
          <FaqList faqs={homeFaqs} />
        </div>
      </section>

      {/* CTA */}
      <section className="container-x py-16">
        <div className="card relative overflow-hidden p-10 text-center md:p-14">
          <div className="grid-bg absolute inset-0 opacity-60" aria-hidden />
          <div className="relative">
            <h2 className="text-2xl font-semibold tracking-tight md:text-3xl">Built a Grok bot?</h2>
            <p className="mx-auto mt-3 max-w-xl text-sm leading-relaxed text-muted md:text-base">
              Get it in front of people who are already looking for it. Free listings are hand-reviewed within 48 hours —
              or grab a featured slot for launch week.
            </p>
            <div className="mt-6 flex flex-wrap justify-center gap-3">
              <Link href="/submit" className="btn btn-accent !px-6 !py-3">
                Submit your bot — free
              </Link>
              <Link href="/featured" className="btn btn-ghost !px-6 !py-3">
                Get featured
              </Link>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
