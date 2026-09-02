import type { Metadata } from "next";
import Link from "next/link";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { FaqList } from "@/components/faq-list";
import { JsonLd } from "@/components/json-ld";
import { faqs } from "@/data/faqs";
import { pageMetadata, breadcrumbsJsonLd } from "@/lib/seo";

export const metadata: Metadata = pageMetadata({
  title: "Grok Bots FAQ - Every Question, Answered Plainly",
  description:
    "What are Grok bots, how do you open one, are they free and safe, how do you get listed, and what's the difference from Custom GPTs? The complete Grok bot FAQ.",
  path: "/faq",
});

export default function FaqPage() {
  return (
    <div className="container-x max-w-3xl py-12">
      <JsonLd data={[breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "FAQ", path: "/faq" }])]} />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "FAQ" }]} />
      <SectionHeader
        kicker="FAQ"
        title="Grok bot questions, answered plainly"
        description="Everything people ask us about Grok bots - no hedging, no fluff. If your question isn't here, email us and we'll answer it (and probably add it)."
      />
      <FaqList faqs={faqs} />
      <p className="mt-10 text-sm text-muted">
        Still stuck? The{" "}
        <Link href="/guides/what-are-grok-bots" className="text-accent hover:underline">
          complete beginner’s guide
        </Link>{" "}
        covers everything in depth.
      </p>
    </div>
  );
}
