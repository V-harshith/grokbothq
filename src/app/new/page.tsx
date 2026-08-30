import type { Metadata } from "next";
import { BotCard } from "@/components/bot-card";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { latestBots, stats } from "@/data/bots";
import { SITE } from "@/data/site";
import { pageMetadata, breadcrumbsJsonLd, botListJsonLd } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: "New Grok Bots This Week",
  description:
    "The freshest hand-reviewed Grok bots, updated weekly. See what was just added to the directory and open any new bot in Grok with one click.",
  path: "/new",
});

export default function NewPage() {
  const fresh = [...latestBots(stats.bots)];

  return (
    <div className="container-x max-w-5xl py-12">
      <JsonLd data={[botListJsonLd(fresh, "/new"), breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "New", path: "/new" }])]} />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "New this week" }]} />
      <SectionHeader
        kicker="Updated weekly"
        title="New this week"
        description={`Every listing is reviewed before it goes live. Directory last updated on ${new Date(SITE.lastUpdated).toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })} — newest first.`}
      />
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {fresh.map((bot) => (
          <BotCard key={bot.slug} bot={bot} />
        ))}
      </div>
    </div>
  );
}
