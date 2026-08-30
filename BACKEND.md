# Backend roadmap — what a database would unlock, and when to build it

The site runs today with **zero backend**: static pages, JSON content, GitHub as the CMS. That is
a feature, not a limitation — it's free to host, fast, and unbreakable. But some features are
structurally impossible without server-side state. Here is the honest map.

## What the current static setup cannot do

| Feature | Why it needs a backend |
|---|---|
| Live upvotes on bots | Votes must be stored per visitor/IP; static files can't accept writes |
| "Connect your bot" feed delivery | Needs per-user subscriptions and an API the bot calls |
| User accounts / saved lists | Auth + storage |
| Realtime install counters | Requires a write endpoint (current: weekly Umami snapshot, honest but delayed) |
| Comment wall | Moderation + storage |

## Recommended stack when the time comes: Supabase (free tier)

1. **Tables**: `bot_votes (bot_slug, voter_hash, created_at)`, `bot_meta (slug, installs, upvotes)`,
   `submissions (…)` if the GitHub pipeline ever feels limiting.
2. **API**: Next.js route handlers (`/api/vote`) with rate limiting by IP hash.
3. **Client**: a small client component posts votes optimistically; counts merge into the build.
4. **Auth**: only if accounts ship — Supabase Auth with X login would fit the audience.

## Migration order (each is a small, contained change)

1. `/api/vote` + upvote button (1 day) — the single highest-value add.
2. Realtime install counts via the same route (bots POST their own install pings).
3. Submissions form → database with a review dashboard (replaces the GitHub-issue flow).
4. Saved lists / favorites (needs auth).

## What we deliberately will NOT build

- A custom CMS — GitHub + Hermes already manage content better than a bespoke admin would.
- A comment system — moderation cost, no audience for it yet.
- Self-serve sponsor checkout — email sales until volume justifies Stripe.
