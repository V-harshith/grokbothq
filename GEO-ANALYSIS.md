# GEO Analysis — GrokBot HQ (grokbothq.xyz)

Generated 2026-09-02 against the live build (309 pages, static).

## GEO Readiness Score: 74/100 → **80/100 after the September audit pass**

> Implemented since this analysis: original citable research page (/stats, Dataset schema, daily recomputed), shareable stats infographic, evidence panels, reviewer attribution, FAQ anchors + dated FAQPage schema. Remaining gap is unchanged: off-site entity presence.

| Criterion | Weight | Score | Basis |
|---|---|---|---|
| Citability | 25% | 80 | Quick-answer blocks + quotable taglines on every page; guide intros run full 134-167 word passages; evidence panel carries method + date + limits |
| Structural readability | 20% | 90 | Clean H1→H2 hierarchy, question-based FAQ headings, comparison tables, ordered workflow lists |
| Multi-modal content | 15% | 40 | Text + SVG identity system only; no video, infographics, or interactive tools yet |
| Authority & brand signals | 20% | 55 | Reviewer attribution + dates + source citations on-site; **no off-site entity presence yet** (Reddit/YouTube/Wikipedia) |
| Technical accessibility | 20% | 95 | Fully server-rendered static HTML, all AI crawlers allowed, llms.txt with key facts, JSON API, RSS |

## Platform breakdown

- **Google AI Overviews: strong.** Static HTML, passage-optimized blocks, NewsArticle schema, news sitemap. Eligible via top-10 ranking on long-tail queries.
- **ChatGPT: weak (entity gap).** ChatGPT cites Wikipedia (47.9%) and Reddit (11.3%) — the site is crawlable, but the brand has no off-site entity footprint yet.
- **Perplexity: weak-medium.** Same gap: community validation on Reddit/forums is the missing signal.
- **Bing Copilot: strong.** Bing indexing is wired (IndexNow key live, daily pings).

## AI crawler access (robots.txt)

Allowed: GPTBot, OAI-SearchBot, ChatGPT-User, ClaudeBot, anthropic-ai, PerplexityBot, Perplexity-User, Google-Extended, Applebot, Applebot-Extended, Amazonbot, meta-externalagent, CCBot. `/api/v1/index.json` explicitly allowed. Nothing blocked — maximum citation surface is the deliberate choice for a Challenger site.

## llms.txt status

Present with description, **Key facts** (scale, review method, license, operator, contact, machine index), key pages, categories, guides, comparisons, combos, and the full bot inventory. `llms-full.txt` carries the complete text feed.

## Brand mention analysis (off-site — the gap)

| Platform | Presence | Action |
|---|---|---|
| X | @harshithOG (owner) | Post bot roundups; every listed builder is a link partner |
| Reddit | none | r/Grok, r/SideProject — answer questions with deep links |
| YouTube | none | Even one "5 Grok bots worth opening" video is the strongest citation signal |
| Wikipedia | none | Not eligible yet — needs notability from press coverage first |

## Top 5 highest-impact changes (in order)

1. **Off-site entity presence** — Reddit answers + one YouTube video mentioning GrokBot HQ. Brand mentions correlate ~3× stronger than backlinks.
2. ✅ **DONE: original citable research** — /stats lives, computed daily, Dataset schema + CC BY. Keep it fresh via the daily pass.
3. ⏳ PARTIAL: the /stats shareable infographic card ships (auto-generated OG image). A demo video is still owner-side.
4. **MCP server** — grokbot.dev hosts one; it's the strongest "go-to app store" lock-in. Needs infra (tracked in BACKEND.md).
5. **RSL 1.0 licensing file** — machine-readable AI licensing (spec watch; not implemented yet).

## Content notes

- Bot listings are short by design (honest data only) — they pass as factual aggregation, not thin content, because each links a live source post and real builder.
- Guides already carry dated, self-contained quick answers; combos and comparisons are structured for extraction.
- Schema in production: SoftwareApplication, FAQPage (with dates), Article, NewsArticle, ItemList, CollectionPage, BreadcrumbList, Organization, WebSite+SearchAction, Person.
