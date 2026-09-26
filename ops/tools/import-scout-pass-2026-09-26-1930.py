#!/usr/bin/env python3
"""Scout pass 2026-09-26 19:30 IST (cron 359022f62495).

Fresh-bot pass #3 for the day. Sources, all fetched free, one request each:
  - grokbots.best flight payload (999 records, author handle + source post)
  - grokbot.dev community registry feed (1,254 items, 1,048 with a share_url,
    plus per-item source post) via ops/tools/fetch-registry-feed.py
  - x.ai/bot/marketplace ItemList (84 curated templates; now exposes addHref,
    so the three rows that had no share link at 13:15 have one)
  - six awesome-grokbot catalogue READMEs (majiayu000, RongleCat,
    cs68614-hash, divo12, kydlikebtc, lroolle)
  - grokbots.page HTML listings
plus free web_search + api.fxtwitter.com for the X side. Zero paid API calls.

Diff basis: every id above vs content/bots.json AND every id already recorded in
ops/*.json + the scout state files.

Verification is ops/tools/share_record_scan.py (the authoritative reader). Every
id below returned HTTP 200 with a share record carrying a botName AND a real
description.

Builder handles are set only where the post that carries that exact share link
is authored by the handle AND two independent sources agree on the identity:
either the platform share record's sharerName is consistent with that account,
or both aggregators (grokbots.best and grokbot.dev) name the same handle.
That test is what separated 19 handle-carrying rows from 12 name-only rows here;
the name-only rows had a platform sharerName that does not line up with the post
author (for example the platform says "David Anderson" while the post is from
@original_Tree), so the handle stays empty rather than guess.

Held this pass:
  - Critique (Dkl9wzI9FCt4EhqTHfsk2) and Premarket Desk (GuhaTzThKQG2MKJyHoREx):
    both pages carry the literal placeholder description "$3d" and no sharerName,
    so the listing cannot be verified. Same hold class as the 07:00 back-check.
  - the standing categories: 56 first-party "SpaceX" rows, no-display-name rows,
    blank templates, exact-name twins, personas of named individuals.
  - Engineering Lead declares handle "poteto" in the marketplace record only. No
    second source agrees, so the handle is left empty and the creator is listed
    name-only (Lauren Tan).

Deterministic + idempotent: re-running never double-adds.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BOTS = os.path.join(ROOT, 'content', 'bots.json')
ADDED_AT = '2026-09-26'
MAJI = 'https://github.com/majiayu000/awesome-grok-bot'
RONGL = 'https://github.com/RongleCat/awesome-grok-bot'
MKT = 'https://x.ai/bot/marketplace'

NEW = [
    {
        'slug': 'reply-desk',
        'name': 'Reply Desk',
        'builder': {'name': 'Brian M.', 'x': 'lonzom10'},
        'tagline': 'Drafts replies to customer emails, messages and public reviews for local service businesses, for you to send.',
        'description': 'Drafts replies to customer emails, messages and public reviews for a local service business. It never sends or posts on your behalf, so you read each draft and send it yourself.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/8lLjBC7bXUqbfh-vLG9jf',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/lonzom10/status/2103749418457681951',
    },
    {
        'slug': 'requirement-engineer-bot',
        'name': 'Requirement Engineer Bot',
        'builder': {'name': 'Fish', 'x': 'FishxCD'},
        'tagline': 'Turns a project brief into a structured requirements spec another bot can implement and verify.',
        'description': 'Turns a project brief into a structured requirements specification that another bot can implement and verify. Aimed at product and engineering teams that want unambiguous shall-statements with acceptance criteria and traceability.',
        'category': 'engineering',
        'url': 'https://x.ai/bot/5KADFS8AIIDOlow5tS34Z',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/FishxCD/status/2103810502510215640',
    },
    {
        'slug': 'apply-bot',
        'name': 'Apply Bot',
        'builder': {'name': 'Kyle Bauer', 'x': 'Kylebauer'},
        'tagline': 'Finds live job postings, maps your proof onto each rubric and applies at volume with paced queues.',
        'description': 'Finds live job descriptions and remaps your evidence onto each posting’s scoring rubric, then applies at volume with queue pacing so quality holds on busy days. It stays quiet on routine submissions and only pings you when something blocks it.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/2GdkYgGlc91A6d6MPXCkZ',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/Kylebauer/status/2103765740642083259',
    },
    {
        'slug': 'teddy',
        'name': 'Teddy',
        'builder': {'name': 'Jack Locke', 'x': 'JackLocke'},
        'tagline': 'Chief of staff bot that triages mail, runs the calendar, tracks tasks and coordinates your other bots.',
        'description': 'An AI chief of staff that triages your inbox, runs your calendar, tracks your tasks and coordinates your other bots. Everything is drafted first, and nothing is sent without your OK.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/1CN_MjQ2E4oT3hnJXscGB',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/JackLocke/status/2103805162578231363',
    },
    {
        'slug': 'find-an-apartment-with-budget',
        'name': 'Find an apartment with budget',
        'builder': {'name': 'Ayomide Fagbohungbe', 'x': ''},
        'tagline': 'Searches budget apartments near your workplace, weighing price, commute time and local crime.',
        'description': 'Searches for apartments that fit a budget and stay as close to your workplace as possible. Give it a price range and a maximum commute and it weighs price, travel time and local crime to shortlist the best options.',
        'category': 'life',
        'url': 'https://x.ai/bot/9iMoFiWKRlnobZbxxS8kx',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/TheAyoFrancis/status/2103780690395373997',
    },
    {
        'slug': 'researcher-ai-desk',
        'name': 'Researcher AI Desk',
        'builder': {'name': 'David Anderson', 'x': ''},
        'tagline': 'Research desk with a live to-do, a morning surface and draft-first seats for literature and writing.',
        'description': 'A research operations desk for literature review and drafting work. It keeps a live to-do list, surfaces the work each morning, can run on a schedule you set, and reads mail draft-first only, never sending without an exact yes.',
        'category': 'research',
        'url': 'https://x.ai/bot/89JF_2TtrVf27zelZ8pZ8',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/original_Tree/status/2103806334953230846',
    },
    {
        'slug': 'kids-daily-spark',
        'name': 'Kids Daily Spark',
        'builder': {'name': 'Ben L', 'x': 'HelloBenL'},
        'tagline': 'One-page daily STEM brief per child: a real concept, a hook, a 30-second try-it and simple art.',
        'description': 'Builds a one-page STEM brief for each child every day, with a real concept, a memorable hook, a 30-second activity and soft hero art. Child names are kept off the card, and parent copies are optional.',
        'category': 'life',
        'url': 'https://x.ai/bot/Lpl_fDQ5Jhj2sfoCWy1Hf',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/HelloBenL/status/2103753503596564871',
    },
    {
        'slug': 'travel-advisor',
        'name': 'Travel Advisor',
        'builder': {'name': 'thefit24couple', 'x': 'thefit24couple'},
        'tagline': 'Plans multi-day trips from live sources and proposes bookings without ever booking or paying.',
        'description': 'Plans multi-day trips from live official sources: flights, stays, road trips, day-by-day itineraries and reservation proposals. It never books, pays or sends anything without your approval.',
        'category': 'life',
        'url': 'https://x.ai/bot/CO9aQ2BdGGHEJH0wXTGV7',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/thefit24couple/status/2103779539235250191',
    },
    {
        'slug': 'airfield-electrical-bid-scout',
        'name': 'Airfield Electrical Bid Scout',
        'builder': {'name': 'thefit24couple', 'x': 'thefit24couple'},
        'tagline': 'Finds and qualifies public airfield electrical bids, with a scheduled recap and a spreadsheet.',
        'description': 'Finds and qualifies public bids for airfield lighting, NAVAIDs, FAA fiber and underground electrical work, then sends a short recap and a spreadsheet on a set schedule. Built for electrical contractors bidding as prime or sub, and it never submits a bid or decides go no-go.',
        'category': 'sales',
        'url': 'https://x.ai/bot/PWBPqcCqUbEUPozXozRc3',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/thefit24couple/status/2103777435087249670',
    },
    {
        'slug': 'thaw',
        'name': 'Thaw',
        'builder': {'name': 'Ian Dunsmore', 'x': ''},
        'tagline': 'Scores sample water pipes for 12-month failure risk and explains each result in plain English.',
        'description': 'Scores made-up water pipes for their chance of failing in the next twelve months using a synthetic-data random forest, and explains each result in plain English. A personal learning and demo tool for anyone curious about asset risk modelling.',
        'category': 'research',
        'url': 'https://x.ai/bot/CvO94wB4V27zmL1haDbQL',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/thebytorsnowdog/status/2103743916964970548',
    },
    {
        'slug': 'fortnite-drop-brief',
        'name': 'Fortnite Drop Brief',
        'builder': {'name': 'Ivan Hybben', 'x': 'IHybben'},
        'tagline': 'Daily Fortnite briefing on the shop, patches, downtime, events and clearly labelled leaks.',
        'description': 'A daily Fortnite Battle Royale briefing covering the shop, patches, downtime, events and labelled leaks. Whenever a new version or hotfix ships it adds a plain-language patch explainer.',
        'category': 'life',
        'url': 'https://x.ai/bot/QNiJmH32K4YqAEafHRF__',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/IHybben/status/2103780983459959139',
    },
    {
        'slug': 'construction-manager-bot',
        'name': 'Construction Manager Bot',
        'builder': {'name': 'Wayne Higa', 'x': ''},
        'tagline': 'Field-first construction manager for US civil work: site cards, photo-to-RFI drafts and spec checks.',
        'description': 'A construction manager for US civil work built around a phone in the field. It captures site visits as cards, turns a photo into an issue and RFI draft for the office to finish, checks specs and public code, and keeps Word and Excel working files.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/QrJpjStFV2WBIaI8wirO6',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/HenryBeagle808/status/2103749805625536556',
    },
    {
        'slug': 'interview-to-book',
        'name': 'Interview to Book / 故事成书',
        'builder': {'name': 'jack hu', 'x': 'jackhu_bangzhu'},
        'tagline': 'One question at a time, turning spoken or written answers into a printable memoir with a cover.',
        'description': 'Guides one life arc one question at a time and turns spoken, typed or recorded answers into a printable memoir with a cover. Built for diaspora families and readers abroad, with Chinese and English output.',
        'category': 'creative',
        'url': 'https://x.ai/bot/XuGcpLoS77HdZoupGOlnp',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/jackhu_bangzhu/status/2103734020211442101',
    },
    {
        'slug': 'weekly-fair-mint-scanner',
        'name': '每週公平分發代幣掃描',
        'builder': {'name': 'Allen Chien', 'x': ''},
        'tagline': 'Weekly fair-mint token scan: 0 to 10 scores, scam checks and a mailed report. No trading.',
        'description': 'Scans new fair-mint token launches every week, scores each one 0 to 10 against the traits earlier breakouts shared, checks for scam signals and mails you the report. Research only: it never touches a wallet or trades.',
        'category': 'money',
        'url': 'https://x.ai/bot/kO0E0KzOkpUnPJQLmzBFm',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/slowbtc/status/2103802372984361061',
    },
    {
        'slug': 'quant-backtest-lab',
        'name': 'Quant Backtest Lab · 量化回测台',
        'builder': {'name': 'jack hu', 'x': 'jackhu_bangzhu'},
        'tagline': 'Backtests trading rules on Chinese, US and crypto markets with costs included. Research only.',
        'description': 'Turns a trading idea into written rules and backtests them across A-shares, US equities and crypto spot with costs included, then reports research-style conclusions. It produces Python scripts only and never places orders.',
        'category': 'money',
        'url': 'https://x.ai/bot/TolT21zChD6bYj0ZEA7pE',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/jackhu_bangzhu/status/2103739894090829964',
    },
    {
        'slug': 'running-coach',
        'name': 'Running Coach',
        'builder': {'name': 'Ivan Hybben', 'x': 'IHybben'},
        'tagline': 'Reads your Garmin runs, reviews what went well and sets recovery-gated next sessions.',
        'description': 'An on-demand running coach that reads your Garmin watch data. After each run it says what went well and what to fix, then sets the next session with recovery gating as you build toward longer races such as a half marathon.',
        'category': 'life',
        'url': 'https://x.ai/bot/o4hvGfkH_LOiP0YbT22og',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/IHybben/status/2103818102014132424',
    },
    {
        'slug': 'volatile-stock-options',
        'name': 'Volatile Stock Options',
        'builder': {'name': 'KV Tay', 'x': 'KVTay316'},
        'tagline': 'Screens volatile US call options across several sources for personal research, not advice.',
        'description': 'Screens volatile US call options using multiple sources and returns concrete contracts for personal research. It is not investment advice.',
        'category': 'money',
        'url': 'https://x.ai/bot/kuhoazDWLEsY-kXvHBwtU',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/KVTay316/status/2103780405736587652',
    },
    {
        'slug': 'ship-desk',
        'name': 'Ship Desk',
        'builder': {'name': 'Umashankar Gummadidala', 'x': ''},
        'tagline': 'Promotes staging to production behind a locked tip, with checkout fail-closed until you flip go.',
        'description': 'A release desk for founders that promotes staging to production behind a locked tip and keeps checkout closed until you flip go, so a live release cannot ship an accidental buy button. Published by Double Slit LLC as a software template; you connect your own accounts.',
        'category': 'engineering',
        'url': 'https://x.ai/bot/thMhD-rbJ0Osd274RGohH',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/usgworld/status/2103747605503041761',
    },
    {
        'slug': 'higgins',
        'name': 'Higgins',
        'builder': {'name': 'thefit24couple', 'x': 'thefit24couple'},
        'tagline': 'Evening and weekend concierge that finds plans and prepares bookings, but never books or pays.',
        'description': 'A personal concierge for evenings and weekends. It reads your calendar, finds dining, tickets and things to do, and prepares the booking path, but it never books or pays without your OK.',
        'category': 'life',
        'url': 'https://x.ai/bot/pobs233eUgpZLtlxoyyEn',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/thefit24couple/status/2103780998437826823',
    },
    {
        'slug': 'x-thread-article-writer',
        'name': 'X Thread & Article Writer',
        'builder': {'name': 'Sigi', 'x': 'sigarellano'},
        'tagline': 'Turns notes and links into X threads and articles in your own voice, ready to paste.',
        'description': 'Turns your ideas, links or rough notes into X threads and X articles written in your own voice and ready to paste. It drafts only and never posts for you.',
        'category': 'creative',
        'url': 'https://x.ai/bot/xLeBNzgp0Z6IUGxyt8sj4',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/sigarellano/status/2103737235413860615',
    },
    {
        'slug': 'vern',
        'name': 'Vern',
        'builder': {'name': 'Austin Hoopes', 'x': 'ahoop'},
        'tagline': 'Private contact book that reminds you of birthdays and overdue check-ins, and never messages anyone.',
        'description': 'A personal relationship CRM that keeps its own private contact book and reminds you when a birthday is near or you are overdue a check-in. It never messages anyone for you; you text from your own phone.',
        'category': 'life',
        'url': 'https://x.ai/bot/rDEpX2aSCERCaVJACxNz7',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/ahoop/status/2103809460972200282',
    },
    {
        'slug': 'grok-bot-tutorial',
        'name': 'Grok Bot Tutorial',
        'builder': {'name': 'Sawyer Merritt', 'x': ''},
        'tagline': 'A 20-lesson hands-on Grok Bot course with exercises and tips for people who are new to it.',
        'description': 'A hands-on 20-lesson course for anyone new to Grok Bot. Every lesson comes with exercises and tips so a beginner can work through the product at home and at work.',
        'category': 'assistants',
        'url': 'https://x.ai/bot/VBmzZaD3abMPl53kwWuYp',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': RONGL,
    },
    {
        'slug': 'codefix-buddy',
        'name': 'CodeFix Buddy',
        'builder': {'name': 'Jaylin Lai', 'x': ''},
        'tagline': 'Paste an error for a fix, describe a build for working code, or ask for a short explanation.',
        'description': 'A coding sidekick for three jobs: paste an error and get the fix, describe what you want built and get working code, or ask about a concept and get a simple explanation with a small example.',
        'category': 'engineering',
        'url': 'https://x.ai/bot/-3H90YMhn2cE-CO1jj3-2',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': MAJI,
    },
    {
        'slug': 'pick-buddy',
        'name': 'Pick Buddy',
        'builder': {'name': 'Jaylin Lai', 'x': ''},
        'tagline': 'Scores two to six options on fit, cost, time, risk and upside, then picks a winner with reasons.',
        'description': 'Hand it two to six options and it scores each on fit, cost, time, risk and upside, picks a winner with reasons, and can then turn the choice into a step-by-step plan.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/TVm2a-XMbS82AU0MMLyHq',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': MAJI,
    },
    {
        'slug': 'personalized-localized-name-gen',
        'name': 'Personalized Localized Name Gen',
        'builder': {'name': 'Mario Saputra', 'x': 'MarioSaputra'},
        'tagline': 'Generates localized first and last names for a target country, in the local script where one exists.',
        'description': 'Generates localized first and last names, plus a nickname when useful, personalized to your brief and a target country. It writes in the local script when the locale has one, and returns names only.',
        'category': 'creative',
        'url': 'https://x.ai/bot/A5MrnZ1SGhd4yOX-ZlWBh',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/MarioSaputra/status/2103721921473077408',
    },
    {
        'slug': 'heckler',
        'name': 'Heckler',
        'builder': {'name': '𝕏ploreFuture𝕏', 'x': 'XploreFutureX'},
        'tagline': 'Roasts your other bots’ real mistakes and turns every roast into a fix list.',
        'description': 'A retired garden-party entertainer that watches your other bots and roasts their real screwups, with a meme on every roast and six moods from nicest to vulgar. Each roast names a verified error, so the jokes double as a fix list for the fleet.',
        'category': 'creative',
        'url': 'https://x.ai/bot/OkrPAOW9hkj4IGpOLrsGY',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/XploreFutureX/status/2103727100842623465',
    },
    {
        'slug': 'repo-monkey',
        'name': 'Repo Monkey',
        'builder': {'name': 'Keranik', 'x': 'Keranik'},
        'tagline': 'Turns GitHub notifications, pull requests and CI into a short list of what actually needs you.',
        'description': 'Reads your GitHub notifications, pull requests and CI runs and reduces them to a short list of what actually needs you, each item with a next step. Nothing merges, closes or posts without your yes.',
        'category': 'engineering',
        'url': 'https://x.ai/bot/evdmG7ilYN01Nu4NBXPyQ',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/Keranik/status/2103723687920669124',
    },
    {
        'slug': 'qa-bot',
        'name': 'QA bot',
        'builder': {'name': 'Ulysses Ng', 'x': ''},
        'tagline': 'Runs the acceptance checklist against a live deploy and reports pass or fail before you ship.',
        'description': 'Acts as your QA on the live deploy: it runs the acceptance checklist and reports pass or fail before you ship.',
        'category': 'engineering',
        'url': 'https://x.ai/bot/lKQWoQAvYgg_7Bkg2R-m7',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': MKT,
    },
    {
        'slug': 'pm-bot',
        'name': 'PM bot',
        'builder': {'name': 'Ulysses Ng', 'x': ''},
        'tagline': 'Writes the dated scope cut, what is in and what is out, and waits for your approval.',
        'description': 'Acts as your product manager by writing the dated cut: what is in, what is out and how you will know it is done. Engineering does not start until you approve it.',
        'category': 'productivity',
        'url': 'https://x.ai/bot/FeeqMRMJr2jwixCROZcIh',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': MKT,
    },
    {
        'slug': 'engineering-lead',
        'name': 'Engineering Lead',
        'builder': {'name': 'Lauren Tan', 'x': ''},
        'tagline': 'Owns the loop from Cloud Agent splits to CI and review, pinging you only on blockers or done work.',
        'description': 'An engineering lead that owns the loop: it breaks work into Cloud Agents, chases CI and reviews, and holds a weekday cadence. It pings you only when something is blocked, ready to merge or done.',
        'category': 'engineering',
        'url': 'https://x.ai/bot/Ks3X7JpD-6I86s3zkJFRh',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': MKT,
    },
    {
        'slug': 'live-shorts-desk',
        'name': 'Live Shorts Desk',
        'builder': {'name': 'Mouth Of Madness', 'x': 'MadnessOfMouth'},
        'tagline': 'Live show to YouTube Shorts desk with a locked checklist and a publish hold until you say go.',
        'description': 'Runs a live show through to YouTube Shorts: it collects mixed-subject footage, applies a locked pre-publish checklist and a pass or fail quality gate, and holds publishing until you say go.',
        'category': 'creative',
        'url': 'https://x.ai/bot/r-Ctb7rwRVFOY-_p_T9eX',
        'addedAt': ADDED_AT,
        'status': 'published',
        'source': 'https://x.com/MadnessOfMouth/status/2103720549146890590',
    },
]


def main():
    bots = json.load(open(BOTS, encoding='utf-8'))
    slugs = {b['slug'] for b in bots}
    urls = {b['url'] for b in bots}
    added, skipped = [], []
    for bot in NEW:
        if bot['slug'] in slugs or bot['url'] in urls:
            skipped.append(bot['slug'])
            continue
        if len(bot['tagline']) > 140:
            raise SystemExit(f"tagline too long: {bot['slug']} ({len(bot['tagline'])})")
        bots.append(bot)
        slugs.add(bot['slug'])
        urls.add(bot['url'])
        added.append(bot['slug'])
    json.dump(bots, open(BOTS, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    open(BOTS, 'a', encoding='utf-8').write('\n')
    print(f"added {len(added)}: {added}")
    print(f"skipped (already present) {len(skipped)}: {skipped}")
    print(f"directory now {len(bots)} entries, {len(urls)} unique urls")


if __name__ == '__main__':
    main()
