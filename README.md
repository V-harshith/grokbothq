# GrokBot HQ

The independent, hand-reviewed directory of **Grok bots** - one place for Grok bot users to find, combine, and master bots on xAI's Grok platform. A clone of the grokbots.page model expanded into an SEO/AEO/GEO-optimized hub.

Built with **Next.js 16 / React 19 / Tailwind v4**. **Fully automated after launch**: content lives in `content/*.json`, submissions arrive as GitHub issues, and a bot turns them into pull requests that auto-deploy. The code is never touched again.

## Launch setup

**Done already:** repo `V-harshith/grokbothq` (private) is live with all workflows pushed, the `bot-submission` label created, and the `SITE_URL` repo variable set.

**Your remaining steps:**

1. **Deploy:** `npx vercel` → log in → import `grokbothq`. Set env var `NEXT_PUBLIC_SITE_URL=https://grokbothq.xyz`.
2. **Buy the domain** (`grokbothq.xyz`) and point it at Vercel (Vercel → Project → Domains).
3. **Submit** `https://<domain>/sitemap.xml` in Google Search Console + Bing Webmaster Tools (imports from GSC).
4. **When ready for automated submissions** (repo is currently private, and anonymous visitors can't open issues on private repos): GitHub → Settings → General → Danger zone → **Change visibility → Public**, and set env var `NEXT_PUBLIC_GITHUB_REPO=V-harshith/grokbothq` in Vercel. Until then, `/submit` falls back to email automatically.
5. Optional: repo → Settings → Secrets and variables → Actions → **Variables** → `AUTO_MERGE=true` for zero-touch publishing (default is one-click PR merge, which keeps "hand-reviewed" honest).

**Done.** From here on the site runs itself:

```
Visitor submits bot (GitHub issue template, spam-screened client-side)
        ↓
GitHub Action validates: URL pattern, category, spam blocklist, duplicates
        ↓ valid
Pull request with the bot appended to content/bots.json (+ comment on the issue)
        ↓ merged (1 click from your phone, or fully automatic - see below)
Vercel auto-deploys → new bot page, updated /new, sitemap, llms.txt, stats, OG image
        ↓
Weekly action: featured placements auto-expire · IndexNow re-crawl ping · build health check
```

### Full-auto mode (optional)

By default each submission opens a **pull request** - merge it with one click and the bot is live (this keeps the "hand-reviewed" claim honest). If you want zero involvement: repo **Settings → Secrets and variables → Actions → Variables → New variable** → `AUTO_MERGE` = `true`. Valid submissions then publish automatically; invalid ones are closed with a reason and can resubmit.

### Editing content without touching code

- **GitHub web editor**: open `content/bots.json`, click ✏️, edit, commit to `main` → auto-deploys. This is "touching GitHub," not the code.
- **Featured slots**: add `"featured": true, "featuredUntil": "2026-09-27"` to any bot - the weekly action expires it automatically. That's the whole featured-placement business loop.
- **Everything regenerates on every build**: counts, `/new`, sitemap, `llms.txt`, canonical dates. No manual steps exist.

## Architecture

| Piece | What it does |
|---|---|
| `content/*.json` | **All content** - bots, categories, combos, guides, comparisons, FAQs. The only thing that ever changes after launch. |
| `src/data/*.ts` | Typed loaders over the JSON (filtering `status: "pending"`, featured expiry). Stable API - pages never change. |
| `src/app/` | Routes: `/`, `/bots` + detail + 8 category pages, `/groups` (6 combos), `/guides` (8), `/compare` (4), `/new`, `/faq`, `/submit`, `/featured`, `/about` |
| `src/lib/seo.ts` | Metadata factory + JSON-LD builders (WebSite, Organization, FAQPage, HowTo, Article, ItemList, SoftwareApplication, BreadcrumbList) |
| `.github/workflows/process-submission.yml` | Issue → validate → PR → optional auto-merge |
| `.github/workflows/weekly-ops.yml` | Featured expiry commit, IndexNow ping, build check (Mondays 04:00 UTC) |
| `.github/workflows/ci.yml` | Every PR (incl. automated ones) must build cleanly |
| `scripts/*.mjs` | CI helpers: `parse-submission`, `expire-featured`, `ping-indexnow` |

## Submission pipeline rules

Baked into `scripts/parse-submission.mjs`: link must be `https://x.ai/bot/…`, valid category, pitch 10–280 chars, no external URLs anywhere, spam blocklist (crypto/casino/SEO-services/etc.), duplicate-URL rejection, auto-slug with dedupe. Rejections close the issue with the reason; resubmission is welcome.

## Domain plan (DNS-checked 2026-08-30)

Taken/parked: `grokbot.xyz`, `grokbots.xyz`, and all the obvious `.com`s. **Available:**

| Domain | First year | Renewal | Verdict |
|---|---|---|---|
| **grokbothq.xyz** ✅ current default | ~$1–3 | ~$10–13/yr | Best cheap start; brand match |
| grokbot.lol / grokbots.lol | ~$2–6 | ~$20–28/yr | Fun, but pricey renewals + weakens directory trust |
| grokbothq.xyz | ~$10 | ~$10/yr | The trust upgrade when revenue justifies it |

Buy at Porkbun / Cloudflare Registrar / Namecheap. `.xyz` is a normal ICANN gTLD - Google treats it like `.com`; its spam-fleet reputation only matters for spammy sites, and this is a content-rich directory. **Swap domains any time without touching code**: point DNS at Vercel, set `NEXT_PUBLIC_SITE_URL`, redeploy. Set auto-renew with a funded card - the one thing automation can't do.

> ⚠️ **Trademark note:** "Grok" is xAI's trademark. The site is positioned as an independent third-party directory (nominative use - same as grokbots.page), with disclaimers in the footer, about page, and metadata. Don't copy xAI's logo or imply endorsement. Rebranding later is a one-file change (`src/data/site.ts` + `content/site.json`).

## SEO / AEO / GEO (all built in)

**SEO:** unique title/description/canonical per page · 67-URL sitemap with changefreqs · semantic HTML · hub-and-spoke internal linking · static rendering · `max-image-preview:large`.
**AEO:** FAQPage/HowTo/Article/ItemList/SoftwareApplication/BreadcrumbList JSON-LD · "Quick answer" blocks on every guide · question-formatted headings · crawlable FAQ accordions.
**GEO:** `llms.txt` + `llms-full.txt` content feeds · robots.txt explicitly allows GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Applebot, CCBot… · quotable verdicts and stats · comparison tables in the format LLMs cite.

## Local development

```bash
npm install
npm run dev     # http://localhost:3000
npm run build   # production build
```

Edit `content/*.json` and the dev server picks it up. The repo's automation means local dev is only needed for engine changes - which, per the plan, you'll never make.

## Backlinks playbook (first 60 days)

**Tier 1 - launch week:** publish the repo public + an `awesome-grok-bots` list repo linking the hub (GitHub do-follow) · Product Hunt · Show HN · X launch thread with bot demos · 50+ AI tool directories (StartupBase, Uneed, Peerlist, ToolPilot…).

**Tier 2 - weeks 2–6:** weekly "New this week" posts (builders link back - they want discovery) · Dev.to/Medium/Hashnode cross-posts with canonical URLs · r/Grok and r/SideProject as genuine comments · "Featured on GrokBot HQ" badge for builders' sites · a monthly "state of Grok bots" stats graphic.

**Tier 3 - ongoing:** builder outreach ("you're listed - grab the badge") · HARO/Qwoted as ecosystem source · resource-page + broken-link outreach to AI roundups · a quarterly data study (linkable research).

Keep anchors natural (brand, "grok bot directory", "hand-reviewed grok bots", bare URL) - especially important on a trademark-adjacent brand.

## Upgrade path (if you ever outgrow this)

Static + rebuilds updates the site on every merge (usually seconds after approval; worst case a few minutes for CI). If you ever want truly instant writes, the move is Supabase + ISR with on-demand revalidation - the data layer (`src/data/*.ts`) is the only thing that changes. Not needed until submissions outpace a few per day.

## Analytics, newsletter, ad slot, and contact

**Analytics (Umami):** set `NEXT_PUBLIC_UMAMI_URL` (your `/script.js` URL) and `NEXT_PUBLIC_UMAMI_WEBSITE_ID` in Vercel. The script loads only when both are set; nothing else changes. Umami is cookieless, so no consent banner needed for most jurisdictions.

**Newsletter:** set `NEXT_PUBLIC_NEWSLETTER_ENDPOINT` to a form endpoint (Buttondown, Loops, Formspree) and the homepage form POSTs emails there. Unset, it falls back to a compose-email flow. Wire the endpoint once; the section ships.

**Ad slot:** one slot exists on the homepage (below the hero) and at the bottom of `/bots`. It is fully data-driven from `content/ads.json`: set `"active": true` and fill `title` / `description` / `cta` / `url` to run a sponsor; set `"active": false` to fall back to the quiet house ad that links to `/featured` (the "get featured" pipeline fills this slot with paying sponsors). The slot is always labeled. One sponsor per slot, never more.

**Contact:** the footer carries `hello@harshithOG.xyz` (mailto) and the `@harshithOG` X handle; the About page has the same. To use a different X handle, change `SITE.twitter` in `src/data/site.ts` - one line, it propagates everywhere.
