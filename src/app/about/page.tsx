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
  keywords: ["about grokbot hq", "independent grok bot directory", "hand-reviewed grok bots"],
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
        <h2 className="text-xl font-semibold tracking-tight">What is GrokBot HQ?</h2>
        <p className="text-[15px] leading-relaxed text-muted">
          GrokBot HQ is an independent, hand-reviewed directory of Grok bots: custom assistants built on xAI&apos;s Grok
          platform that anyone can open in one click at x.ai/bot. As of {new Date(SITE.lastUpdated).toLocaleDateString("en-US", { month: "long", year: "numeric" })} it
          lists {stats.bots} bots from {stats.builders} builders across {stats.categories} categories, each one opened and tested by a human
          before publication. Listings link to the bot, its builder, and the X post where it was introduced, and every
          page is served as plain HTML plus a JSON index so Grok bots themselves can read the directory. It is operated
          by the GrokBot HQ team and is not affiliated with xAI. Directory content is licensed CC BY 4.0
          with attribution.
        </p>

        <h2 className="mt-8 text-xl font-semibold tracking-tight">Why this site exists</h2>
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

        <h2 className="mt-8 text-xl font-semibold tracking-tight">Open source</h2>
        <p className="text-[15px] leading-relaxed text-muted">
          GrokBot HQ is an open-source project: the engine that powers this site lives on{" "}
          <a href={SITE.githubUrl} target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">GitHub</a>{" "}
          under the MIT license, and the directory data (every bot, guide, and comparison) is CC BY 4.0. Star the repo
          if the directory is useful, report bugs, or contribute a feature — the{" "}
          <a href={`${SITE.githubUrl}/blob/main/CONTRIBUTING.md`} target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">contributing guide</a>{" "}
          covers everything from content edits to local setup.
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
