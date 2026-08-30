import Link from "next/link";
import type { Metadata } from "next";
import { BotCard } from "@/components/bot-card";
import { ComboCard } from "@/components/combo-card";
import { GuideCard } from "@/components/guide-card";
import { FaqList } from "@/components/faq-list";
import { SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { HeroBot } from "@/components/hero-bot";
import { AdSlot } from "@/components/ad-slot";
import { UseCaseCard } from "@/components/use-case-card";
import { NewsletterForm } from "@/components/newsletter-form";
import { categories } from "@/data/categories";
import { featuredBots, latestBots, stats } from "@/data/bots";
import { combos } from "@/data/combos";
import { guides } from "@/data/guides";
import { faqs } from "@/data/faqs";
import { SITE } from "@/data/site";
import { botsByCategory } from "@/data/bots";
import { pageMetadata, faqJsonLd, absUrl } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: "GrokBot HQ - The Hand-Reviewed Directory of Grok Bots",
  description:
    "Find a Grok bot worth opening. Hand-reviewed directory of the best Grok bots on xAI's platform - browse by category, learn bot combos, and master bot instructions with free guides.",
  path: "/",
});

const homeFaqs = faqs.slice(0, 8);

export default function HomePage() {
  const featured = featuredBots().length ? featuredBots() : latestBots(4);
  const fresh = latestBots(4);
  const useCases = latestBots(30).filter((b) => b.source).slice(0, 3);

  return (
    <>
      <JsonLd data={[faqJsonLd(homeFaqs), { "@context": "https://schema.org", "@type": "WebPage", name: "GrokBot HQ - Grok bot directory", url: absUrl("/"), description: SITE.description }]} />

      {/* Hero */}
      <section className="relative overflow-hidden border-b border-border">
        <div className="hero-glow" aria-hidden />
        <div className="container-x relative pb-16 pt-10 text-center md:pb-20 md:pt-14">
          <HeroBot />
          <h1 className="mx-auto mt-8 max-w-3xl text-4xl font-semibold tracking-tight md:text-6xl">
            Find a Grok bot <span className="text-accent">worth opening</span>
          </h1>
          <p className="mx-auto mt-4 max-w-xl text-base leading-relaxed text-muted md:text-lg">
            Every listing tested by hand. One click opens it in Grok.
          </p>
          <div className="mt-7 flex flex-wrap items-center justify-center gap-3">
            <Link href="/bots" className="btn btn-accent !px-6 !py-3 !text-base">
              Browse {stats.bots} bots
            </Link>
            <Link href="/guides/what-are-grok-bots" className="btn btn-ghost !px-6 !py-3 !text-base">
              New to Grok bots?
            </Link>
          </div>
        </div>
      </section>

      {/* Stats strip */}
      <section className="border-b border-border bg-surface">
        <div className="container-x flex justify-center py-6" data-reveal>
          <dl className="flex flex-wrap items-center justify-center divide-x divide-border">
            {[
              { label: "bots listed", value: `${stats.bots}` },
              { label: "builders", value: `${stats.builders}` },
              { label: "categories", value: `${stats.categories}` },
            ].map((s) => (
              <div key={s.label} className="px-8 text-center">
                <dt className="text-xs text-muted">{s.label}</dt>
                <dd className="font-mono text-xl font-semibold text-accent">{s.value}</dd>
              </div>
            ))}
          </dl>
        </div>
      </section>

      {/* Ad slot (sponsor card, or the quiet Get-featured house ad) */}
      <div className="pt-8">
        <AdSlot />
      </div>

      {/* Featured */}
      <section className="container-x py-16" data-reveal>
        <SectionHeader
          title="This week's standouts"
          description="Rotating picks from the directory. Each one was opened and tested before it earned a listing."
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
        <div className="container-x py-16" data-reveal>
          <SectionHeader
            title="Fresh this week"
            description="Just cleared a full review pass."
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
      <section className="container-x py-16" data-reveal>
        <SectionHeader title="Browse by job" description="Eight categories. Every listing tested against real prompts before it went live." />
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
        <div className="container-x py-16" data-reveal>
          <SectionHeader
            title="Chain bots into workflows"
            description="Two or three bots that hand work to each other. Tested end to end."
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

      {/* Guides */}
      <section className="container-x py-16" data-reveal>
        <SectionHeader
          title="Get good, fast"
          description="Everything we learned reviewing hundreds of bots, written into short guides."
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

      {/* Use cases */}
      <section className="border-y border-border bg-surface">
        <div className="container-x py-16" data-reveal>
          <SectionHeader
            title="Real use, real receipts"
            description="Every example pairs a listed bot with the X post where it was put to work."
            link="/use-cases"
            linkLabel="All use cases"
          />
          <div className="grid gap-4 sm:grid-cols-3">
            {useCases.map((bot) => (
              <UseCaseCard key={bot.slug} bot={bot} />
            ))}
          </div>
        </div>
      </section>

      {/* Newsletter */}
      <section className="container-x max-w-xl py-16 text-center" data-reveal>
        <p className="kicker">The weekly drop</p>
        <h2 className="mt-2 text-2xl font-semibold tracking-tight md:text-3xl">New bots, every week</h2>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          One email with the freshest listings and one combo worth stealing. No spam, unsubscribe anytime.
        </p>
        <div className="mt-6">
          <NewsletterForm />
        </div>
      </section>

      {/* FAQ */}
      <section className="border-t border-border bg-surface">
        <div className="container-x max-w-3xl py-16">
          <SectionHeader title="Questions, answered" description="The questions we get most, answered plainly. More on the full FAQ page." link="/faq" />
          <FaqList faqs={homeFaqs} />
        </div>
      </section>

      {/* CTA */}
      <section className="container-x py-16">
        <div className="card relative overflow-hidden p-10 text-center md:p-14">
          <div className="relative">
            <h2 className="text-2xl font-semibold tracking-tight md:text-3xl">Built a Grok bot? Put it where people are looking.</h2>
            <p className="mx-auto mt-3 max-w-xl text-sm leading-relaxed text-muted md:text-base">
              Listings are free and reviewed within 48 hours. Want the top slot instead? That&apos;s what featured is for.
            </p>
            <div className="mt-6 flex flex-wrap justify-center gap-3">
              <Link href="/submit" className="btn btn-accent !px-6 !py-3">
                List your bot
              </Link>
              <Link href="/featured" className="btn btn-ghost !px-6 !py-3">
                Sponsor the site
              </Link>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
