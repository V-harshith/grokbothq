<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->

# GrokBot Hub — agent management runbook

You (an AI agent with GitHub access to `V-harshith/grokbothq`) are a maintainer of this directory. This file is your operating manual. When unsure, re-read it rather than improvising.

## What this repo is

A fully static Next.js site (directory of Grok bots) that **auto-deploys on every push to `main`** (Vercel). All site content lives in `content/*.json`. The code in `src/` is a stable engine that reads that JSON — **you never need to touch `src/` to manage the site.**

## Hard rules

1. **Content changes = `content/*.json` only.** Never edit `src/`, `scripts/`, or `.github/` for content operations.
2. **Work through pull requests by default.** Commit directly to `main` only for trivial fixes the owner explicitly requested. Every PR is automatically build-checked (`.github/workflows/ci.yml`); only merge when it's green.
3. **Never commit secrets** (API keys, tokens). Env vars live in Vercel/GitHub settings, not the repo.
4. **Never weaken validation** (`scripts/parse-submission.mjs`) or mass-approve unreviewed submissions. The site's only asset is trust.
5. Every push to `main` deploys to production. Check `npm run build` passes before pushing anything.

## Submission review SOP (issues labeled `bot-submission`)

New submissions arrive as GitHub issues (form template) and are auto-processed by the `Process bot submission` workflow: it validates (real `https://x.ai/bot/…` link, category whitelist, spam blocklist, duplicates), appends to `content/bots.json`, and opens a PR closing the issue.

Your job when a submission PR appears:
1. Open the bot's `url` from the PR diff and confirm the bot exists and its pitch matches reality (or inspect the issue thread).
2. If good → merge the PR (squash). The site redeploys automatically and the issue closes.
3. If bad → comment the reason on the issue, close the PR (don't merge), and close the issue.

To manually run validation on a candidate, simulate the workflow locally with the issue body in `ISSUE_BODY` env var and `node scripts/parse-submission.mjs`.

## Content systems (all files)

| File | What it drives | Notes |
|---|---|---|
| `content/bots.json` | The directory (233 real bots) | See schema below. `installs`, `integrations`, `source`, `hue` are optional enrichment. |
| `content/combos.json` | /groups bot pipelines | `botSlugs` MUST exist in bots.json - dead slugs render empty cards. |
| `content/news.json` | /news feed + RSS | Newest first; one-line summaries in our words; dedupe by URL; keep ~15 newest. |
| `content/ads.json` | All ad units | `active`+title/desc/cta/url = the in-grid and header units; `rails[]` = the desktop side rail (up to 2). |
| `content/metrics.json` | Install/click counters | Written by weekly cron from Umami - do not hand-edit unless correcting. |
| `content/categories.json`, `guides.json`, `compare.json`, `faqs.json` | Long-form pages | Hand-written editorial; update sparingly and well. |

Derived automatically from those files: /new, /use-cases, /integrations (+ per-tool pages), /news, RSS, sitemap, llms.txt, and the JSON API (/api/v1/index.json). Nothing else needs updating after a content change.

## Content schema cheatsheet (`content/bots.json`)

```jsonc
{
  "slug": "unique-kebab-case",          // auto-dedupes
  "name": "Bot Name",
  "builder": { "name": "Display", "x": "handle-without-@" },
  "tagline": "One-sentence hook",
  "description": "2-3 sentences",
  "category": "assistants|engineering|research|money|sales|creative|life|productivity",
  "instructions": "persona excerpt shown on the detail page",
  "features": ["..."], "bestFor": ["..."],
  "url": "https://x.ai/bot/<id>",
  "addedAt": "YYYY-MM-DD",
  "status": "published"                  // "pending" = hidden from the site
  "featured": true,                      // optional; only with owner approval
  "featuredUntil": "YYYY-MM-DD"          // optional; auto-expires via weekly ops
}
```

## Sourcing real bots and use cases

Follow **HERMES-SCRAPING.md** for the full data pipeline: sources, verification (every x.ai/bot link must be opened and confirmed live), JSON schema, and the PR workflow. Never list an unverified bot link.

## Common tasks (exact commands)

```bash
# Feature a bot for 30 days (only when the owner says so — this is a paid slot)
#   edit content/bots.json: set "featured": true, "featuredUntil": "<today+30d>"
# Delist a bad bot (never delete — keep the record)
#   set "status": "pending" in its entry
# Verify everything still builds
npm run build
# Run a sponsor (edit content/ads.json first: active, title, description, cta, url)
#   (no command needed - merging to main deploys it)
# Trigger the weekly ops pipeline manually
gh workflow run "Weekly ops" -R V-harshith/grokbothq
# Check repo automation state
gh run list -R V-harshith/grokbothq --limit 5
```

After any `content/*.json` change and build: stats, `/new`, sitemap, llms.txt, canonical dates regenerate automatically. Nothing else needs updating.

## Definition of done

`npm run build` exits 0, and these routes return 200 locally (`npm start`): `/`, `/bots`, `/news`, `/use-cases`, `/integrations`, `/groups`, plus one bot detail page for anything you changed. `node scripts/route-sweep.mjs http://localhost:3000` after `npm start` checks every sitemap URL. Report what you changed, the deploy it triggered, and anything you deliberately did not do.
