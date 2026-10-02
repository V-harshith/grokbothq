import type { Metadata } from "next";
import Link from "next/link";
import { BotsBrowser } from "@/components/bots-browser";
import { BotCard } from "@/components/bot-card";
import { Pagination, PAGE_SIZE, pageNumber, pageHref, totalPagesFor } from "@/components/pagination";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { RotatingAdSlot } from "@/components/rotating-ad-slot";
import { bots, categoryTotals, previewBots } from "@/data/bots";
import { roundups } from "@/data/roundups";
import { categories } from "@/data/categories";
import { SITE } from "@/data/site";
import { absUrl, pageMetadata, botListJsonLd, breadcrumbsJsonLd, collectionPageJsonLd } from "@/lib/seo";

export const revalidate = 300; // pages refresh within 5 minutes of content changes

type Props = { searchParams: Promise<{ page?: string }> };

const TOTAL_PAGES = totalPagesFor(bots.length);

/**
 * How many listings the interactive browser holds. Sending the whole directory to the client island
 * put a ~1.5 MB React flight payload inside a page whose first byte of HTML is already 2.2 MB.
 */
const CLIENT_BROWSER_LIMIT = 600;

export async function generateMetadata({ searchParams }: Props): Promise<Metadata> {
  const page = pageNumber((await searchParams).page, TOTAL_PAGES);
  const base = pageMetadata({
    // Carries the head term ("grok bot directory") in the title, the H1 and the opening line - it
    // ranked 29th with the phrase only in the meta tag, on a page that never said it out loud.
    title:
      page === 1
        ? "Grok Bot Directory: Browse All Hand-Reviewed Grok Bots"
        : `Grok Bot Directory - Page ${page} of ${TOTAL_PAGES}`,
    description:
      page === 1
        ? "The grok bots directory: browse every hand-reviewed Grok bot in one place: assistants, engineering agents, research bots, money hunters, sales tools, creative helpers, and life admin. Filter by category and open any bot in Grok with one click."
        : `Page ${page} of ${TOTAL_PAGES} of the Grok bot directory - every hand-reviewed Grok bot, in one place. Open any bot in Grok with one click.`,
    path: pageHref("/bots", page),
    keywords: ["grok bot directory", "grok bots directory", "grok bots list", "all grok bots", "best grok bots", "free grok bots", "grok bot categories", "browse grok bots"],
  });
  // Each page of the series stands on its own: self-canonical, so a crawler reads it as a page of
  // the directory rather than as a duplicate of page 1.
  return page === 1 ? base : { ...base, alternates: { canonical: absUrl(pageHref("/bots", page)) } };
}

export default async function BotsPage({ searchParams }: Props) {
  const page = pageNumber((await searchParams).page, TOTAL_PAGES);
  const start = (page - 1) * PAGE_SIZE;
  const slice = bots.slice(start, start + PAGE_SIZE);

  return (
    <div className="container-x py-12">
      <JsonLd
        data={[
          botListJsonLd(slice, pageHref("/bots", page)),
          breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Bots", path: "/bots" }]),
          collectionPageJsonLd("All Grok bots", "The hand-reviewed directory of Grok bots", pageHref("/bots", page)),
        ]}
      />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Bots" }]} />
      <div className="flex flex-col gap-8 lg:flex-row lg:items-start lg:justify-between">
        <SectionHeader
          kicker="Directory"
          title={page === 1 ? "The Grok bot directory: every bot, reviewed by hand" : `The Grok bot directory - page ${page} of ${TOTAL_PAGES}`}
          description={
            page === 1
              ? `Every listing below is described in full and was checked against the bot's own public listing before it went live. Use the tabs to filter by category, search for a specific job, or page through the whole directory - ${bots.length.toLocaleString("en-US")} bots and counting.`
              : `Listings ${start + 1}-${Math.min(start + PAGE_SIZE, bots.length)} of ${bots.length.toLocaleString("en-US")}. Every bot is checked against its own public listing; a listing that stops answering is delisted.`
          }
          asH1
        />
        <div className="shrink-0 lg:pt-1">
          <RotatingAdSlot />
        </div>
      </div>

      {page === 1 ? (
        <BotsBrowser bots={previewBots(CLIENT_BROWSER_LIMIT)} totals={categoryTotals()} />
      ) : (
        <>
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {slice.map((bot) => (
              <BotCard key={bot.slug} bot={bot} />
            ))}
          </div>
          <p className="mt-6 text-sm text-muted">
            Looking for one specific bot?{" "}
            <Link href="/bots" className="text-accent hover:underline">
              Search and filter the whole directory
            </Link>
            .
          </p>
        </>
      )}

      <Pagination basePath="/bots" page={page} totalPages={TOTAL_PAGES} label="Grok bot directory" />

      <p className="mt-6 text-center text-sm text-muted">
        After a shortlist rather than a list?{" "}
        {roundups.map((r, i) => (
          <span key={r.slug}>
            <Link href={`/roundups/${r.slug}`} className="text-foreground hover:text-accent">
              {categories.find((c) => c.slug === r.category)?.name ?? r.category}
            </Link>
            {i < roundups.length - 1 ? " · " : " "}
          </span>
        ))}
        bots, compared.
      </p>

      {page === 1 && (
        <section className="card mt-10 p-6" aria-label="Methodology">
          <h2 className="text-lg font-semibold">How the numbers are counted</h2>
          <dl className="mt-4 grid gap-4 text-sm leading-relaxed text-muted sm:grid-cols-2">
            <div>
              <dt className="font-semibold text-foreground">Every listing is checked</dt>
              <dd>Each bot is checked against its own public x.ai listing before it earns a page here, and re-checked daily. A listing that stops answering is delisted, not left to rot.</dd>
            </div>
            <div>
              <dt className="font-semibold text-foreground">Install counts come from the source listing</dt>
              <dd>Where a bot&apos;s public listing publishes install data, we show that number and link the bot and builder.</dd>
            </div>
            <div>
              <dt className="font-semibold text-foreground">Data freshness</dt>
              <dd>
                The directory is re-verified daily and was last updated on{" "}
                {new Date(SITE.lastUpdated).toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })}.
              </dd>
            </div>
            <div>
              <dt className="font-semibold text-foreground">Limitations</dt>
              <dd>Bot behavior depends on xAI&apos;s platform and each builder&apos;s instructions - test a bot yourself before relying on it.</dd>
            </div>
          </dl>
        </section>
      )}
    </div>
  );
}
