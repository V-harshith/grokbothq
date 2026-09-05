import type { Metadata } from "next";
import Link from "next/link";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { comparePages } from "@/data/compare";
import { pageMetadata, breadcrumbsJsonLd, collectionPageJsonLd } from "@/lib/seo";

export const revalidate = 300; // pages refresh within 5 minutes of content changes

export const metadata: Metadata = pageMetadata({
  title: "Grok Bots vs Everything - Honest Comparisons",
  description:
    "Grok bots compared to Custom GPTs, Claude Skills, Gemini Gems, and agent frameworks - honest verdicts, feature tables, and when to choose each.",
  path: "/compare",
keywords: ["grok bots vs custom gpts", "grok bots vs chatgpt", "grok bots vs claude skills", "grok bots vs gemini gems", "grok bots vs agents", "grok bot comparison"],
});

export default function ComparePage() {
  return (
    <div className="container-x max-w-5xl py-12">
      <JsonLd data={[breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Compare", path: "/compare" }]), collectionPageJsonLd("Grok bot comparisons", "Honest comparisons of Grok bots against the alternatives", "/compare")]} />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Compare" }]} />
      <SectionHeader
        kicker="Compare"
        title="Grok bots vs everything else"
        description="Same idea, different platforms - or genuinely different tools? Each comparison gives the honest overlap, the real differences, and a verdict you can act on."
      />
      <div className="grid gap-4 sm:grid-cols-2">
        {comparePages.map((page) => (
          <Link key={page.slug} href={`/compare/${page.slug}`} className="card card-hover flex flex-col p-6">
            <h2 className="text-lg font-semibold leading-snug">
              Grok Bots <span className="text-muted">vs</span> {page.other}
            </h2>
            <p className="mt-2 flex-1 text-sm leading-relaxed text-muted">{page.verdict.summary.slice(0, 150)}…</p>
            <span className="mt-3 text-sm font-medium text-accent">Read the verdict →</span>
          </Link>
        ))}
      </div>
    </div>
  );
}
