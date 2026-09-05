import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { BotCard, OpenButton } from "@/components/bot-card";
import { BotFace } from "@/components/bot-face";
import { Breadcrumbs } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { bots, botMap, relatedBots, botOpens } from "@/data/bots";
import { categoryMap } from "@/data/categories";
import { pageMetadata, botSoftwareJsonLd, breadcrumbsJsonLd, absUrl } from "@/lib/seo";

export const revalidate = 300; // pages refresh within 5 minutes of content changes

type Props = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return bots.map((bot) => ({ slug: bot.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const bot = botMap.get(slug);
  if (!bot) return {};
  const category = categoryMap.get(bot.category);
  return pageMetadata({
    title: `${bot.name} - ${bot.tagline}`,
    description: `${bot.description.slice(0, 140)} Open ${bot.name} in Grok with one click.`,
    path: `/bots/${bot.slug}`,
    type: "article",
    publishedTime: bot.addedAt,
    keywords: [
      ...(bot.keywords ?? []),
      `${bot.name} grok bot`,
      bot.name,
      ...(category ? [`${category.name} grok bot`, `grok bots for ${category.name.toLowerCase()}`] : []),
      `${bot.name} review`,
    ],
  });
}

export default async function BotPage({ params }: Props) {
  const { slug } = await params;
  const bot = botMap.get(slug);
  if (!bot) notFound();

  const category = categoryMap.get(bot.category);
  const related = relatedBots(bot, 2);

  return (
    <div className="container-x max-w-6xl py-12">
      <JsonLd
        data={[
          botSoftwareJsonLd(bot),
          breadcrumbsJsonLd([
            { name: "Home", path: "/" },
            { name: "Bots", path: "/bots" },
            ...(category ? [{ name: category.name, path: `/bots/category/${category.slug}` }] : []),
            { name: bot.name, path: `/bots/${bot.slug}` },
          ]),
        ]}
      />
      <Breadcrumbs
        items={[
          { name: "Home", path: "/" },
          { name: "Bots", path: "/bots" },
          ...(category ? [{ name: category.name, path: `/bots/category/${category.slug}` }] : []),
          { name: bot.name },
        ]}
      />

      <div className="grid gap-10 lg:grid-cols-[1fr_320px]">
        {/* main column */}
        <div className="min-w-0">
          <header>
            <div className="flex flex-wrap items-center gap-2">
              {category && (
                <Link href={`/bots/category/${category.slug}`} className="badge hover:text-accent">
                  {category.name}
                </Link>
              )}
              {bot.trending && <span className="badge badge-accent">Trending</span>}
              <span className="text-xs text-muted">
                Added {new Date(bot.addedAt).toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })}
              </span>
            </div>
            <h1 className="mt-3 text-3xl md:text-4xl font-semibold tracking-tighter md:text-5xl">{bot.name}</h1>
            <p className="mt-2 text-lg leading-relaxed text-muted">
              {bot.tagline}
              {bot.builder.x && (
                <span className="text-sm">
                  {" "}by{" "}
                  <a href={`https://x.com/${bot.builder.x}`} target="_blank" rel="noopener noreferrer" className="text-foreground underline decoration-border underline-offset-4 hover:text-accent">
                    @{bot.builder.x}
                  </a>
                </span>
              )}
            </p>
          </header>

          <section className="prose-block mt-8">
            <div>
              {bot.description.split("\n\n").map((p) => (
                <p key={p.slice(0, 24)} className="text-[15px] leading-relaxed text-muted">{p}</p>
              ))}
            </div>
          </section>

          {bot.features && bot.features.length > 0 && (
            <section className="mt-10">
              <h2 className="text-2xl font-semibold tracking-tight">What you get</h2>
              <ul className="mt-4 space-y-2">
                {bot.features.map((f) => (
                  <li key={f} className="flex items-start gap-2.5 border-b border-border pb-2 text-[15px] leading-relaxed text-muted">
                    <svg className="mt-1.5 shrink-0 text-accent" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
                      <path d="M20 6 9 17l-5-5" />
                    </svg>
                    {f}
                  </li>
                ))}
              </ul>
            </section>
          )}

          {bot.instructions && (
            <section className="mt-10">
              <h2 className="text-2xl font-semibold tracking-tight">Instructions</h2>
              <p className="mt-2 text-sm text-muted">
                The core of the bot’s persona, shared by the builder - this is exactly how it works under the hood.
              </p>
              <pre className="mt-3 overflow-x-auto rounded-xl border border-border p-5 text-[13px] leading-relaxed" style={{ background: "var(--code-bg)", color: "var(--code-fg)" }}>
                <code>{bot.instructions}</code>
              </pre>
            </section>
          )}

          {bot.bestFor && bot.bestFor.length > 0 && (
            <section className="mt-10">
              <h2 className="text-2xl font-semibold tracking-tight">You’ll like this if you’re…</h2>
              <div className="mt-3 flex flex-wrap gap-2">
                {bot.bestFor.map((b) => (
                  <span key={b} className="badge !normal-case">{b}</span>
                ))}
              </div>
            </section>
          )}

          {related.length > 0 && (
            <section className="mt-14">
              <h2 className="text-2xl font-semibold tracking-tight">
                More {category?.name.toLowerCase()} bots
              </h2>
              <div className="mt-4 grid gap-4 sm:grid-cols-2">
                {related.map((b) => (
                  <BotCard key={b.slug} bot={b} />
                ))}
              </div>
              {category && (
                <Link href={`/bots/category/${category.slug}`} className="mt-4 inline-block text-sm font-medium text-accent hover:underline">
                  All {category.name.toLowerCase()} bots →
                </Link>
              )}
            </section>
          )}

          <footer className="mt-14 border-t border-border pt-6 text-xs text-muted">
            Reviewed by hand by the GrokBot HQ team. <Link href="/submit" className="hover:text-foreground">built something similar?</Link>{" "}
            <a href={absUrl("/faq")} className="hover:text-foreground">report a problem</a>
          </footer>
        </div>

        {/* sticky rail */}
        <aside className="self-start lg:sticky lg:top-20">
          <div className="card p-5">
            <div className="flex items-center gap-3">
              <BotFace slug={bot.slug} name={bot.name} size={48} />
              <div className="min-w-0">
                <p className="font-semibold leading-snug">{bot.name}</p>
                <p className="text-xs text-muted">{category?.name ?? "Grok bot"}</p>
              </div>
            </div>
            <div className="mt-4 grid gap-2 text-sm">
              <OpenButton bot={bot} />
              {botOpens(bot.slug) > 0 ? (
                <p className="text-center text-xs text-muted">
                  <strong className="tnum font-mono text-foreground">{botOpens(bot.slug)}</strong> opens from GrokBot HQ readers
                </p>
              ) : typeof bot.installs === "number" && bot.installs > 0 && (
                <p className="text-center text-xs text-muted">
                  <strong className="tnum font-mono text-foreground">{bot.installs}</strong> installs reported so far
                </p>
              )}
            </div>
            <dl className="mt-5 space-y-2 border-t border-border pt-4 text-xs">
              <div className="flex justify-between gap-3">
                <dt className="text-muted">Builder</dt>
                <dd className="truncate">
                  {bot.builder.x ? (
                    <a href={`https://x.com/${bot.builder.x}`} target="_blank" rel="noopener noreferrer" className="hover:text-accent">
                      @{bot.builder.x}
                    </a>
                  ) : (
                    "Unknown"
                  )}
                </dd>
              </div>
              <div className="flex justify-between gap-3">
                <dt className="text-muted">Listed</dt>
                <dd>{new Date(bot.addedAt).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}</dd>
              </div>
              {bot.source && (
                <div className="flex justify-between gap-3">
                  <dt className="text-muted">Source</dt>
                  <dd>
                    <a href={bot.source} target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">
                      X post ↗
                    </a>
                  </dd>
                </div>
              )}
            </dl>
            <p className="mt-4 text-center text-[11px] leading-relaxed text-muted">
              Opens at <span className="font-mono">x.ai/bot</span>. Free, no setup.
            </p>
          </div>

          <div className="card mt-4 border-accent/40 p-5">
            <h2 className="text-sm font-semibold">Before you install</h2>
            <p className="mt-2 text-xs leading-relaxed text-muted">
              A shared bot carries somebody else’s instructions. Read them before you run it, and never paste a
              password or an API key if it asks.
            </p>
            <Link href="/guides/grok-bot-safety-and-privacy" className="mt-3 inline-block text-xs font-semibold text-accent hover:underline">
              Safety guide →
            </Link>
          </div>
        </aside>
      </div>
    </div>
  );
}
