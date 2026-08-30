export const SITE = {
  name: "GrokBot HQ",
  shortName: "GrokBot HQ",
  domain: "grokbothq.xyz",
  url: process.env.NEXT_PUBLIC_SITE_URL ?? "https://grokbothq.xyz",
  tagline: "Find a Grok bot worth opening",
  description:
    "GrokBot HQ is the independent, hand-reviewed directory of Grok bots. Browse bots by category, open any bot in Grok with one click, learn bot combos, and master Grok bot instructions with step-by-step guides.",
  locale: "en_US",
  twitter: "@grokbothq",
  email: "hello@grokbothq.xyz",
  submitEmail: "submit@grokbothq.xyz",
  founder: "The GrokBot HQ team",
  founded: "2026",
  /** Recomputed at every build - stays fresh automatically as content updates flow in. */
  lastUpdated: new Date().toISOString().slice(0, 10),
  /** GitHub repo ("owner/repo") that receives bot submissions as issues. Enables the automated submission pipeline. */
  githubRepo: process.env.NEXT_PUBLIC_GITHUB_REPO ?? "",
  /** xAI's bot builder - where every listed bot opens */
  builderUrl: "https://x.ai/bot",
  xaiUrl: "https://x.ai",
} as const;

export const DISCLAIMER =
  "GrokBot HQ is an independent directory maintained by fans of the Grok bot ecosystem. It is not affiliated with, endorsed by, or sponsored by xAI. Grok is a trademark of xAI; references are for identification only.";
