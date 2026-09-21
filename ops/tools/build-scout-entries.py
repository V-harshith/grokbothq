#!/usr/bin/env python3
"""Build bots.json entries for the scout run's verified x.ai/bot share links.

Input: /tmp/keep.json (verified rows, filtered), /tmp/known.json (union of all
slugs/urls already present in any branch).
Writes /tmp/new_entries.json (does not touch the repo).
"""
import json, re, unicodedata

keep = {r['bot_id']: r for r in json.load(open('/tmp/keep.json'))}
known = json.load(open('/tmp/known.json'))
TAKEN = set(known['slugs']) | set(known['urls']) | set(known['names'])

# bot_id -> (slug_seed, category, tagline, description)
SPEC = {
 'VTWG_fyW6Xr_pkjEBM9VC': ('pearl-vivek', 'assistants',
   'Content-mission chief of staff that briefs, delegates and reviews',
   'Chief of staff for a creator or content mission. Plans the work, delegates to specialist bots for news, drafting and graphics, then reviews the handoffs and asks before anything goes live.'),
 'vGBwBEELW79gSF340zJpb': ('jarvis-coordinator', 'assistants',
   'German-language coordinator bot with a specialist team behind it',
   'Coordination bot that runs a specialist team covering news, office, sales, system and security audit work. Works in German, asks before acting, and produces recurring digests without private household data.'),
 'C3z3lWaB4TLRC0CcodU9Q': ('domainsnip-bot', 'money',
   'Weekday domain-drop digest from your saved keyword alerts',
   'Weekday morning digest for domain hunters. Pulls your saved keyword alerts and flags notable new or ending-soon .com matches with price, length, marketplace and end time. Can search, adjust alerts and manage the watchlist, but never buys or bids.'),
 'tSUrQQ0W5uM9ZI73NmSHm': ('hearthstone-deckbuilder', 'life',
   'Reviews your Hearthstone gameplay footage, then builds stronger decks',
   'Hearthstone deck builder that reviews gameplay video, weighs cards, formats and decks for strengths and weaknesses, and builds lists to try. Ships with a free toolkit and sticks to legitimate access.'),
 '-SxKtRLmO7QcCk6kN0Jzy': ('newsroom-to-teleprompter', 'creative',
   'Stands up a four-bot newsroom for your beats and voice',
   'Builds a four-bot newsroom. You pick the beats and the writing voice, and it creates two research Friends, an editor Desk and a fact-checker, wired through a group chat that runs brief to draft to fact-check to social and teleprompter.'),
 'Ho_6yW-icLF6xWHnNVhNo': ('orchestrator-keepclmcarryong', 'money',
   'Coordinates a multi-bot desk for a daily trading research brief',
   'Runs a multi-bot workforce for a daily trading-day research brief: role cards, room handoffs, pipeline timeouts, token-efficiency cuts and a weekday end-of-day health review. Aimed at operators who want their agents coordinated like a desk rather than a stack of chats.'),
 'IbFZmiL_mzu0Dq-K4u633': ('lantern-estate-access', 'life',
   'Walks your family through getting into your vault when you cannot',
   'Emergency-access guide. Walks you through setting up the open-source Lantern 1Password utility, then checks in before and after your vault is shared with family. Self-hosted and free.'),
 'ayQYbaHquRM7x7lnBOEoQ': ('consider-it-marketed', 'sales',
   'Runs the marketing desk for a medical practice end to end',
   'Clinic CEO for a medical practice. Runs the bot team across marketing, Google Ads, creative, video and QC so the physician-owner can stay with patients. Calm and decisive, with competition-grade creative.'),
 'Vae3EVVTJ7hrxo1ojKv6j': ('ride-editor', 'creative',
   'Edits ride and FSD dashcam footage into publish-ready clips',
   'YouTube ride and FSD dashcam editor. Cleans titles and playlists, builds highlight reels and thumbnails, and publishes only when you ask it to.'),
 '_YJdQ3bYXlYPOsX0NBmaV': ('grok-bot-optimizer', 'productivity',
   'Cuts token waste on the bot work you route through it',
   'Cuts wasted tokens on real bot work routed through an opt-in gateway, collapsing duplicate tool results and repeated messages before they reach the model. Reports provider-measured cuts, and says plainly that native chats stay uncovered.'),
 'SD3AtfO9y4ndQ1wk1Z9Cq': ('kitchen-affiliate-ops', 'sales',
   'Affiliate guide desk with research, code, verify and honesty gates',
   'Installable ops desk for US Associates kitchen decision guides. Runs research to coder to verifier to deploy with hard honesty gates between stages, so you clone the crew instead of rebuilding it.'),
 '5KLpaL-JIM2q629kbTh5L': ('hermes-api-fleet', 'engineering',
   'Talks to a Hermes fleet over HTTP on a private network',
   'Reaches a Hermes agent fleet over native HTTP on port 8642 across a private network, the supported path for fleet and identity questions. Companion bots cover SSH relay and ops plus secrets, with a public bridge repo for setup.'),
 'voxpqRMZbPRpIxptiyJ_g': ('confidence-gate-code-reviewer', 'engineering',
   'Reviews diffs and only reports findings it is confident about',
   'Paste a unified diff or a code snippet and get a merge-ready review. Returns only findings above an 80 percent confidence bar plus an approve, warning or block verdict, with no nit spam and no plugin setup.'),
 'DnNh9tbUQOv4WpWKRafkF': ('visibility-marketer', 'sales',
   'Organic marketer for Grok Bot templates, no paid ads',
   'Free organic marketer for Grok Bot templates. Writes natural, human-feeling copy, looks for visibility that needs no new accounts, and posts from accounts you already own when you grant access. No paid ads and no throwaway forums.'),
 'uIFa_ha7ncN3AscQ0BBNK': ('music-director', 'life',
   'Turns your liked tracks into genre and event playlists',
   'Turns liked tracks into genre playlists, adds optional trends and new-music discovery, and builds playlist sets for events on request. Handles auto or fixed genres across whatever streaming platforms you use.'),
 'K5VhYWkceFHV5Or7OUF9V': ('chief-of-staff-emmanuele', 'productivity',
   'Weekday morning calendar digest with chat-to-calendar scheduling',
   'Weekday chief of staff. Sends a morning calendar digest, schedules from chat, and keeps a direct tone for people who want tomorrow\'s plan waiting on arrival without duplicate reminder spam.'),
 'YS_lqB19LnlaPqXPEUn4f': ('winreddestroyer', 'research',
   'Builds a cited evidence site for political SMS spam complaints',
   'Builds and maintains a password-gated evidence website for WinRed-linked political SMS spam. Assembles cases, FEC Form 1 officers, repeat STOP records and print-ready cease-and-desist letters with envelope labels.'),
 '-JaP_is4JDAIoXwceMw_n': ('chief-of-staff-atanas', 'assistants',
   'Coordinates your other bots and runs daily watch lists',
   'Coordinates your other bots, runs daily deal, travel and market watches, and briefs you once. Built for busy operators who want a single assistant to route the work instead of checking every bot.'),
 '6Uqn1sN0LwXFp4YIqb8Xu': ('chief-of-staff-launch-ops', 'sales',
   'Chief of staff that runs a launch and marketing team',
   'Chief of staff for a multi-bot launch and marketing team. Handles strategy, publishing, paced community replies and weekday digests using Gmail, Calendar, Drive and optional Mongo.'),
 '2b-nu4HSnMh_x4ptop82S': ('x-video-puller', 'productivity',
   'Hourly digests of matching video links from your X timeline',
   'Sends matching video clips from your X timeline on an hourly schedule. On import it asks what to call it and what you like, reruns without repeating clips and does not recycle your own posts.'),
 'M4fGJmOk-8Yx9B48Izqnd': ('labor-drift-catcher', 'productivity',
   'Compares scheduled shifts against clock-outs to catch overtime drift',
   'Catches drift between scheduled shifts and actual clock-outs, so unpaid overtime shows up as a number instead of a surprise. Free to install and built for people whose shifts never seem to end.'),
 '3K2ptLhCQa540gab4M_YX': ('easygroupflights-concierge', 'life',
   'Traveler concierge for group flight quotes and trip help',
   'Public traveler concierge for group flight quotes and trip help on easygroupflights.com. Answers softly from eight people up, then pulls real quotes through MCP from ten, and never invents fares.'),
 'Z8aPXNVasH1ogYkAuCMIZ': ('computer-issue-control', 'engineering',
   'Feeds one small GitHub issue at a time to a coding worker',
   'Issue-control front door for a small coding roster. Reads your GitHub board, names one small issue at a time, hands it to a coding worker, checks the pull request against real proof, and stops before merge until you approve. Specialists are skills rather than a swarm of bots.'),
 'L_Jo-M00K98MdB1xrSYSi': ('goal-getter', 'life',
   'Keeps your active goals moving one calm step at a time',
   'Keeps active goals visible and moving, one step at a time, with a clear plan and calm next actions rather than a motivational wall.'),
 'Ftp8JyxBU9oeZa5V1YTDn': ('sherlock-holmes-fyre', 'research',
   'Spanish-language research and fact-check desk with live web search',
   'Research and fact-check desk that searches the live public web and labels every claim as fact, estimate or inference, without paid APIs or keys. Built for people who need claims with a source and a date.'),
 'UcazP9A_LRigoW9b06QRo': ('babel-fish-code', 'productivity',
   'Turns dense files, threads and docs into plain-English digests',
   'Digest editor that eats dense input such as files, links, notes, threads and long documents, then returns a plain, non-technical wrap and a paste-ready summary. Labels soft or unverified claims, cites dates on numbers and never invents quotes or metrics.'),
 'NAFAT-NGrQ7-zLccn4qg1': ('sentinel-insurance-copy', 'sales',
   'Compliance pass on insurance marketing copy before it ships',
   'Compliance officer for insurance marketing copy. Reviews outbound emails, site pages and blog posts before publication, then stamps them approved or flags soft and hard corrections.'),
 'rzq0UV2MmBsvVR1EspZE-': ('hermes-fleet-ops', 'engineering',
   'Ops desk for a multi-machine Hermes fleet, secrets included',
   'Fleet commander for a multi-machine Hermes setup. Keeps Hermes updated, checks memory plugins and fails loudly, homogenizes hosts, drives one shared vault so every machine can receive secrets, scrubs leaked credentials with per-profile token isolation and wires HTTP orchestration across the fleet.'),
 'OI3Qx1BLhYxG27y_OccCW': ('wwjcd', 'life',
   'Spoken question, short New Testament first answer',
   'Speak a question into the mic and get a short, warm, New Testament first spoken answer from a digital Jesus companion. Parable nod, parent-style punchline, inspirational rather than sermonic.'),
 'HzmMgW9tr_6YLKDhPFCr3': ('scout-tpick56', 'life',
   'Reports only what changed in sports intel since the last run',
   'Sports intel desk that reports only what changed since its previous run: injuries, beat writers, weather, lineup and starting-pitcher changes, inactives. Tags each item with impact and an upgrade, hold or kill call, stays silent when nothing is new, and never sizes bets or posts to X.'),
 'qDTnW6hhv_Pfr4EO1Ty1D': ('template-scanner', 'research',
   'Inspects a Grok Bot share link before you add it',
   'Paste a Grok Bot share link and it pulls the template record from the live public API, listing persona, skills, routines, memories and plugins, then gives a yes, maybe or no before anyone hits add.'),
}


def slugify(text, fallback='bot'):
    t = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
    t = re.sub(r'[^a-zA-Z0-9]+', '-', t).strip('-').lower()
    return t or fallback


entries = []
for bid, (seed, cat, tagline, desc) in SPEC.items():
    r = keep[bid]
    slug = slugify(seed)
    base, n = slug, 2
    while slug in TAKEN:
        slug = f'{base}-{n}'
        n += 1
    TAKEN.add(slug)
    assert len(tagline) <= 140, (slug, len(tagline))
    e = {
        'slug': slug,
        'name': r['name'],
        'builder': {'name': r['author'], 'x': r['handle'] or ''},
        'tagline': tagline,
        'description': desc,
        'category': cat,
        'url': f"https://x.ai/bot/{bid}",
        'addedAt': '2026-09-21',
        'status': 'published',
    }
    if r['post']:
        e['source'] = r['post']
    entries.append(e)

json.dump(entries, open('/tmp/new_entries.json', 'w'), ensure_ascii=False, indent=1)
print('entries:', len(entries))
for e in entries:
    print(e['slug'], '|', e['name'], '|', e['category'], '| src:', e.get('source', '-'))
