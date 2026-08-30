import type { Metadata } from "next";
import { ComboCard } from "@/components/combo-card";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { combos } from "@/data/combos";
import { pageMetadata, breadcrumbsJsonLd, collectionPageJsonLd } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: "Grok Bot Combos - Sets of Bots That Work Together",
  description:
    "Curated Grok bot combos: sets of two or three bots that hand work to each other - Ship Desk for overnight engineering, Research Desk for cited briefs, Money Hunters for real cash back.",
  path: "/groups",
});

export default function GroupsPage() {
  return (
    <div className="container-x max-w-5xl py-12">
      <JsonLd data={[breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Combos", path: "/groups" }]), collectionPageJsonLd("Grok bot combos", "Sets of Grok bots that work together", "/groups")]} />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Combos" }]} />
      <SectionHeader
        kicker="Combos"
        title="Bots that work better together"
        description="Single-purpose bots are the unit - combos are the workflow. Each combo is a paste-outputs-forward pipeline we've tested end to end. They're starting ideas, not integrations: you are the transport layer."
      />
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {combos.map((combo) => (
          <ComboCard key={combo.slug} combo={combo} />
        ))}
      </div>

      <section className="card mt-12 p-6 md:p-8">
        <h2 className="text-lg font-semibold">How combos work (and what they can&apos;t do)</h2>
        <p className="mt-3 text-sm leading-relaxed text-muted">
          A combo is a sequence: run bot A, copy its structured output, paste it into bot B. The magic ingredient is output
          discipline - every bot in a combo produces a clean artifact (a verdict, a ranked list, a drafted email) that the
          next bot consumes happily. Bots can&apos;t call each other or share memory; if you need unattended automation,
          that&apos;s an agent framework problem. Our guide to{" "}
          <a href="/guides/how-to-chain-grok-bots" className="text-accent hover:underline">
            chaining Grok bots
          </a>{" "}
          covers the details.
        </p>
      </section>
    </div>
  );
}
