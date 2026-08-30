import type { Metadata } from "next";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { pageMetadata, breadcrumbsJsonLd } from "@/lib/seo";
import { SITE, DISCLAIMER } from "@/data/site";

export const metadata: Metadata = pageMetadata({
  title: "Terms of Use",
  description: "The simple terms for using GrokBot HQ: what the directory is, how listings and submissions work, and the limits of our responsibility.",
  path: "/terms",
});

export default function TermsPage() {
  return (
    <div className="container-x max-w-3xl py-12">
      <JsonLd data={[breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Terms", path: "/terms" }])]} />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Terms" }]} />
      <SectionHeader
        kicker="Legal"
        title="Terms of use"
        description="Plain-language terms. The gist: use the site, verify before you rely on anything, and remember the bots live on xAI's platform, not here."
      />

      <div className="prose-block mt-10">
        <h2 className="text-xl font-semibold tracking-tight">What this site is</h2>
        <p className="text-[15px] leading-relaxed text-muted">
          An independent directory of Grok bots with guides and curated news. Listings link to bots hosted on xAI&apos;s
          platform; we host none of them. {DISCLAIMER}
        </p>

        <h2 className="mt-8 text-xl font-semibold tracking-tight">Listings and submissions</h2>
        <p className="text-[15px] leading-relaxed text-muted">
          Submissions are reviewed before publication and may be rejected or later delisted for any reason, including
          broken links, misleading descriptions, or policy violations. By submitting, you confirm you have the right to
          describe the bot and that the description is accurate. Descriptions are short factual summaries written by
          our editors; bot names and builders belong to their respective owners.
        </p>

        <h2 className="mt-8 text-xl font-semibold tracking-tight">Sponsorships</h2>
        <p className="text-[15px] leading-relaxed text-muted">
          Sponsored placements are paid and always labeled. A sponsorship is a placement, not an endorsement, and it
          never changes an organic listing&apos;s position. Sponsors pass the same review as organic submissions.
        </p>

        <h2 className="mt-8 text-xl font-semibold tracking-tight">No warranty</h2>
        <p className="text-[15px] leading-relaxed text-muted">
          The site and its content are provided as is. Bot behavior depends on xAI&apos;s platform and each builder&apos;s
          instructions - test a bot yourself before relying on its output, especially for money, legal, or health
          matters. We are not liable for what a third-party bot does, and links to external sites are not
          endorsements of their content.
        </p>

        <h2 className="mt-8 text-xl font-semibold tracking-tight">Contact</h2>
        <p className="text-[15px] leading-relaxed text-muted">
          Questions, takedown requests, or corrections: {SITE.email}.
        </p>
      </div>
    </div>
  );
}
