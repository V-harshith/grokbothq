# grokbothq.xyz — SEO log

Repo-side record of what changed, why, what the baseline was, and when it is due to be re-checked.
It lives in the repo so a cold-start reader (human or agent, this machine or another) can tell a
decision from an accident without access to any agent's private state.

Audit of record: SEOO pack, 2026-10-02 — `grokbothq.xyz.md`, 11 ordered prescriptions.

## How to change this site

1. `content/*.json` is the content; `src/app/**` renders it. Nothing is hand-edited in the output.
2. `npm run build` — TypeScript plus prerender of every route.
3. `node scripts/route-sweep.mjs http://localhost:3000` — hits every sitemap URL, reports non-200s.
   Last run 2026-10-02: **2,779 pages, all 200**.
4. Push to `main` on `github.com/V-harshith/grokbothq`.
5. `node scripts/ping-indexnow.mjs` after a content change, so Bing/Yandex see the new pages.

**Do not run a build while the ops cron is writing `content/bots.json`.** It happened on 2026-10-02:
the file was rewritten mid-build, the prerendered set and the runtime map disagreed, and one listing
(`/bots/data`) returned 404 until a clean rebuild. Check the file's mtime is stable across the build.

## Verified deploy path

- Vercel project serving `grokbothq.xyz`, built from this repo (`next build`, Next 16.3.3). No
  `vercel.json` — the framework preset does the work.
- The repo is public **by design** (MIT / CC BY 4.0 content): pushes are public, and that is fine.
- Deploy verification is by watching the live domain after a push, not by trusting the dashboard —
  see the first commit in this batch (`SEOC` note below records the outcome).

## What shipped, 2026-10-02 (audit items 1, 3, 4, 5, 6, 7, 8, 9, 10, 11)

| # | Item | What changed |
|---|---|---|
| 1 | Description mid-word truncation (the audit's headline bug) | `src/lib/seo.ts` gained `clampText` / `clampSentence` / `composeDescription` / `composeTitle`. Bot metadata now trims on a sentence (never mid-word) and keeps the whole name. 1,501 pages were cut mid-word; 91% of titles ran long |
| 3 | 77 duplicate-name clusters | **Not consolidated — deliberately.** See `DECISIONS.md`: all 77 clusters are distinct bots (0 shared URLs, different builders). Titles now disambiguate: `Chief of Staff (aryamankhawow) - Grok bot` |
| 4 | One non-commodity element per listing | New "How this one fits" block, computed per listing: category size, install rank within the category, how many listings share the name, verification date. Plus the render no longer repeats the tagline (1,904 descriptions opened by restating it) |
| 5 | Hub equity to the terminal tier | `/bots` gained crawlable server-side pagination (`?page=2..43`, self-canonical, 60 per page, in the sitemap). The homepage now links the 50 most-installed listings internally instead of linking straight out to x.ai with `nofollow` |
| 6 | Head term "grok bot directory" (was pos 29) | The phrase is now in the H1 and the opening line of `/bots`, not only the meta tag |
| 7 | Hub page weight | `/new` 10.0 MB → 269 KB, `/use-cases` 6.5 MB → 636 KB, `/bots` 2.2 MB → 455 KB (paginated; the client search island went from 2,594 listings to 600 with exact totals still displayed) |
| 8 | `/md/*` indexable duplicates | `X-Robots-Tag: noindex` on every markdown variant |
| 9 | Category roundups | 4 new pages: `/roundups/engineering`, `/roundups/productivity`, `/roundups/money`, `/roundups/research` — every number computed at build, ranking only the listings that publish install counts, with that coverage printed |
| 10 | Change ledger + decisions | this file and `DECISIONS.md` |
| 11 | `lastVerifiedAt` per listing | `scripts/audit-directory.mjs` stamps the date on every listing it reaches (writes only when a date changes; `--no-stamp` for a read-only run). The bot page shows it |

## Baseline (Search Console, read 2026-10-02)

- Page dimension, 28 days to 2026-09-28: **5,403 impressions, 7 clicks, 140 of ~2,608 sitemap URLs
  received any impression.**
- `/bots` alone carries ~85% of impressions at position 6.3 with 1 click. The terminal tier (2,588
  listings) is essentially invisible, which is the finding every change above is aimed at.
- Query dimension stops at 2026-09-15. **Diagnosed, not a bug** — see below.
- Index coverage of the listing tier is **unknown**: the per-URL indexing report is not reachable
  without the Search Console UI, and neither the page nor query dimension stores index status. Do not
  infer it from impressions.

### The query-dimension gap (audit item 2)

Settled 2026-10-02 with a control, not a guess: the sync endpoint authenticates and returns rows
(`{"success":true,"keywordsInserted":151,"pagesInserted":374}`), and solarbachat + nullmail return
query rows through the same pipeline for the same days. grokbothq does not, because its impressions
collapsed from 2,711/day to under 75/day on 09-08 — no query then clears Google's anonymity
threshold. Recorded as a known cause in `~/.hermes/scripts/gsc-dimension-diagnostic.py`, which runs
daily and stays silent unless a *different* site develops the symptom or any site's page data stalls
behind the freshest property.

The OAuth refresh token in `~/.hermes/secrets/gsc-crawlseo-creds.json` is dead (`invalid_grant`);
the pipeline itself runs on the app's NextAuth session token, which is fine, but any future direct
API work needs a re-auth.

## Due for review

| Change | Ships | Measure by | How |
|---|---|---|---|
| The whole 2026-10-02 batch | 2026-10-02 | **2026-10-30** (4 weeks) | Page-level clicks + impressions for `/bots` and the pager series; whether `/bots/*` URLs start registering impressions. The changes ship together, so they cannot be attributed individually — measure the aggregate, on clicks |
| Titles (set here) | 2026-10-02 | 2026-11-13 (6 weeks) | CTR on the few listing pages that surface; do not re-touch titles before then |
| Roundups | 2026-10-02 | 2026-11-13 | Whether the four pages get indexed at all and which queries they pick up |

## Limits, stated rather than inferred

- No Search Console UI access: index coverage per template, the Links report, and any indexing export
  are unavailable. Everything above comes from the page/query performance tables plus live fetches.
- `/md/*` pages are served for AI agents; they are deliberately excluded from search.
- Listings that declare no integrations are "unknown", never "none". The site says so on each page.
