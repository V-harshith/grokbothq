# Keyword Map — GrokBot HQ

Research method: **zero-budget autocomplete harvesting**. `ops/tools/keyword-harvester.mjs` mines Google + DuckDuckGo autocomplete (the same suggestions real searchers see) via the alphabet-soup technique — 14 seed queries expanded with a–z and intent prefixes = **168 queries per run**, both engines, `en-IN` locale. Latest run (`ops/data/keywords-2026-09-06.json`): **367 unique keywords**.

Re-run monthly (`node ops/tools/keyword-harvester.mjs --locale=en-IN`) and after major ecosystem events; new intents go into this map and the matching page's metadata.

## The clusters (what searchers actually want)

| Intent | Harvested queries | Owner page |
|---|---|---|
| Confusion: product vs bots | what is grok chatbot, is grok a chatbot, grok ai chatbot free | /faq, /guides/what-are-grok-bots |
| Platform: PC/Mac/Android | grok chatbot for pc, grok bot for android, grok bot for mac/windows | /faq |
| Pricing | grok bot pricing, grok bot cost, is grok bot free, grok bot subscription, grok bot free trial | /faq |
| Comparisons | grok bot vs hermes, grok bot vs openclaw, grok bot vs claude cowork, grok bot vs custom gpts, grok bot alternative | /compare |
| Setup & how-to | grok bot setup, grok bot install, grok bot commands, how to use grok bot, how to get grok bot, grok bot github install | /guides, /agent |
| Directory | best grok bots, grok bot directory, grok bots list, grok bot xai | /bots, / |
| Use cases | grok bot use cases, grok bot examples, what can grok bots do | /use-cases |
| Integrations | grok bot gmail, grok bot slack, grok bot notion, grok bot github | /integrations |
| Freshness | new grok bots, grok bot news, grok bot drops | /new, /news |
| Data | how many grok bots are there, grok bot statistics | /stats |

## Per-page implementation (live in metadata)

| Page | Primary keyword | In title? | meta keywords |
|---|---|---|---|
| / | grok bots + grok chatbot confusion terms | ✅ | ✅ |
| /bots | grok bots list, grok bot directory | ✅ | ✅ |
| /new | new grok bots, fresh drops | ✅ | ✅ |
| /use-cases | grok bot use cases, examples | ✅ | ✅ |
| /integrations | grok bot integrations, gmail/slack | ✅ | ✅ |
| /integrations/[tool] | N grok bots that work with {tool} | ✅ | via tags |
| /groups | grok bot combos & workflows | ✅ | ✅ |
| /guides | grok bot setup, tutorials | ✅ | ✅ |
| /guides/[slug] | per-guide topic keywords | ✅ (seoTitle) | via tags |
| /compare | grok bot vs claude, openclaw, hermes, custom gpts | ✅ | ✅ |
| /news | grok bot news & xAI updates | ✅ | ✅ |
| /stats | how many grok bots exist, statistics | ✅ | ✅ |
| /agent | grok bot api, commands, prompt | ✅ | ✅ |
| /faq | pricing, safety, free | ✅ | ✅ |
| /submit | submit/publish grok bot | ✅ | via pageMetadata |

## Volume - the honest status

Autocomplete proves demand exists but does NOT give search volume. Real volumes require one free step:
upload `ops/data/keyword-planner-upload.csv` (367 keywords, ready) to Google Keyword Planner →
"Get search volume and forecasts" (any Google Ads account works, no spend needed), export, and drop the
result back as `ops/data/keyword-volumes.csv` - pages then get re-prioritized by real numbers.

Until then, `ops/data/keywords-tiered.json` carries a **proxy demand tier** per keyword (multi-seed hits,
both-engine coverage, head-term length): **116 HEAD**, **149 BODY**, **102 long-tail**. Treat tiers as
relative priority, never as volume claims.

## Rules for Hermes

1. New pages must take keywords from **this map or a fresh harvest** — never invented.
2. Primary keyword goes in the title (≤60 chars), first 160 chars of description, and the H1 where natural.
3. FAQ answers: 30–50 words, self-contained, no pronoun ambiguity.
4. Re-run the harvester monthly; add discovered intents here and ship the matching page or FAQ.
5. Never keyword-stuff: one primary phrase per page, used once in the title and once in the first paragraph.
