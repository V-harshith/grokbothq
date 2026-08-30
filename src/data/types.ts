export type Bot = {
  slug: string;
  name: string;
  builder: { name: string; x: string };
  tagline: string;
  /** 2-3 sentence description used on the detail page + in LLM feeds */
  description: string;
  category: string;
  /** persona/instruction excerpt shown on the detail page */
  instructions?: string;
  features?: string[];
  bestFor?: string[];
  /** x.ai/bot deep link */
  url: string;
  addedAt: string;
  featured?: boolean;
  trending?: boolean;
  /** ISO date - featured placement auto-expires after this date */
  featuredUntil?: string;
  /** X post where this bot was introduced or used - powers the use-cases hub */
  source?: string;
  /** Install count from the source directory, when published */
  installs?: number;
};

export type Category = {
  slug: string;
  name: string;
  /** one-liner shown on cards and tabs */
  short: string;
  /** SEO intro paragraph for the category landing page */
  intro: string;
  faqs: { q: string; a: string }[];
};

export type Combo = {
  slug: string;
  name: string;
  emoji: string;
  /** one-line hook */
  tagline: string;
  description: string;
  botSlugs: string[];
  /** how the bots work together, in order */
  steps: { name: string; text: string }[];
  bestFor: string[];
  addedAt: string;
};

export type GuideSection = {
  heading: string;
  body?: string[];
  list?: string[];
  /** if present, this guide gets HowTo schema */
  steps?: { name: string; text: string }[];
};

export type Guide = {
  slug: string;
  title: string;
  /** SEO title (~55 chars) */
  seoTitle: string;
  description: string;
  readingMinutes: number;
  updatedAt: string;
  tags: string[];
  intro: string;
  sections: GuideSection[];
  /** short TL;DR answer for answer engines */
  quickAnswer: string;
};

export type ComparePage = {
  slug: string;
  title: string;
  seoTitle: string;
  description: string;
  other: string;
  updatedAt: string;
  verdict: {
    summary: string;
    chooseGrokBots: string[];
    chooseOther: string[];
  };
  rows: { aspect: string; grok: string; other: string }[];
  sections: { heading: string; body: string[] }[];
  faqs: { q: string; a: string }[];
};

export type Faq = { q: string; a: string };
