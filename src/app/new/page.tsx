import type { Metadata } from "next";
import { BotCard } from "@/components/bot-card";
import { Pagination, PAGE_SIZE, pageNumber, pageHref, totalPagesFor } from "@/components/pagination";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { AdSlotCard } from "@/components/ad-slot";
import { newBots, stats } from "@/data/bots";
import { SITE } from "@/data/site";
import { absUrl, pageMetadata, breadcrumbsJsonLd, botListJsonLd } from "@/lib/seo";

export const revalidate = 300; // pages refresh within 5 minutes of content changes

type Props = { searchParams: Promise<{ page?: string }> };

const TOTAL_PAGES = totalPagesFor(newBots.length);

export async function generateMetadata({ searchParams }: Props): Promise<Metadata> {
  const page = pageNumber((await searchParams).page, TOTAL_PAGES);
  const base = pageMetadata({
    title: page === 1 ? "New Grok Bots This Week - Fresh Drops" : `New Grok Bots - Page ${page} of ${TOTAL_PAGES}`,
    description:
      page === 1
        ? "The freshest checked Grok bots, updated as they are added. See what just landed in the directory and open any new bot in Grok with one click."
        : `Page ${page} of ${TOTAL_PAGES} of new Grok bots - earlier additions still in the directory, newest first.`,
    path: pageHref("/new", page),
    keywords: ["new grok bots", "newest grok bots", "grok bots this week", "fresh grok bots", "latest grok bots"],
  });
  return page === 1 ? base : { ...base, alternates: { canonical: absUrl(pageHref("/new", page)) } };
}

export default async function NewPage({ searchParams }: Props) {
  const page = pageNumber((await searchParams).page, TOTAL_PAGES);
  const start = (page - 1) * PAGE_SIZE;
  // This page used to server-render the entire directory (~10 MB of HTML) to show "new" listings.
  // It is a chronological series now: 60 per page, each page linked from the last.
  const fresh = newBots.slice(start, start + PAGE_SIZE);
  const total = newBots.length;

  return (
    <div className="container-x max-w-5xl py-12">
      <JsonLd
        data={[
          botListJsonLd(fresh, pageHref("/new", page)),
          breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "New", path: "/new" }]),
        ]}
      />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Newest additions" }]} />
      <SectionHeader
        kicker="Newest first"
        title={page === 1 ? "Newest Grok bots" : `Newest Grok bots - page ${page}`}
        description={`Every listing is checked before it goes live. This page shows ${start + 1}-${Math.min(start + PAGE_SIZE, total)} of ${total.toLocaleString("en-US")} listings, newest first - the newest week is at the top. Directory last updated on ${new Date(SITE.lastUpdated).toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })}.`}
        asH1
      />
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {page === 1 && fresh.length > 3 ? (
          <>
            {fresh.slice(0, 3).map((bot) => (
              <BotCard key={bot.slug} bot={bot} />
            ))}
            <AdSlotCard />
            {fresh.slice(3).map((bot) => (
              <BotCard key={bot.slug} bot={bot} />
            ))}
          </>
        ) : (
          fresh.map((bot) => (
            <BotCard key={bot.slug} bot={bot} />
          ))
        )}
      </div>
      <Pagination basePath="/new" page={page} totalPages={TOTAL_PAGES} label="New Grok bots" />
    </div>
  );
}
