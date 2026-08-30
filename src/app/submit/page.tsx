import type { Metadata } from "next";
import Link from "next/link";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { SubmitForm } from "./submit-form";
import { pageMetadata, breadcrumbsJsonLd } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: "Submit Your Grok Bot - Free Listing, Hand-Reviewed",
  description:
    "Get your Grok bot in front of people searching for it. Submit to GrokBot HQ for a free, hand-reviewed listing within 48 hours - or apply for a featured launch slot.",
  path: "/submit",
});

export default function SubmitPage() {
  return (
    <div className="container-x max-w-3xl py-12">
      <JsonLd data={[breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Submit", path: "/submit" }])]} />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Submit" }]} />
      <SectionHeader
        kicker="Free listing"
        title="Submit your Grok bot"
        description="Reviews are done by humans: we open your bot, test it against three real prompts, and check the description matches reality. About 8 in 10 submissions make it in."
      />

      <SubmitForm />

      <section className="mt-12">
        <h2 className="text-lg font-semibold">What we look for</h2>
        <ul className="mt-3 space-y-2">
          {[
            "One job, done well - 'assistant that does everything' submissions get rejected.",
            "Instructions with explicit rules and a failure mode, not just a personality.",
            "The x.ai/bot link must open a working, published bot.",
            "Honest description - no feature claims the bot can't back up.",
            "Nothing that impersonates real people, asks for credentials, or breaks xAI's terms.",
          ].map((item) => (
            <li key={item.slice(0, 24)} className="flex items-start gap-2.5 text-sm leading-relaxed text-muted">
              <svg className="mt-1.5 shrink-0 text-accent" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
                <path d="M20 6 9 17l-5-5" />
              </svg>
              {item}
            </li>
          ))}
        </ul>
        <p className="mt-4 text-sm text-muted">
          Want the top slot instead?{" "}
          <Link href="/featured" className="text-accent hover:underline">
            See featured placements
          </Link>
          . Not sure if your bot is ready? Read{" "}
          <Link href="/guides/how-to-write-bot-instructions" className="text-accent hover:underline">
            How to Write Bot Instructions
          </Link>{" "}
          first.
        </p>
      </section>
    </div>
  );
}
