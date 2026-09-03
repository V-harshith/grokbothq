# GrokBot HQ

[![CI](https://github.com/V-harshith/grokbothq/actions/workflows/ci.yml/badge.svg)](https://github.com/V-harshith/grokbothq/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Content: CC BY 4.0](https://img.shields.io/badge/content-CC_BY_4.0-green.svg)](LICENSE-CONTENT.md)

**The independent, hand-reviewed directory of Grok bots** — live at [grokbothq.xyz](https://grokbothq.xyz).

One place for Grok bot users to find, combine, and master bots on xAI's Grok platform. Every listing is opened and tested by a human before publication.

## What's inside

- **Directory** — 230+ Grok bots, filterable by category, with install counts and source links
- **Bot combos** — tested sets of bots that work together in pipelines
- **Guides** — how to create, write instructions for, chain, and monetize Grok bots
- **Comparisons** — Grok bots vs Custom GPTs, Claude Skills, Gemini Gems, and agent frameworks
- **News & use cases** — curated ecosystem news and real-world usage from X
- **Stats** — original, citable directory statistics
- **Submission pipeline** — visitors submit via GitHub issue template → an Action validates (URL pattern, category, spam blocklist, duplicates) → a pull request adds the bot to the data file → merge deploys

The site is fully static and data-driven: **all content lives in `content/*.json`**, and every page (sitemap, RSS, llms.txt, JSON API, counts) regenerates on every build. No database, no backend.

## Tech stack

Next.js 16 (App Router, static rendering) · React 19 · Tailwind CSS 4 · TypeScript · Vercel Analytics

## Local development

```bash
npm install
npm run dev     # http://localhost:3000
npm run build   # production build
npm run lint    # eslint
```

Edit anything in `content/*.json` and the dev server picks it up.

## Project structure

```
content/*.json      All content: bots, categories, combos, guides, comparisons, FAQs, news, ads
src/data/*.ts       Typed loaders over the JSON (filters pending status, featured expiry)
src/app/            Routes: /, /bots (+ detail + categories), /groups, /guides, /compare,
                    /new, /news, /stats, /use-cases, /integrations, /faq, /submit,
                    /featured, /about, /privacy, /terms
src/lib/seo.ts      Metadata factory + JSON-LD builders (WebSite, Organization, FAQPage,
                    Article, ItemList, SoftwareApplication, BreadcrumbList)
src/app/api/v1/     JSON index of the full directory (for bots/LLMs)
scripts/*.mjs       CI helpers: submission parsing, featured expiry, metrics pull, IndexNow ping
.github/workflows/  ci.yml (build check) · process-submission.yml (issue → PR) · daily-ops.yml
```

### Bot entry schema (`content/bots.json`)

```json
{
  "slug": "my-bot",
  "name": "My Bot",
  "builder": { "name": "", "x": "" },
  "tagline": "One-line summary",
  "description": "What it does, in a sentence or two.",
  "category": "productivity",
  "features": ["Connects with Slack"],
  "integrations": ["slack"],
  "installs": 12,
  "url": "https://x.ai/bot/…",
  "addedAt": "2026-09-01",
  "status": "published",
  "source": "https://x.com/…"
}
```

## Submitting a bot

Open a [bot submission issue](https://github.com/V-harshith/grokbothq/issues/new?template=bot-submission.yml) (or use [the site's submit page](https://grokbothq.xyz/submit)). Rules baked into the validator: the link must be an `https://x.ai/bot/…` URL, the pitch is 10–280 characters, no external URLs in the pitch, no duplicates, and a spam blocklist (crypto, casino, SEO services, …). Rejections close the issue with the reason; resubmission is welcome.

## Contributing

Contributions are welcome — content fixes, new features, and bug reports alike. See [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md). Every PR must build cleanly (CI enforces this).

## License

- **Code** — [MIT](LICENSE). You may use, modify, and redistribute the engine, including commercially. Attribution appreciated but not required.
- **Content** (`content/*.json` + editorial prose) — [CC BY 4.0](LICENSE-CONTENT.md). Quote or republish freely **with attribution**: *Source: GrokBot HQ (https://grokbothq.xyz)*.

## Trademark notice

"Grok" is a trademark of xAI. GrokBot HQ is an independent third-party directory (nominative use) and is not affiliated with, endorsed by, or sponsored by xAI.
