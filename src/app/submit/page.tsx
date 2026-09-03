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
  keywords: ["submit a grok bot", "get your grok bot listed", "grok bot submission", "free grok bot listing"],
});

export default function SubmitPage() {
  return (
    <div className="container-x max-w-3xl py-12">
      <JsonLd data={[breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Submit", path: "/submit" }])]} />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Submit" }]} />
      <SectionHeader
        kicker="Free listing"
        title="List your Grok bot"
        description="You built something useful. Put it in front of people searching for exactly that. Every submission is opened and tested against real prompts - reviews take about 48 hours."
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

      <section className="mt-12">
        <h2 className="text-xl font-semibold tracking-tight">What happens to your submission</h2>
        <ol className="mt-4 space-y-4">
          {[
            {
              name: "It lands in the review queue",
              text: "Your listing becomes a tracked ticket the moment you submit - nothing gets lost in a DM.",
            },
            {
              name: "We open and test the bot",
              text: "A human runs it against three real prompts: a typical case, a messy case, and something out of scope. About 48 hours.",
            },
            {
              name: "It goes live - or you get the reason",
              text: "Approved listings publish automatically with the site's next update. Rejections come with the exact reason, and resubmitting is welcome.",
            },
          ].map((step, i) => (
            <li key={step.name} className="card flex gap-4 p-5">
              <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-accent font-mono text-sm font-bold text-accent-foreground" aria-hidden>
                {i + 1}
              </span>
              <div>
                <h3 className="font-semibold">{step.name}</h3>
                <p className="mt-1 text-sm leading-relaxed text-muted">{step.text}</p>
              </div>
            </li>
          ))}
        </ol>
        <p className="mt-4 text-sm text-muted">
          Where the review record lives: submissions through the site open a GitHub issue and, once approved, a pull
          request you can read - the whole history is public. Email submissions get a reply from a human.
        </p>
      </section>
    </div>
  );
}
