import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Breadcrumbs } from "@/components/ui";
import { BotCard } from "@/components/bot-card";
import { FaqList } from "@/components/faq-list";
import { JsonLd } from "@/components/json-ld";
import { RotatingAdSlot } from "@/components/rotating-ad-slot";
import { roundups, roundupMap, roundupFacts, categoryShare } from "@/data/roundups";
import { bots } from "@/data/bots";
import { SITE } from "@/data/site";
import { pageMetadata, breadcrumbsJsonLd, articleJsonLd, faqJsonLd, collectionPageJsonLd } from "@/lib/seo";

export const revalidate = 300; // pages refresh within 5 minutes of content changes

type Props = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return roundups.map((r) => ({ slug: r.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const page = roundupMap.get(slug);
  if (!page) return {};
  return pageMetadata({
    title: page.seoTitle,
    description: page.description,
    path: `/roundups/${page.slug}`,
    type: "article",
    publishedTime: page.updatedAt,
    tags: ["grok bots", `${page.category} grok bots`],
    keywords: [
      `best ${page.category} grok bots`,
      `${page.category} grok bots`,
      `grok bots for ${page.category}`,
      `compare ${page.category} grok bots`,
    ],
  });
}

const n = (value: number) => value.toLocaleString("en-US");

export default async function RoundupPage({ params }: Props) {
  const { slug } = await params;
  const page = roundupMap.get(slug);
  if (!page) notFound();
  const facts = roundupFacts(page.category);
  const share = categoryShare(page.category);

  return (
    <div className="container-x max-w-4xl py-12">
      <JsonLd
        data={[
          faqJsonLd(page.faqs, { dateModified: page.updatedAt }),
          articleJsonLd({
            title: page.title,
            description: page.description,
            path: `/roundups/${page.slug}`,
            dateModified: page.updatedAt,
            author: SITE.name,
          }),
          collectionPageJsonLd(page.title, page.description, `/roundups/${page.slug}`),
          breadcrumbsJsonLd([
            { name: "Home", path: "/" },
            { name: "Roundups", path: "/roundups" },
            { name: page.title, path: `/roundups/${page.slug}` },
          ]),
        ]}
      />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Roundups", path: "/roundups" }, { name: page.title }]} />

      <article>
        <header>
          <p className="kicker">Roundup</p>
          <h1 className="mt-2 text-3xl md:text-4xl font-semibold tracking-tighter md:text-5xl">{page.title}</h1>
          <p className="mt-3 text-[15px] leading-relaxed text-muted">{page.intro}</p>
          <p className="mt-2 text-xs text-muted">
            Updated {new Date(page.updatedAt).toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })}
          </p>
        </header>

        {/* Every number below is computed from the current data on each rebuild. */}
        <section className="card mt-8 p-6" aria-label="What the numbers say">
          <h2 className="text-lg font-semibold">What the numbers say</h2>
          <dl className="mt-4 grid gap-4 text-sm sm:grid-cols-2">
            <div>
              <dt className="font-mono text-2xl font-medium text-foreground">{n(facts.total)}</dt>
              <dd className="text-muted">
                listed {facts.categoryName.toLowerCase()} bots, by {n(facts.builders)} different builders - {share}% of the directory.
              </dd>
            </div>
            <div>
              <dt className="font-mono text-2xl font-medium text-foreground">
                {n(facts.withInstalls)} <span className="text-base text-muted">of {n(facts.total)}</span>
              </dt>
              <dd className="text-muted">
                publish install counts on their own source listing. Any ranking in this category can only order those.
              </dd>
            </div>
            <div>
              <dt className="font-mono text-2xl font-medium text-foreground">
                {n(facts.withIntegrations)} <span className="text-base text-muted">of {n(facts.total)}</span>
              </dt>
              <dd className="text-muted">
                declare a tool connection. An undeclared connection is unknown, not absent.
                {facts.topIntegrations.length > 0 && (
                  <>
                    {" "}Most declared:{" "}
                    {facts.topIntegrations.map((i, idx) => (
                      <span key={i.slug}>
                        <Link href={`/integrations/${i.slug}`} className="text-foreground hover:text-accent">
                          {i.slug}
                        </Link>
                        {idx < facts.topIntegrations.length - 1 ? ", " : ""}
                      </span>
                    ))}
                    .
                  </>
                )}
              </dd>
            </div>
            <div>
              <dt className="font-mono text-2xl font-medium text-foreground">{n(facts.addedLast7)}</dt>
              <dd className="text-muted">added in the last seven days - this category is still filling up.</dd>
            </div>
          </dl>
        </section>

        <section className="mt-10" aria-label="Shortlist">
          <h2 className="text-xl font-semibold tracking-tight">The shortlist, by published installs</h2>
          <p className="mt-2 text-sm text-muted">
            Ordered by the install count each bot&apos;s own source listing publishes - the only outcome measure available, and
            one that only {n(facts.withInstalls)} of {n(facts.total)} listings here provide. It is a ranking of the documented,
            not of the best.
          </p>
          {facts.ranked.length > 0 ? (
            <ol className="mt-4 divide-y divide-border border-y border-border">
              {facts.ranked.map((bot, i) => (
                <li key={bot.slug} className="flex items-baseline justify-between gap-4 py-3">
                  <span className="flex min-w-0 items-baseline gap-3">
                    <span className="font-mono text-xs text-muted">{i + 1}</span>
                    <span className="min-w-0">
                      <Link href={`/bots/${bot.slug}`} className="font-medium hover:text-accent">
                        {bot.name}
                      </Link>
                      <span className="block truncate text-[13px] text-muted">{bot.tagline}</span>
                    </span>
                  </span>
                  <span className="tnum shrink-0 font-mono text-sm text-foreground">{bot.installs} installs</span>
                </li>
              ))}
            </ol>
          ) : (
            <p className="mt-4 text-sm text-muted">
              No listing in this category publishes an install count, so there is nothing to rank on. The category page lists
              all {n(facts.total)}.
            </p>
          )}
        </section>

        <section className="mt-10" aria-label="How we picked">
          <h2 className="text-xl font-semibold tracking-tight">How we picked</h2>
          <ul className="mt-4 space-y-2">
            {page.howWePicked.map((line) => (
              <li key={line} className="border-b border-border pb-2 text-sm leading-relaxed text-muted">
                {line}
              </li>
            ))}
          </ul>
        </section>

        {page.sections.map((section) => (
          <section key={section.heading} className="mt-10">
            <h2 className="text-xl font-semibold tracking-tight">{section.heading}</h2>
            <div className="prose-block mt-3">
              {section.body.map((p) => (
                <p key={p.slice(0, 24)} className="mt-3 text-[15px] leading-relaxed text-muted">
                  {p}
                </p>
              ))}
            </div>
          </section>
        ))}

        <section className="mt-12" aria-label="Newest listings">
          <div className="mb-5 flex flex-wrap items-baseline justify-between gap-3">
            <h2 className="text-xl font-semibold tracking-tight">Newest in {facts.categoryName.toLowerCase()}</h2>
            <Link href={`/bots/category/${page.category}`} className="text-sm text-muted hover:text-foreground">
              All {n(facts.total)} →
            </Link>
          </div>
          <div className="grid gap-4 sm:grid-cols-2">
            {facts.newest.map((bot) => (
              <BotCard key={bot.slug} bot={bot} />
            ))}
          </div>
        </section>

        <section className="mt-12" aria-label="Questions">
          <h2 className="text-xl font-semibold tracking-tight">Questions</h2>
          <FaqList faqs={page.faqs} />
        </section>

        <footer className="mt-12 border-t border-border pt-6 text-sm text-muted">
          <p>
            This roundup covers the{" "}
            <Link href={`/bots/category/${page.category}`} className="text-foreground hover:text-accent">
              {facts.categoryName.toLowerCase()}
            </Link>{" "}
            category - {n(facts.total)} listings, all checked against their own public page. Prefer to browse everything?{" "}
            <Link href="/bots" className="text-foreground hover:text-accent">
              The whole directory
            </Link>{" "}
            is {n(bots.length)} bots and counting.
          </p>
        </footer>

        <div className="mt-8 flex justify-center">
          <RotatingAdSlot />
        </div>
      </article>
    </div>
  );
}
