import type { Metadata } from "next";
import Link from "next/link";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { roundups, roundupFacts } from "@/data/roundups";
import { bots } from "@/data/bots";
import { pageMetadata, breadcrumbsJsonLd, collectionPageJsonLd } from "@/lib/seo";

export const revalidate = 300; // pages refresh within 5 minutes of content changes

export const metadata: Metadata = pageMetadata({
  title: "Grok Bot Roundups: Categories Compared",
  description:
    "Category roundups for the Grok bot directory: what each category actually contains, which listings publish install data, and how to choose between them.",
  path: "/roundups",
  keywords: ["grok bot roundup", "best grok bots by category", "compare grok bots", "grok bots compared"],
});

export default function RoundupsIndex() {
  return (
    <div className="container-x max-w-4xl py-12">
      <JsonLd
        data={[
          collectionPageJsonLd(
            "Grok bot roundups",
            "Category-by-category comparisons of the Grok bot directory",
            "/roundups"
          ),
          breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Roundups", path: "/roundups" }]),
        ]}
      />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Roundups" }]} />
      <SectionHeader
        kicker="Compared"
        title="Category roundups"
        description={`Not a list of favourites: each roundup shows what its category contains, how many listings publish anything measurable, and how to choose between them. Every number is computed from the current directory of ${bots.length.toLocaleString("en-US")} bots.`}
        asH1
      />

      <div className="mt-8 grid gap-4">
        {roundups.map((r) => {
          const facts = roundupFacts(r.category);
          return (
            <Link key={r.slug} href={`/roundups/${r.slug}`} className="card card-hover block p-6">
              <div className="flex flex-wrap items-baseline justify-between gap-3">
                <h2 className="text-lg font-semibold tracking-tight">{r.title}</h2>
                <span className="font-mono text-xs text-muted">
                  {facts.total.toLocaleString("en-US")} listings · {facts.withInstalls.toLocaleString("en-US")} with install data
                </span>
              </div>
              <p className="mt-2 text-sm leading-relaxed text-muted">{r.description}</p>
            </Link>
          );
        })}
      </div>

      <p className="mt-8 text-sm text-muted">
        Looking for a specific bot instead?{" "}
        <Link href="/bots" className="text-foreground hover:text-accent">
          Browse all {bots.length.toLocaleString("en-US")} listings
        </Link>{" "}
        or{" "}
        <Link href="/use-cases" className="text-foreground hover:text-accent">
          see them in use
        </Link>
        .
      </p>
    </div>
  );
}
