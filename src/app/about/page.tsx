import type { Metadata } from "next";
import Link from "next/link";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { pageMetadata, breadcrumbsJsonLd } from "@/lib/seo";
import { SITE, DISCLAIMER } from "@/data/site";
import { stats } from "@/data/bots";

export const metadata: Metadata = pageMetadata({
  title: "About GrokBot HQ - Independent, Hand-Reviewed, Free",
  description:
    "Who runs GrokBot HQ, how the review process works, why independence matters, and how to contact us. The directory of Grok bots built for users first.",
  path: "/about",
});

export default function AboutPage() {
  return (
    <div className="container-x max-w-3xl py-12">
      <JsonLd data={[breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "About", path: "/about" }])]} />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "About" }]} />
      <SectionHeader
        kicker="About"
        title="One place for Grok bot users"
        description={`GrokBot HQ exists because the Grok bot ecosystem grew faster than anyone's ability to browse it. ${stats.bots} bots in, the thesis holds: human review beats algorithmic feeds.`}
      />

      <div className="prose-block">
        <h2 className="text-xl font-semibold tracking-tight">Why this site exists</h2>
        <p className="text-[15px] leading-relaxed text-muted">
          Grok bots are tiny, useful, and scattered. The good ones spread by word of mouth and die in reply threads; the
          bad ones wear the same clothes. We started GrokBot HQ as the missing layer between builders and users: a
          single place to find a bot for the job you have right now, with enough context to know whether it’s worth
          opening.
        </p>

        <h2 className="mt-8 text-xl font-semibold tracking-tight">How reviews work</h2>
        <p className="text-[15px] leading-relaxed text-muted">
          Every submission is opened by a human who tests it against three real prompts: a typical case, a messy case,
          and an out-of-scope case. We check that the description matches reality and that the bot refuses cleanly when
          it should. Roughly 8 in 10 submissions pass. Rejections come with a reason, because the ecosystem gets better
          when builders understand the bar.
        </p>

        <h2 className="mt-8 text-xl font-semibold tracking-tight">Independence and funding</h2>
        <p className="text-[15px] leading-relaxed text-muted">
          Browsing is free, listings are free, and rankings are never for sale. Sponsored placements are clearly labeled,
          and sponsors pass the same review as everyone else. If those two sentences ever stop being true, this section
          is where we’ll say so.
        </p>

        <h2 className="mt-8 text-xl font-semibold tracking-tight">Trademarks and affiliation</h2>
        <p className="text-[15px] leading-relaxed text-muted">{DISCLAIMER}</p>

        <h2 className="mt-8 text-xl font-semibold tracking-tight">Contact</h2>
        <p className="text-[15px] leading-relaxed text-muted">
          General: <a href={`mailto:${SITE.email}`} className="text-accent hover:underline">{SITE.email}</a>, Submissions:{" "}
          <a href={`mailto:${SITE.submitEmail}`} className="text-accent hover:underline">{SITE.submitEmail}</a>, On X:{" "}
          <a href={`https://x.com/${SITE.twitter.replace("@", "")}`} target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">
            {SITE.twitter}
          </a>
        </p>
      </div>

      <div className="mt-10 flex flex-wrap gap-3">
        <Link href="/bots" className="btn btn-accent">Browse the directory</Link>
        <Link href="/submit" className="btn btn-ghost">Submit a bot</Link>
      </div>
    </div>
  );
}
