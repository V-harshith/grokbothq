import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { BotCard, OpenButton } from "@/components/bot-card";
import { Breadcrumbs } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { bots, botMap, relatedBots } from "@/data/bots";
import { categoryMap } from "@/data/categories";
import { pageMetadata, botSoftwareJsonLd, breadcrumbsJsonLd, absUrl } from "@/lib/seo";

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
    title: `${bot.name} — ${bot.tagline}`,
    description: `${bot.description.slice(0, 140)} Open ${bot.name} in Grok with one click.`,
    path: `/bots/${bot.slug}`,
    type: "article",
    publishedTime: bot.addedAt,
    tags: [`${bot.name} grok bot`, `${category?.name ?? ""} grok bot`, "grok bots"],
  });
}

export default async function BotPage({ params }: Props) {
  const { slug } = await params;
  const bot = botMap.get(slug);
  if (!bot) notFound();

  const category = categoryMap.get(bot.category);
  const related = relatedBots(bot);

  return (
    <div className="container-x max-w-4xl py-12">
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
        <h1 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">{bot.name}</h1>
        <p className="mt-2 text-lg text-muted">
          {bot.tagline}{" "}
          <span className="text-sm">
            by{" "}
            <a href={`https://x.com/${bot.builder.x}`} target="_blank" rel="noopener noreferrer" className="text-foreground underline decoration-border underline-offset-4 hover:text-accent">
              @{bot.builder.x}
            </a>
          </span>
        </p>
        <div className="mt-5 flex flex-wrap gap-3">
          <OpenButton bot={bot} />
          <a href={`https://x.ai/bot`} target="_blank" rel="noopener noreferrer" className="btn btn-ghost">
            What is this?
          </a>
        </div>
      </header>

      <section className="prose-block mt-10">
        <h2 className="text-xl font-semibold tracking-tight">What it does</h2>
        <div className="mt-3">
          {bot.description.split("\n\n").map((p) => (
            <p key={p.slice(0, 24)} className="text-[15px] leading-relaxed text-muted">{p}</p>
          ))}
        </div>
      </section>

      <section className="mt-10">
        <h2 className="text-xl font-semibold tracking-tight">Features</h2>
        <ul className="mt-3 grid gap-2 sm:grid-cols-2">
          {bot.features.map((f) => (
            <li key={f} className="card flex items-start gap-2.5 p-3.5 text-sm">
              <svg className="mt-0.5 shrink-0 text-accent" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
                <path d="M20 6 9 17l-5-5" />
              </svg>
              {f}
            </li>
          ))}
        </ul>
      </section>

      <section className="mt-10">
        <h2 className="text-xl font-semibold tracking-tight">Instructions</h2>
        <p className="mt-2 text-sm text-muted">
          The core of the bot&apos;s persona, shared by the builder — this is exactly how it works under the hood.
        </p>
        <pre className="mt-3 overflow-x-auto rounded-xl border border-border p-5 text-[13px] leading-relaxed" style={{ background: "var(--code-bg)", color: "var(--code-fg)" }}>
          <code>{bot.instructions}</code>
        </pre>
      </section>

      <section className="mt-10">
        <h2 className="text-xl font-semibold tracking-tight">You&apos;ll like this if you&apos;re…</h2>
        <div className="mt-3 flex flex-wrap gap-2">
          {bot.bestFor.map((b) => (
            <span key={b} className="badge !normal-case">{b}</span>
          ))}
        </div>
      </section>

      <section className="card mt-10 p-6">
        <h2 className="text-lg font-semibold">How to open {bot.name}</h2>
        <ol className="mt-3 list-decimal space-y-2 pl-5 text-sm leading-relaxed text-muted">
          <li>
            Click <strong className="text-foreground">Open in Grok</strong> above — it takes you straight to the bot at{" "}
            <span className="font-mono text-xs">x.ai/bot</span>.
          </li>
          <li>Sign in with your X account if asked.</li>
          <li>Paste your real task — an inbox, a diff, a question — and the bot handles the rest.</li>
        </ol>
        <div className="mt-4">
          <OpenButton bot={bot} />
        </div>
      </section>

      {related.length > 0 && (
        <section className="mt-14">
          <h2 className="text-xl font-semibold tracking-tight">
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
        Reviewed by hand by the GrokBot Hub team · <Link href="/submit" className="hover:text-foreground">built something similar?</Link> ·{" "}
        <a href={absUrl("/faq")} className="hover:text-foreground">report a problem</a>
      </footer>
    </div>
  );
}
