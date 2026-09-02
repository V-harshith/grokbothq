import type { Metadata } from "next";
import { SITE } from "@/data/site";
import type { Bot } from "@/data/bots";

export function absUrl(path = "/"): string {
  const base = SITE.url.replace(/\/$/, "");
  return path.startsWith("http") ? path : `${base}${path.startsWith("/") ? path : `/${path}`}`;
}

type PageMetaInput = {
  title: string;
  description: string;
  path: string;
  type?: "website" | "article";
  publishedTime?: string;
  tags?: string[];
};

/** Standard metadata block: canonical, OG, Twitter. OG images come from app/opengraph-image. */
export function pageMetadata({ title, description, path, type = "website", publishedTime, tags }: PageMetaInput): Metadata {
  const url = absUrl(path);
  return {
    title,
    description,
    alternates: { canonical: url },
    openGraph: {
      title,
      description,
      url,
      siteName: SITE.name,
      type,
      locale: SITE.locale,
      ...(publishedTime ? { publishedTime } : {}),
      ...(tags ? { tags } : {}),
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      site: SITE.twitter,
    },
  };
}

/* ---------- JSON-LD builders ---------- */

export function websiteJsonLd() {
  return {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: SITE.name,
    alternateName: "GrokBot Directory",
    url: absUrl("/"),
    description: SITE.description,
    inLanguage: "en",
    publisher: { "@type": "Organization", name: SITE.name, url: absUrl("/") },
    potentialAction: {
      "@type": "SearchAction",
      target: { "@type": "EntryPoint", urlTemplate: `${absUrl("/bots")}?q={search_term_string}` },
      "query-input": "required name=search_term_string",
    },
  };
}

export function organizationJsonLd() {
  return {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: SITE.name,
    url: absUrl("/"),
    logo: absUrl("/logo.svg"),
    description: SITE.description,
    foundingDate: SITE.founded,
    email: SITE.email,
    sameAs: [`https://x.com/${SITE.twitter.replace("@", "")}`],
  };
}

export function breadcrumbsJsonLd(items: { name: string; path: string }[]) {
  return {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: items.map((item, i) => ({
      "@type": "ListItem",
      position: i + 1,
      name: item.name,
      item: absUrl(item.path),
    })),
  };
}

export function articleJsonLd(opts: { title: string; description: string; path: string; datePublished?: string; dateModified: string; author: string; tags?: string[] }) {
  return {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: opts.title,
    description: opts.description,
    url: absUrl(opts.path),
    mainEntityOfPage: absUrl(opts.path),
    datePublished: opts.datePublished ?? opts.dateModified,
    dateModified: opts.dateModified,
    author: { "@type": "Organization", name: opts.author, url: absUrl("/") },
    publisher: { "@type": "Organization", name: SITE.name, url: absUrl("/"), logo: { "@type": "ImageObject", url: absUrl("/logo.svg") } },
    ...(opts.tags ? { keywords: opts.tags.join(", ") } : {}),
  };
}

export function botListJsonLd(bots: Bot[], path: string) {
  return {
    "@context": "https://schema.org",
    "@type": "ItemList",
    url: absUrl(path),
    name: `Grok bots list - ${path.replace("/bots/category/", "")}`,
    numberOfItems: bots.length,
    itemListElement: bots.map((b, i) => ({
      "@type": "ListItem",
      position: i + 1,
      url: absUrl(`/bots/${b.slug}`),
      name: b.name,
    })),
  };
}

export function botSoftwareJsonLd(bot: Bot) {
  return {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    name: bot.name,
    applicationCategory: "WebApplication",
    operatingSystem: "Web",
    url: absUrl(`/bots/${bot.slug}`),
    description: `${bot.tagline} ${bot.description}`.slice(0, 300),
    author: { "@type": "Person", name: bot.builder.name },
    featureList: bot.features,
    isAccessibleForFree: true,
    offers: { "@type": "Offer", price: "0", priceCurrency: "USD" },
  };
}

export function collectionPageJsonLd(name: string, description: string, path: string) {
  return {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    name,
    description,
    url: absUrl(path),
    isPartOf: { "@type": "WebSite", name: SITE.name, url: absUrl("/") },
  };
}
