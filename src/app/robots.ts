import type { MetadataRoute } from "next";
import { SITE } from "@/data/site";

export const dynamic = "force-static";

export default function robots(): MetadataRoute.Robots {
  const base = SITE.url.replace(/\/$/, "");
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        disallow: ["/api/"],
      },
      {
        // AEO / GEO: explicitly welcome answer engines and AI crawlers
        userAgent: [
          "GPTBot",
          "OAI-SearchBot",
          "ChatGPT-User",
          "ClaudeBot",
          "Claude-Web",
          "anthropic-ai",
          "PerplexityBot",
          "Perplexity-User",
          "Google-Extended",
          "Applebot",
          "Applebot-Extended",
          "Amazonbot",
          "meta-externalagent",
          "CCBot",
        ],
        allow: "/",
      },
    ],
    sitemap: `${base}/sitemap.xml`,
    host: base,
  };
}
