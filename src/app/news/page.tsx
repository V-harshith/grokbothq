import type { Metadata } from "next";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { news } from "@/lib/news";
import { SITE } from "@/data/site";
import { pageMetadata, breadcrumbsJsonLd, collectionPageJsonLd, absUrl } from "@/lib/seo";

export const revalidate = 300; // pages refresh within 5 minutes of content changes

export const metadata: Metadata = pageMetadata({
  title: "Grok News - What's New in the Grok Bot Ecosystem",
  description:
    "The latest Grok and Grok Bot news, curated and summarized: launches, model releases, builder tools, and ecosystem moves - with links to the original sources.",
  path: "/news",
  keywords: ["grok news", "grok bot news", "grok ecosystem news", "xai grok updates"],
});

export default function NewsPage() {
  const items = [...news].sort((a, b) => b.date.localeCompare(a.date));

  const newsArticleLd = items.slice(0, 10).map((item) => ({
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    headline: item.title,
    datePublished: item.date,
    url: item.url,
    description: item.summary,
    publisher: { "@type": "Organization", name: SITE.name, url: absUrl("/") },
  }));

  return (
    <div className="container-x max-w-3xl py-12">
      <JsonLd
        data={[
          ...newsArticleLd,
          collectionPageJsonLd("Grok news", "Curated news from the Grok bot ecosystem", "/news"),
          breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "News", path: "/news" }]),
        ]}
      />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "News" }]} />
      <SectionHeader
        kicker="Ecosystem"
        title="Grok news, curated"
        description="Launches, model releases, and builder-tool moves - summarized in one line each, always linked to the original source."
      />

      <ol className="mt-4 divide-y divide-border">
        {items.map((item) => (
          <li key={item.url + item.date} className="py-6" data-reveal>
            <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1 text-xs text-muted">
              <span className="font-mono font-medium text-accent">{item.source}</span>
              <time dateTime={item.date}>
                {new Date(item.date).toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })}
              </time>
            </div>
            <h2 className="mt-2 text-xl font-semibold tracking-tight">
              <a href={item.url} target="_blank" rel="noopener noreferrer" className="hover:text-accent">
                {item.title}
              </a>
            </h2>
            <p className="mt-2 text-[15px] leading-relaxed text-muted">{item.summary}</p>
            <p className="mt-2 text-xs">
              <a href={item.url} target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">
                Read the original →
              </a>
            </p>
          </li>
        ))}
      </ol>

      <p className="mt-10 text-sm text-muted">
        Found Grok news we missed?{" "}
        <a href={`mailto:${SITE.email}?subject=${encodeURIComponent("News tip")}`} className="text-accent hover:underline">
          Send the link
        </a>
        . Items are added with a summary and always link back to the source.
      </p>
    </div>
  );
}
