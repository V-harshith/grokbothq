import type { Metadata } from "next";
import { BotsBrowser } from "@/components/bots-browser";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { AdSlot } from "@/components/ad-slot";
import { bots } from "@/data/bots";
import { SITE } from "@/data/site";
import { pageMetadata, botListJsonLd, breadcrumbsJsonLd, collectionPageJsonLd } from "@/lib/seo";

export const revalidate = 300; // pages refresh within 5 minutes of content changes

export const metadata: Metadata = pageMetadata({
  title: "All Grok Bots - Hand-Reviewed Directory",
  description:
    "Browse every hand-reviewed Grok bot in one place: assistants, engineering agents, research bots, money hunters, sales tools, creative helpers, and life admin. Filter by category and open any bot in Grok with one click.",
  path: "/bots",
keywords: ["grok bots list", "all grok bots", "best grok bots", "free grok bots", "grok bot categories", "browse grok bots"],
});

export default function BotsPage() {
  return (
    <div className="container-x py-12">
      <JsonLd data={[botListJsonLd(bots, "/bots"), breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Bots", path: "/bots" }]), collectionPageJsonLd("All Grok bots", "The hand-reviewed directory of Grok bots", "/bots")]} />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Bots" }]} />
      <div className="flex flex-col gap-8 lg:flex-row lg:items-start lg:justify-between">
        <SectionHeader
          kicker="Directory"
          title="Every Grok bot, reviewed by hand"
          description="Every listing below was opened, tested against real prompts, and checked against its description. Use the tabs to filter by category or search to find a specific job."
        />
        <div className="shrink-0 lg:pt-1">
          <AdSlot />
        </div>
      </div>
      <BotsBrowser bots={bots} />
      <section className="card mt-10 p-6" aria-label="Methodology">
        <h2 className="text-lg font-semibold">How the numbers are counted</h2>
        <dl className="mt-4 grid gap-4 text-sm leading-relaxed text-muted sm:grid-cols-2">
          <div>
            <dt className="font-semibold text-foreground">Every listing was opened and tested</dt>
            <dd>Each bot is run against real prompts before it earns a page here. Listings that fail or die are set to hidden, not shown.</dd>
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
    </div>
  );
}
