import type { Metadata } from "next";
import { GuideCard } from "@/components/guide-card";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { guides } from "@/data/guides";
import { pageMetadata, breadcrumbsJsonLd, collectionPageJsonLd } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: "Grok Bot Guides - Create, Write Instructions, Chain & Monetize",
  description:
    "Free, practical Grok bot guides: what bots are, how to create one in 10 minutes, instruction-writing patterns, chaining bots into workflows, safety, and monetization.",
  path: "/guides",
  keywords: ["grok bot guides", "how to create a grok bot", "grok bot instructions", "grok bot tutorial", "grok bot tips", "grok bot workflow"],
});

export default function GuidesPage() {
  return (
    <div className="container-x max-w-5xl py-12">
      <JsonLd data={[breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Guides", path: "/guides" }]), collectionPageJsonLd("Grok bot guides", "Free, practical guides to the Grok bot ecosystem", "/guides")]} />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Guides" }]} />
      <SectionHeader
        kicker="Learn"
        title="Grok bot guides, written by reviewers"
        description="Everything we've learned hand-testing hundreds of bots, distilled into practical guides. No fluff, no course upsells - each guide ends with something you can do today."
      />
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {guides.map((guide) => (
          <GuideCard key={guide.slug} guide={guide} />
        ))}
      </div>
    </div>
  );
}
