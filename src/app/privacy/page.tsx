import type { Metadata } from "next";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { pageMetadata, breadcrumbsJsonLd } from "@/lib/seo";
import { SITE, DISCLAIMER } from "@/data/site";

export const metadata: Metadata = pageMetadata({
  title: "Privacy Policy",
  description: "What GrokBot HQ collects (almost nothing), what it never collects, and how third parties like Umami and xAI fit in.",
  path: "/privacy",
});

export default function PrivacyPage() {
  return (
    <div className="container-x max-w-3xl py-12">
      <JsonLd data={[breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Privacy", path: "/privacy" }])]} />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Privacy" }]} />
      <SectionHeader
        kicker="Legal"
        title="Privacy policy"
        description="Short version: this site has no accounts, no logins, and nothing to sell about you. Here is exactly what touches your data."
      />

      <div className="prose-block mt-10">
        <h2 className="text-xl font-semibold tracking-tight">What we collect</h2>
        <p className="text-[15px] leading-relaxed text-muted">
          If analytics are enabled, the site uses Umami - a cookieless, privacy-first analytics tool - to count page
          views and referral sources. Umami does not use cookies, does not build advertising profiles, and does not
          store personal identifiers. If analytics are not configured, nothing is collected at all.
        </p>

        <h2 className="mt-8 text-xl font-semibold tracking-tight">What we never collect</h2>
        <p className="text-[15px] leading-relaxed text-muted">
          No accounts, no passwords, no advertising identifiers, no cross-site trackers. We do not sell, rent, or share
          visitor data, because we do not collect any worth sharing.
        </p>

        <h2 className="mt-8 text-xl font-semibold tracking-tight">Forms</h2>
        <p className="text-[15px] leading-relaxed text-muted">
          The bot submission and newsletter forms send only what you type. Newsletter emails are stored with the
          newsletter provider for the sole purpose of sending the weekly email; every email includes an unsubscribe
          link. Submission content (bot name, link, description) becomes part of the public directory when approved.
        </p>

        <h2 className="mt-8 text-xl font-semibold tracking-tight">Third parties</h2>
        <p className="text-[15px] leading-relaxed text-muted">
          Open in Grok links hand you off to xAI’s platform; what xAI collects there is governed by xAI’s own
          privacy policy. External news and source links (X posts, press coverage) are governed by those platforms.
          Sponsored links are regular links to the sponsor’s own site and are always labeled.
        </p>

        <h2 className="mt-8 text-xl font-semibold tracking-tight">Contact and changes</h2>
        <p className="text-[15px] leading-relaxed text-muted">
          Questions or deletion requests: {SITE.email}. If this policy changes materially, the change gets a date and a
          plain-English summary at the top of this page.
        </p>
        <p className="text-[15px] leading-relaxed text-muted">{DISCLAIMER}</p>
      </div>
    </div>
  );
}
