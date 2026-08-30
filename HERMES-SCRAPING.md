# Hermes scraping playbook - keeping the directory real and fresh

You (Hermes, or any agent with GitHub + browser access) are the data pipeline for GrokBot HQ
(`V-harshith/grokbothq`). This document tells you exactly what to collect, how to verify it,
and how to ship it. Read `AGENTS.md` first for the hard rules.

## Mission

1. Keep every bot in `content/bots.json` **real** - every `url` must open an actual bot at x.ai/bot.
2. Grow the **use-cases** data: each bot with a `source` field (the X post where it was introduced
   or used) automatically appears on `/use-cases` and its detail page. Your job is to find and
   attach more of those.

## Sources and methods

### A. Grok bot directories (easiest, structured data)

Both reference directories embed their full listing data as JSON inside the page HTML:

- `https://grokbots.best/` - records look like:
  `{"slug":"be-happier","name":"Be Happier","description":"...","author":"@lennysan",
    "link":"https://x.ai/bot/<ID>","source_url":"https://x.com/<user>/status/<id>",
    "tags":[...],"integrations":[...],"published":true,"created_at":"..."}`
- `https://www.grokbots.page/` - similar directory, inspect its HTML/JSON payload.

Fetch the page (curl or browser), locate the embedded JSON array, and extract records.
`scripts/import-real-bots.mjs` is a working reference implementation for the grokbots.best format:

```bash
node scripts/import-real-bots.mjs saved.html --analyze   # inspect
node scripts/import-real-bots.mjs saved.html --write     # replace content/bots.json
```

**Do not blind-copy.** Extract candidates from these sources, then run verification (below).
Do not copy their editorial descriptions verbatim beyond short factual one-liners - keep
descriptions short, factual, and in our own words where practical.

### B. X discovery (fresh bots, use cases)

Using browser automation on x.com (logged in), run search queries and collect candidate posts:

- `"x.ai/bot"` (links)
- `"built a grok bot"`, `"made a grok bot"`, `"i built a bot on grok"`
- `"grok bot" filter:links`
- niche variants: `"grok bot" (invoice OR expenses)`, `"grok bot" (inbox OR email)`, etc.

For each promising post, capture:

- the post URL (the future `source` field)
- the author handle
- the `x.ai/bot/<id>` link if present (often in the post or a reply)
- 1-2 sentences: what the bot does, in the author's own words (paraphrase for our copy)

### C. Verification (mandatory, every bot, every time)

1. Open the `x.ai/bot/<id>` URL. If it errors, 404s, or shows no bot, **discard** - never ship a
   dead link. This is the #1 quality rule; the directory's entire value is that listings work.
2. Confirm the bot's actual behavior roughly matches the description.
3. Confirm the author handle exists and is plausible (a real account, not a throwaway spam bot).

## Output schema

Append to `content/bots.json` (never reformat the whole file; keep 2-space indent + trailing newline):

```json
{
  "slug": "kebab-case-unique",
  "name": "Bot Name",
  "builder": { "name": "handle", "x": "handle" },
  "tagline": "One-sentence hook (max 140 chars)",
  "description": "1-3 factual sentences. End with: Open it directly from the listing with one click.",
  "category": "assistants|engineering|research|money|sales|creative|life|productivity",
  "url": "https://x.ai/bot/<real-id>",
  "addedAt": "YYYY-MM-DD",
  "status": "published",
  "source": "https://x.com/<user>/status/<id>"
}
```

Optional: `instructions` (only if the builder published them), `features` (2-4 concrete items,
e.g. integrations), `bestFor` (up to 3), `trending: true` (short-lived highlight).

Rules:

- `category` must be one of the eight whitelisted values. When unsure, pick the closest by
  description keywords (see `scripts/import-real-bots.mjs` CATEGORY_RULES for the pattern).
- `source` should be present whenever you found the bot via an X post - it feeds `/use-cases`.
- One of `slug`/`url` already in the file = skip (dedupe).
- Empty `builder.x` is allowed (unknown builder) - the UI hides it.

## Shipping workflow

1. Create a branch: `git checkout -b data/bots-YYYY-MM-DD`.
2. Edit `content/bots.json` (append verified bots) or `content/use-cases` additions.
3. Validate: `node -e "JSON.parse(require('fs').readFileSync('content/bots.json'))"` and `npm run build`.
4. Commit, push, open a PR titled `data: add N verified bots (YYYY-MM-DD)`.
5. CI (Build check) must be green. Merge squash. Deploy is automatic.
6. Alternatively, if only small changes: file a **Management task** issue describing the change
   and let the maintainer flow handle it.

Batch weekly. One PR per batch. Never edit `src/`, `scripts/`, or `.github/` for data work.

## Honesty and legal guardrails

- The site claims listings are reviewed. Agent review + link verification counts, but flag anything
  doubtful in the PR body instead of shipping it silently.
- Never fabricate descriptions, install counts, or reviews. No invented numbers.
- Respect x.com and the reference directories: no aggressive scraping, cache pages, batch requests,
  don't hammer. If a source blocks you, stop and report.
- Trademark: the site is an independent directory; never imply xAI endorsement in copy you write.
