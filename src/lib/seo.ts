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
  keywords?: string[];
};

/** Every page ships these; page-specific keywords merge on top. */
const BASE_KEYWORDS = ["grok bots", "grok bot directory", "grokbot hq"];

function mergeKeywords(...groups: (string[] | undefined)[]): string[] {
  return [...new Set(groups.flat().filter((k): k is string => Boolean(k)))];
}

/** Standard metadata block: canonical, keywords, OG, Twitter. OG images come from app/opengraph-image. */
export function pageMetadata({ title, description, path, type = "website", publishedTime, tags, keywords }: PageMetaInput): Metadata {
  const url = absUrl(path);
  const allKeywords = mergeKeywords(keywords, tags, BASE_KEYWORDS);
  return {
    title,
    description,
    keywords: allKeywords,
    alternates: { canonical: url },
    openGraph: {
      title,
      description,
      url,
      siteName: SITE.name,
      type,
      locale: SITE.locale,
      ...(publishedTime ? { publishedTime } : {}),
      tags: allKeywords,
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      site: SITE.twitter,
    },
  };
}

/* ---------- fitting text into meta tags ---------- */
// Bot data is long-form (taglines run past 200 characters), and it used to reach the meta tags raw,
// so Google cut it mid-word: "...helps with life and work rhythm includ Open Jarvis in Grok with one
// click." Every string that lands in a <title> or a description goes through these instead.

/** Trim to <= max characters on a word boundary. Never cuts a word, never leaves dangling punctuation. */
export function clampText(input: string, max: number): string {
  const text = (input ?? "").replace(/\s+/g, " ").trim();
  if (text.length <= max) return text;
  const head = text.slice(0, max + 1);
  const space = head.lastIndexOf(" ");
  const cut = space > 0 ? head.slice(0, space) : head.slice(0, max);
  return cut.replace(/[\s,;:.!?&/|–—-]+$/u, "").trim();
}

/**
 * Trim to <= max characters, preferring the last complete sentence in the window. Falls back to a
 * word boundary, and only cuts a word when the text has no spaces at all.
 */
export function clampSentence(input: string, max: number): string {
  const text = (input ?? "").replace(/\s+/g, " ").trim();
  if (text.length <= max) return text;
  const window = text.slice(0, max + 1);
  const ends = [...window.matchAll(/[.!?](?=\s|$)/g)];
  const last = ends.length > 0 ? ends[ends.length - 1] : null;
  // Only accept a sentence end in the second half of the window; earlier than that loses too much.
  if (last?.index !== undefined && last.index >= max * 0.5) return window.slice(0, last.index + 1).trim();
  return clampText(text, max);
}

/**
 * Body + call to action, fitted to a snippet.
 *
 * The body is never cut mid-sentence to make room for the CTA: "…learns the week, and helps with
 * life Open Jarvis in Grok with one click." is the bug this replaced. So the CTA is kept only when
 * the whole description fits beside it; otherwise the description gets the full window and ends on a
 * sentence.
 */
export function composeDescription(body: string, cta = "", max = 155): string {
  const clean = (body ?? "").replace(/\s+/g, " ").trim();
  const suffix = (cta ?? "").replace(/\s+/g, " ").trim();
  if (!suffix) return clampSentence(clean, max);
  if (clean.length + suffix.length + 1 <= max) return `${clean} ${suffix}`;
  const withCta = `${clampSentence(clean, max - suffix.length - 1).trim()} ${suffix}`;
  // Keep the CTA only when the body still ends on a sentence — otherwise it reads as truncated text.
  if (withCta.length <= max && /[.!?]$/.test(withCta.slice(0, withCta.length - suffix.length - 1).trim())) {
    return withCta;
  }
  return clampSentence(clean, max);
}

/**
 * Title that keeps the whole name. Tries `name - descriptor`, then `name - fallback`, then the bare
 * name, and only clamps the name itself as a last resort — a half-name is worse than no descriptor.
 */
export function composeTitle(name: string, descriptor = "", max = 62, fallback = ""): string {
  const primary = (name ?? "").replace(/\s+/g, " ").trim();
  const withDescriptor = (d: string) => `${primary} - ${d}`;
  const desc = (descriptor ?? "").replace(/\s+/g, " ").trim();
  const fb = (fallback ?? "").replace(/\s+/g, " ").trim();
  if (desc && withDescriptor(desc).length <= max) return withDescriptor(desc);
  if (fb && withDescriptor(fb).length <= max) return withDescriptor(fb);
  if (primary.length <= max) return primary;
  return clampText(primary, max);
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
    sameAs: [`https://x.com/${SITE.twitter.replace("@", "")}`, SITE.githubUrl],
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

/** FAQPage stays valuable for AI citation even though Google retired its rich-result display. */
export function faqJsonLd(faqs: { q: string; a: string }[], opts?: { dateModified?: string }) {
  return {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    ...(opts?.dateModified ? { datePublished: opts.dateModified, dateModified: opts.dateModified } : {}),
    mainEntity: faqs.map((f) => ({
      "@type": "Question",
      name: f.q,
      acceptedAnswer: { "@type": "Answer", text: f.a },
    })),
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
    description: clampText(`${bot.tagline} ${bot.description}`, 300),
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
