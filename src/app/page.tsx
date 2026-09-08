import Link from "next/link";
import type { Metadata } from "next";
import { JsonLd } from "@/components/json-ld";
import { HeroMascot } from "@/components/hero-mascot";
import { RotatingAdSlot } from "@/components/rotating-ad-slot";
import { categories } from "@/data/categories";
import { botsByCategory, stats, topInstalledBots } from "@/data/bots";
import { guides, type Guide } from "@/data/guides";
import { SITE } from "@/data/site";
import { absUrl, pageMetadata } from "@/lib/seo";

const HOME_DESCRIPTION =
  "Find a Grok bot worth opening. Hand-reviewed directory of the best Grok bots on xAI's platform - browse by category, learn bot combos, and master bot instructions with free guides.";

export const revalidate = 300;

export const metadata: Metadata = pageMetadata({
  title: "GrokBot HQ - The Hand-Reviewed Directory of Grok Bots",
  description: HOME_DESCRIPTION,
  path: "/",
  keywords: ["grok bots", "grok bot directory", "best grok bots", "grok bot list", "free grok bots", "grok bot combos", "grok xai bots", "grok ai bots", "grok bots that work"],
});

const READ_FIRST_SLUGS = [
  "what-are-grok-bots",
  "how-to-create-a-grok-bot",
  "how-to-write-bot-instructions",
];

const LEVELS: Record<string, string> = {
  "what-are-grok-bots": "Beginner",
  "how-to-create-a-grok-bot": "Builder",
  "how-to-write-bot-instructions": "Craft",
};

function levelFor(guide: Guide): string {
  const level = LEVELS[guide.slug];
  if (level) return level;
  const tag = guide.tags[0];
  if (!tag) return "Guide";
  return tag.charAt(0).toUpperCase() + tag.slice(1);
}

export default function HomePage() {
  const installed = topInstalledBots(6);
  const readFirst = READ_FIRST_SLUGS.map((slug) => guides.find((guide) => guide.slug === slug)).filter(
    (guide): guide is Guide => Boolean(guide),
  );

  return (
    <>
      <JsonLd data={[{ "@context": "https://schema.org", "@type": "WebPage", name: "GrokBot HQ - Grok bot directory", url: absUrl("/"), description: HOME_DESCRIPTION }]} />

      <section className="border-b border-border">
        <div className="container-x grid items-center gap-12 pb-[72px] pt-[96px] md:grid-cols-[1.05fr_0.95fr]">
          <div>
          <p className="kicker in">The independent Grok bot directory</p>
          <h1 className="in d1 mb-[18px] mt-5 max-w-[14ch] text-[clamp(40px,6.4vw,64px)] font-medium leading-[1.05] tracking-[-0.035em]">
            Find a Grok bot worth opening.
          </h1>
          <p className="in d2 max-w-[44ch] text-[17px] text-muted">
            Every listing tested by hand. One click opens it in Grok.
          </p>
          <div className="in d3 mt-[34px] flex flex-wrap gap-3">
            <Link href="/bots" className="btn btn-primary">
              Browse all {stats.bots} bots
            </Link>
            <Link href="/submit" className="btn btn-ghost">
              Submit a bot
            </Link>
          </div>
          </div>
          <div className="in d2 mx-auto w-full max-w-[320px]">
            <HeroMascot className="h-auto w-full" />
          </div>
        </div>
      </section>

      <section className="border-b border-border">
        <div className="container-x flex flex-wrap">
          {[
            { value: `${stats.bots}`, label: "verified bots" },
            { value: `${stats.builders}`, label: "builders" },
            { value: `${stats.categories}`, label: "categories" },
            { value: "100%", label: "opened by hand before listing" },
          ].map((stat, index, list) => (
            <div key={stat.label} className={`min-w-[200px] flex-1 py-[26px] ${index < list.length - 1 ? "border-r border-border pr-6" : ""} ${index > 0 ? "pl-6" : ""}`}>
              <p className="tnum font-mono text-[26px] font-medium tracking-[-0.02em]">{stat.value}</p>
              <p className="mt-1 text-[12.5px] text-muted">{stat.label}</p>
            </div>
          ))}
        </div>
        <p className="container-x pb-5 text-right font-mono text-[11px] text-muted">
          directory updated {new Date(SITE.lastUpdated).toLocaleDateString("en-US", { month: "short", day: "numeric" })}
        </p>
      </section>

      <div className="container-x flex justify-center py-10">
        <RotatingAdSlot />
      </div>

      <section className="container-x py-[72px]" id="bots">
        <div className="mb-7 flex flex-wrap items-baseline justify-between gap-4">
          <h2 className="text-2xl font-medium tracking-[-0.02em]">Most installed</h2>
          <Link href="/bots" className="text-[13.5px] text-muted transition-[color] duration-[180ms] ease-out hover:text-foreground">
            All bots →
          </Link>
        </div>
        <div className="grid gap-[14px] min-[560px]:grid-cols-2 min-[860px]:grid-cols-3">
          {installed.map((bot) => (
            <a
              key={bot.slug}
              href={bot.url}
              target="_blank"
              rel="noopener noreferrer nofollow"
              className="card card-hover flex flex-col gap-3 p-[22px]"
            >
              <div className="flex items-center justify-between gap-[10px]">
                <h3 className="text-base font-medium tracking-[-0.01em]">{bot.name}</h3>
                <span className="whitespace-nowrap rounded-md border border-border px-2 py-[3px] font-mono text-[10.5px] uppercase tracking-[0.08em] text-muted">
                  {bot.category}
                </span>
              </div>
              <p className="flex-1 text-[13.5px] text-muted">{bot.tagline}</p>
              <div className="flex items-center justify-between border-t border-border pt-3 text-[12.5px] text-muted">
                <span>{bot.builder.x ? `by ${bot.builder.x}` : bot.builder.name}</span>
                <span className="tnum font-mono text-foreground">{bot.installs ?? 0} installs</span>
              </div>
            </a>
          ))}
        </div>
      </section>

      <section className="container-x py-[72px]">
        <div className="mb-7 flex flex-wrap items-baseline justify-between gap-4">
          <h2 className="text-2xl font-medium tracking-[-0.02em]">Browse by job</h2>
          <Link href="/use-cases" className="text-[13.5px] text-muted transition-[color] duration-[180ms] ease-out hover:text-foreground">
            All use cases →
          </Link>
        </div>
        <div className="flex flex-wrap gap-[10px]">
          {categories.map((category) => (
            <Link
              key={category.slug}
              href={`/bots/category/${category.slug}`}
              className="inline-flex items-center gap-2 rounded-[10px] border border-border px-[14px] py-[9px] text-[13.5px] transition-[border-color] duration-[180ms] ease-out hover:border-[var(--border-hov)]"
            >
              {category.name}
              <span className="tnum font-mono text-[11px] text-muted">{botsByCategory(category.slug).length}</span>
            </Link>
          ))}
        </div>
      </section>

      <section className="container-x py-[72px]">
        <div className="mb-7 flex flex-wrap items-baseline justify-between gap-4">
          <h2 className="text-2xl font-medium tracking-[-0.02em]">Read first</h2>
          <Link href="/guides" className="text-[13.5px] text-muted transition-[color] duration-[180ms] ease-out hover:text-foreground">
            All guides →
          </Link>
        </div>
        <div className="grid gap-[14px] min-[860px]:grid-cols-3">
          {readFirst.map((guide) => (
            <Link
              key={guide.slug}
              href={`/guides/${guide.slug}`}
              className="card card-hover flex flex-col gap-[10px] p-5"
            >
              <p className="text-xs text-muted">{levelFor(guide)}</p>
              <h3 className="text-[15.5px] font-medium leading-[1.35] tracking-[-0.01em]">{guide.title}</h3>
              <p className="flex gap-[10px] font-mono text-xs text-muted">
                <span>{guide.readingMinutes} min</span>
                <span>updated {new Date(guide.updatedAt).toLocaleDateString("en-US", { month: "short", day: "numeric" })}</span>
              </p>
            </Link>
          ))}
        </div>
      </section>
    </>
  );
}
