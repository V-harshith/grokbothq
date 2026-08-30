import type { Metadata } from "next";
import Link from "next/link";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { UseCaseCard } from "@/components/use-case-card";
import { bots } from "@/data/bots";
import { categories } from "@/data/categories";
import { pageMetadata, breadcrumbsJsonLd, collectionPageJsonLd, botListJsonLd } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: "How People Use Grok Bots - Real Use Cases from X",
  description:
    "Real-world Grok bot use cases, sourced from the X posts that introduced each bot. See how people automate email, coding, research, money, and daily life with Grok bots.",
  path: "/use-cases",
});

export default function UseCasesPage() {
  const sourced = bots.filter((b) => b.source);
  const grouped = categories
    .map((c) => ({ category: c, items: sourced.filter((b) => b.category === c.slug) }))
    .filter((g) => g.items.length > 0);

  return (
    <div className="container-x max-w-5xl py-12">
      <JsonLd
        data={[
          botListJsonLd(sourced, "/use-cases"),
          collectionPageJsonLd(
            "How people use Grok bots",
            "Real-world Grok bot use cases sourced from X posts",
            "/use-cases"
          ),
          breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Use cases", path: "/use-cases" }]),
        ]}
      />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Use cases" }]} />
      <SectionHeader
        title="How people are using Grok bots"
        description="Every example below is a real, listed bot paired with the X post where its builder put it to work. No hypotheticals - actual use, with a link you can check."
      />

      {grouped.map(({ category, items }) => (
        <section key={category.slug} className="mt-10 first:mt-0">
          <h2 className="text-xl font-semibold tracking-tight">
            {category.name} <span className="font-mono text-sm text-accent">{items.length}</span>
          </h2>
          <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {items.map((bot) => (
              <UseCaseCard key={bot.slug} bot={bot} />
            ))}
          </div>
        </section>
      ))}

      <section className="card mt-14 p-6 md:p-8">
        <h2 className="text-lg font-semibold">Spotted a bot in the wild?</h2>
        <p className="mt-2 text-sm leading-relaxed text-muted">
          When you see a Grok bot doing something useful on X, send it in. Every listing is opened and tested before it
          goes live, and the source post is linked right on the listing.
        </p>
        <div className="mt-4 flex flex-wrap gap-3">
          <Link href="/submit" className="btn btn-accent">
            Submit a bot
          </Link>
          <Link href="/bots" className="btn btn-ghost">
            Browse the directory
          </Link>
        </div>
      </section>
    </div>
  );
}
