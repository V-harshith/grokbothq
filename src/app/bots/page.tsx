import type { Metadata } from "next";
import { BotsBrowser } from "@/components/bots-browser";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { bots } from "@/data/bots";
import { pageMetadata, botListJsonLd, breadcrumbsJsonLd, collectionPageJsonLd } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: "All Grok Bots — Hand-Reviewed Directory",
  description:
    "Browse every hand-reviewed Grok bot in one place: assistants, engineering agents, research bots, money hunters, sales tools, creative helpers, and life admin. Filter by category and open any bot in Grok with one click.",
  path: "/bots",
});

export default function BotsPage() {
  return (
    <div className="container-x py-12">
      <JsonLd data={[botListJsonLd(bots, "/bots"), breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Bots", path: "/bots" }]), collectionPageJsonLd("All Grok bots", "The hand-reviewed directory of Grok bots", "/bots")]} />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Bots" }]} />
      <SectionHeader
        kicker="Directory"
        title="Every Grok bot, reviewed by hand"
        description="Every listing below was opened, tested against real prompts, and checked against its description. Use the tabs to filter by category or search to find a specific job."
      />
      <BotsBrowser bots={bots} />
    </div>
  );
}
