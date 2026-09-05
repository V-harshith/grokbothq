import Link from "next/link";
import type { Metadata } from "next";
import { BotCard } from "@/components/bot-card";
import { ComboCard } from "@/components/combo-card";
import { GuideCard } from "@/components/guide-card";
import { FaqList } from "@/components/faq-list";
import { SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { HeroBot } from "@/components/hero-bot";
import { AdSlotCard } from "@/components/ad-slot";
import { UseCaseCard } from "@/components/use-case-card";
import { NewsletterForm } from "@/components/newsletter-form";
import { news } from "@/lib/news";
import { CopyAgentPrompt } from "@/components/copy-agent-prompt";
import { categories } from "@/data/categories";
import { featuredBots, latestBots, stats, bots } from "@/data/bots";
import { combos } from "@/data/combos";
import { guides } from "@/data/guides";
import { SITE } from "@/data/site";
import { faqs } from "@/data/faqs";
import { botsByCategory } from "@/data/bots";
import { pageMetadata, faqJsonLd, absUrl } from "@/lib/seo";

export const revalidate = 300; // pages refresh within 5 minutes of content changes

export const metadata: Metadata = pageMetadata({
  title: "GrokBot HQ - The Hand-Reviewed Directory of Grok Bots",
  description:
    "Find a Grok bot worth opening. Hand-reviewed directory of the best Grok bots on xAI's platform - browse by category, learn bot combos, and master bot instructions with free guides.",
  path: "/",
keywords: ["grok bots", "grok bot directory", "best grok bots", "grok bot list", "free grok bots", "grok bot combos", "grok xai bots", "grok ai bots", "grok bots that work"],
});


export default function HomePage() {
  const fresh = latestBots(4);
  const freshSlugs = new Set(fresh.map((b) => b.slug));
  // Standouts: paid featured placements first, then top-installed bots - always
  // excluding the fresh row so the same bot never appears in both sections.
  const standouts = (() => {
    const featured = featuredBots().filter((b) => !freshSlugs.has(b.slug));
    if (featured.length >= 3) return featured.slice(0, 3);
    const rest = [...bots]
      .filter((b) => !freshSlugs.has(b.slug))
      .sort((a, b) => (b.installs ?? 0) - (a.installs ?? 0));
    return [...featured, ...rest].slice(0, 3);
  })();
  const useCases = latestBots(30).filter((b) => b.source).slice(0, 3);

  return (
    <>
      <JsonLd data={[faqJsonLd(faqs.slice(0, 8), { dateModified: SITE.lastUpdated }), { "@context": "https://schema.org", "@type": "WebPage", name: "GrokBot HQ - Grok bot directory", url: absUrl("/"), description: SITE.description }]} />

      {/* Hero */}
      <section className="relative overflow-hidden border-b border-border">
        <div className="hero-glow" aria-hidden />
        <div className="container-x relative pb-16 pt-10 text-center md:pb-20 md:pt-14">
          <HeroBot />
          <h1 className="mx-auto mt-8 max-w-3xl text-4xl md:text-7xl font-semibold tracking-tighter leading-[1.05]">
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
            <CopyAgentPrompt />
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
                <dd className="tnum font-mono text-xl font-semibold text-accent">{s.value}</dd>
              </div>
            ))}
          </dl>
        </div>
      </section>

      {/* Featured */}
      <section className="container-x py-16 md:py-24" data-reveal>
        <SectionHeader
          kicker="Featured" title="This week's standouts"
          description="Rotating picks from the directory. Each one was opened and tested before it earned a listing."
          link="/bots"
          linkLabel="All bots"
        />
        <div className="stagger grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {standouts.map((bot) => (
            <BotCard key={bot.slug} bot={bot} />
          ))}
          <AdSlotCard />
        </div>
      </section>

      {/* New this week */}
      <section className="border-y border-border bg-surface">
        <div className="container-x py-16 md:py-24" data-reveal>
          <SectionHeader
            kicker="New listings" title="Fresh this week"
            description="Just cleared a full review pass."
            link="/new"
            linkLabel="See all new bots"
          />
          <div className="stagger grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {fresh.map((bot) => (
              <BotCard key={bot.slug} bot={bot} />
            ))}
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="container-x py-16 md:py-24" data-reveal>
        <SectionHeader kicker="Categories" title="Browse by job" description="Eight categories. Every listing tested against real prompts before it went live." />
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
        <div className="container-x py-16 md:py-24" data-reveal>
          <SectionHeader
            kicker="Combos" title="Chain bots into workflows"
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
      <section className="container-x py-16 md:py-24" data-reveal>
        <SectionHeader
          kicker="Guides" title="Get good, fast"
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

      {/* Power tools */}
      <section className="container-x py-16 md:py-24" data-reveal>
        <SectionHeader
          kicker="Power tools"
          title="More than a list"
          description="The directory is machine-readable. Point your own Grok Bot at it, browse by the tools you already use, or subscribe to the feed."
        />
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Link href="/agent" className="card card-hover flex flex-col p-6">
            <h3 className="font-semibold">Point your Grok Bot here</h3>
            <p className="mt-2 flex-1 text-sm leading-relaxed text-muted">
              Copy one prompt and your bot fetches the directory itself - recommends bots for any task, on your schedule.
            </p>
            <span className="mt-4 text-xs font-semibold text-accent">Get the routines →</span>
          </Link>
          <Link href="/integrations" className="card card-hover flex flex-col p-6">
            <h3 className="font-semibold">Browse by integration</h3>
            <p className="mt-2 flex-1 text-sm leading-relaxed text-muted">
              Gmail, Slack, Notion, GitHub - every tool a listed bot connects to gets its own page.
            </p>
            <span className="mt-4 text-xs font-semibold text-accent">Find yours →</span>
          </Link>
          <div className="card flex flex-col p-6">
            <h3 className="font-semibold">Read it like a feed</h3>
            <p className="mt-2 flex-1 text-sm leading-relaxed text-muted">
              RSS for new drops and news, or the whole directory as one JSON document. No key, no account.
            </p>
            <span className="mt-4 space-x-4 text-xs font-semibold">
              <a href="/rss.xml" className="text-accent hover:underline">RSS →</a>
              <a href="/api/v1/index.json" className="text-accent hover:underline">JSON API →</a>
            </span>
          </div>
          <Link href="/stats" className="card card-hover flex flex-col p-6">
            <h3 className="font-semibold">State of Grok Bots</h3>
            <p className="mt-2 flex-1 text-sm leading-relaxed text-muted">
              Original daily-computed statistics: category distribution, installs, builders, growth. Citable under CC BY.
            </p>
            <span className="mt-4 text-xs font-semibold text-accent">See the data →</span>
          </Link>
        </div>
      </section>

      {/* Use cases */}
      <section className="border-y border-border bg-surface">
        <div className="container-x py-16 md:py-24" data-reveal>
          <SectionHeader
            kicker="Use cases" title="Real use, real receipts"
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

      {/* News */}
      <section className="container-x py-16 md:py-24" data-reveal>
        <SectionHeader
          kicker="Ecosystem" title="Grok news, curated"
          description="Launches and ecosystem moves, one line each, always linked to the source."
          link="/news"
          linkLabel="All news"
        />
        <ol className="divide-y divide-border">
          {news.slice(0, 3).map((item) => (
            <li key={item.url + item.date} className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1 py-4">
              <a href={item.url} target="_blank" rel="noopener noreferrer" className="font-medium hover:text-accent">
                {item.title}
              </a>
              <span className="text-xs text-muted">
                {item.source}, {new Date(item.date).toLocaleDateString("en-US", { month: "short", day: "numeric" })}
              </span>
            </li>
          ))}
        </ol>
      </section>

      {/* Newsletter */}
      <section className="container-x max-w-xl py-16 md:py-24 text-center" data-reveal>
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
        <div className="container-x max-w-3xl py-16 md:py-24">
          <SectionHeader kicker="FAQ" title="Questions, answered" description="The questions we get most, answered plainly. More on the full FAQ page." link="/faq" />
          <FaqList faqs={faqs.slice(0, 8)} />
        </div>
      </section>

      {/* CTA */}
      <section className="container-x py-16 md:py-24">
        <div className="card relative overflow-hidden p-10 text-center md:p-14">
          <div className="relative">
            <h2 className="text-3xl md:text-4xl font-semibold tracking-tighter">Built a Grok bot? Put it where people are looking.</h2>
            <p className="mx-auto mt-3 max-w-xl text-sm leading-relaxed text-muted md:text-base">
              Listings are free and reviewed within 48 hours. Want the top slot instead? That’s what featured is for.
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
