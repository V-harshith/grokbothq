# Launch checklist — what exists, what's missing, who does it

The site is a **static Next.js app with GitHub as its CMS**. There is no admin dashboard by
design: every piece of content is a JSON file, every change is a commit, every merge auto-deploys.
You manage it through GitHub (web editor, issues, or Hermes). If you ever want a point-and-click
dashboard, that's the Supabase upgrade path documented in the README.

## Done (working today)

| Area | State |
|---|---|
| Directory | 71 real bots with live x.ai links, install counts from source data |
| Category pages | 8 programmatic pages with FAQ schema |
| Use cases | 69 real examples sourced from X posts (/use-cases) |
| News | /news with real sourced headlines; NewsArticle schema for Google News |
| Bot pages | Two-column layout, sticky action rail, source links, safety note |
| Submission pipeline | Form → GitHub issue → validation → PR → merge = deploy (needs repo **public**) |
| Ads | Carbon-style unit in the standout grid + /bots header; content/ads.json drives it; featured page sells slots |
| Newsletter | Homepage form; works via email now, real provider via one env var |
| Analytics | Umami via env vars; Open-button click events tracked per bot |
| Metrics | Weekly cron pulls Umami click counts into content/metrics.json (needs 3 repo secrets) |
| Ops automation | Weekly: featured expiry, metrics pull, IndexNow ping, build health check |
| SEO/AEO/GEO | Sitemap (121 pages), llms.txt + llms-full.txt, JSON-LD everywhere, robots welcoming AI crawlers |
| Legal | Privacy policy + Terms of use pages |

## Before launch (owner actions)

1. **Buy the domain** (grokbothq.xyz) → attach in Vercel → `NEXT_PUBLIC_SITE_URL`.
2. **Deploy**: `npx vercel`, import `V-harshith/grokbothq`.
3. **Search Console + Bing**: submit `/sitemap.xml`.
4. **Umami**: add site, set `NEXT_PUBLIC_UMAMI_URL` + `NEXT_PUBLIC_UMAMI_WEBSITE_ID` in Vercel; set
   `UMAMI_URL` / `UMAMI_TOKEN` / `UMAMI_SITE_ID` repo secrets so weekly metrics pull works.
5. **Newsletter**: create a Buttondown/Loops list → `NEXT_PUBLIC_NEWSLETTER_ENDPOINT`.
6. **Flip the repo public** when you want the automated submission pipeline live.
7. **Domain auto-renew** with a funded card.

## Deliberately not built (say the word when needed)

- **Live upvotes** — needs a database (Supabase) + spam control. Install-click metrics are the
  honest interim signal.
- **User accounts / dashboards** — not needed for a directory.
- **Sponsor self-serve checkout** — email-based sales flow is fine until volume justifies Stripe.
