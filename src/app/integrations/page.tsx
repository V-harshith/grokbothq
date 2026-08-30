import type { Metadata } from "next";
import Link from "next/link";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { allIntegrations } from "@/lib/integrations";
import { bots } from "@/data/bots";
import { pageMetadata, breadcrumbsJsonLd, collectionPageJsonLd } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: "Grok Bots by Integration - Gmail, Slack, Notion, GitHub & More",
  description:
    "Browse Grok bots by the tools they connect to: Gmail, Google Calendar, Slack, Notion, GitHub, YouTube and more. Every integration is a real page with the bots that use it.",
  path: "/integrations",
});

export default function IntegrationsPage() {
  const integrations = allIntegrations();

  return (
    <div className="container-x max-w-5xl py-12">
      <JsonLd
        data={[
          collectionPageJsonLd("Grok bots by integration", "Every tool a listed Grok bot connects to, each with its own page", "/integrations"),
          breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Integrations", path: "/integrations" }]),
        ]}
      />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Integrations" }]} />
      <SectionHeader
        kicker="Works with"
        title="Browse by integration"
        description={`${bots.length} listed bots, grouped by the tools they connect to. Every integration below is its own page listing the bots that use it.`}
      />

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {integrations.map((intg) => (
          <Link key={intg.slug} href={`/integrations/${intg.slug}`} className="card card-hover p-5">
            <h2 className="font-semibold">
              {intg.name} <span className="font-mono text-sm text-accent">{intg.count}</span>
            </h2>
            <p className="mt-2 text-sm leading-relaxed text-muted">
              {intg.count === 1 ? "One listed bot connects" : `${intg.count} listed bots connect`} to {intg.name}.
            </p>
          </Link>
        ))}
      </div>
    </div>
  );
}
