#!/usr/bin/env python3
"""Append 2026-11-15 07:24 IST scout finds: 12 verified bots from grokbots.best newest
(lastmod 2026-11-14/15) cross-checked against x.ai bot pages and source X posts."""
import json, sys

BOTS = 'content/bots.json'
CANDS = 'ops/scout-candidates.json'
FOUND = '2026-11-15 07:24 IST'

new = [
 dict(slug="balanced-news-desk", name="Balanced News Desk", builder={"name": "Barney", "x": "Barneyishere175"},
      tagline="Twice-daily news briefings that pair left and right outlets, keeping reported facts apart from opinion.",
      description="Pulls the day's stories from outlets across the political spectrum and writes two short briefings a day with facts separated from commentary. A standing watch pings you when a major story breaks.",
      category="research",
      features=["Briefings drawn from both sides of the aisle", "Facts kept separate from opinion", "Hourly breaking-news alerts"],
      url="https://x.ai/bot/OT1d4r6xCmNIM6OtjEMH8",
      source="https://x.com/Barneyishere175/status/2121750321747664961"),
 dict(slug="chef-bot", name="Chef Bot", builder={"name": "Leo Martinez", "x": ""},
      tagline="Photo of a dish in, recipe with ingredients and steps out, plus cooking videos that it opened and checked.",
      description="Reads a photo of a dish and returns one or two matching recipes with ingredients and method. It opens candidate cooking videos and watches them before recommending, and takes a name or style hint to sharpen the match.",
      category="life",
      features=["Turns a dish photo into a recipe", "Verifies cooking videos before suggesting them", "Accepts cuisine or style hints"],
      url="https://x.ai/bot/8Q1Pu5Wg8Xaf6mrydCo1w",
      source="https://x.com/SI5NAL/status/2121634261350641926"),
 dict(slug="content-guard", name="Content Guard", builder={"name": "I'm not an alien, I promise.", "x": "bobpickettsr"},
      tagline="Sanitizes drafts before you send them: strips hidden Unicode, normalizes text and flags steganographic payloads.",
      description="Checks text you are about to share for invisible characters and other hidden payloads, then rewrites it clean and reports what it removed. Built for emails, posts and documents that pass through tools you do not fully control.",
      category="engineering",
      features=["Strips invisible Unicode", "Flags anomalies in a draft", "Returns a cleaned version to send"],
      url="https://x.ai/bot/_oew7twKrlIXo6x71pIDb",
      source="https://x.com/bobpickettsr/status/2121662490312655267"),
 dict(slug="farol-analista-de-mercados", name="Farol · Analista de Mercados", builder={"name": "Lord Ricardo Santos", "x": ""},
      tagline="Portuguese-language market analyst for European and US indices and Forex, with pre- and post-session summaries.",
      description="Watches European and US index and Forex sessions, writes a plain-Portuguese summary before and after each one, and alerts on strong moves with the public sources cited. It never places or moves money.",
      category="money",
      features=["Pre-session and post-session summaries", "Alerts on strong index and Forex moves", "Cites public sources, never trades"],
      url="https://x.ai/bot/FW-vlDkCZN_b7kyQst9hw",
      source="https://x.com/TheCornerTrader/status/2121577354191401433"),
 dict(slug="keepsake-memory-book-maker", name="Keepsake: Memory Book Maker", builder={"name": "Melissa", "x": ""},
      tagline="Collects a family's memories of someone who died, then assembles them into a print-ready memorial book.",
      description="Gathers stories and photos from relatives about a person who has died, organises them, and produces a print-ready PDF that can be ordered as a physical book. The builder made it after struggling to collect memories for their own father-in-law.",
      category="life",
      features=["Collects memories from several relatives", "Organises photos and stories into chapters", "Outputs a print-ready PDF"],
      url="https://x.ai/bot/gB5POIEAeLdihLQE-oUVs",
      source="https://x.com/ReconBailey/status/2121744212517372398"),
 dict(slug="medcomms-study-coach", name="MedComms Study Coach", builder={"name": "Amina Guleid", "x": "GuleidAmina"},
      tagline="Study coach for medical communications: GRADE, bias, fair balance and safety claims, taught in short lessons.",
      description="Runs short lessons with worked examples and practice questions on appraising medical evidence, covering GRADE, bias, fair balance and safety claims. Aimed at health reporters and medical writers who need to check claims rather than read a whole course.",
      category="research",
      features=["GRADE and bias appraisal drills", "Practice questions with worked examples", "Fair-balance and safety-claim checks"],
      url="https://x.ai/bot/EuF__9l6RkRWTCezU8spM",
      source="https://x.com/GuleidAmina/status/2121733952360563017"),
 dict(slug="mention-brand-monitor", name="Mention & Brand Monitor", builder={"name": "Darrell Cox II", "x": "DC__Squared"},
      tagline="Sweeps your X mentions, replies and brand keywords, flags problems many people report, drafts replies for approval.",
      description="Reads your mentions, replies and chosen brand keywords on X, groups the ones that point at the same problem, and surfaces opportunities worth answering. It writes reply drafts and waits for your approval before anything posts.",
      category="sales",
      features=["Groups repeated complaints into issues", "Watches brand keywords on X", "Reply drafts, never auto-posts"],
      url="https://x.ai/bot/9Z6MkiClROS5qX66WGfFD",
      source="https://x.com/DC__Squared/status/2121659009606341119"),
 dict(slug="noelle", name="Noelle", builder={"name": "Dave Gambrill", "x": "gambrill"},
      tagline="Holiday gift agent: idea and link per person in a Google Sheet, tracked from order through to wrapped.",
      description="Keeps a Google Sheet of everyone you are shopping for, fills it with gift ideas and links, and tracks each present from order to delivery to wrapped. You do the paying; it does the remembering.",
      category="life",
      features=["One row per person in a Google Sheet", "Gift ideas with buy links", "Order-to-wrapped tracking"],
      url="https://x.ai/bot/Q3ja7ucRHbaP8ntAXMdko",
      source="https://x.com/gambrill/status/2121641808346464437"),
 dict(slug="shoebox", name="Shoebox", builder={"name": "Vishnu Vardhan Reddy", "x": "var_wish"},
      tagline="Sorts years of photos into year and trip folders and finds near-duplicates, showing the plan before it moves files.",
      description="Takes a photo collection and proposes a folder layout by year and trip, catching exact and near-duplicates even when file names differ. It shows the plan first, never deletes anything, and puts suspected duplicates in a review folder.",
      category="life",
      features=["Sorts by year and trip", "Finds near-duplicates across file names", "Plan-first, never deletes"],
      url="https://x.ai/bot/oA2LC3aRpxUKKBX03cyWR",
      source="https://x.com/var_wish/status/2121718429472211450"),
 dict(slug="touch-grass-bot", name="Touch Grass Bot", builder={"name": "Daniel Kelly", "x": "liminalprompt"},
      tagline="A voice-led reset: it calls you off the screen, walks you to the nearest park and breathes with you there.",
      description="Places a voice call, talks you away from the desk, guides you to the closest green space and runs a short breathing session once you arrive. Free to use and it does not store your location.",
      category="life",
      features=["Incoming voice call that pulls you outside", "Routes to the nearest park", "Guided breathing on arrival"],
      url="https://x.ai/bot/iHGNYncTV7FaBO3H2-Dsv",
      source="https://x.com/liminalprompt/status/2121639037194641481"),
 dict(slug="twitter-tony", name="Twitter Tony", builder={"name": "James Harrison", "x": ""},
      tagline="Growth assistant for small creators: finds posts worth replying to, drafts replies in your voice, tracks progress.",
      description="Watches for fresh posts where a reply would land, drafts replies and planned posts in your own voice, and catches comments you have not answered. It also reports growth honestly; you press Post.",
      category="sales",
      features=["Finds reply-worthy posts", "Drafts in your voice", "Flags unanswered comments"],
      url="https://x.ai/bot/_mOgvEOBhJuSBpEGB-67o",
      source="https://x.com/jimaggie/status/2121691413117329472"),
 dict(slug="x-year-lookback", name="X Year Lookback", builder={"name": "Brian", "x": "BrianRoemmele"},
      tagline="Turns any X account's year into a magazine-style PDF retrospective: themes, big moments, recurring people and places.",
      description="Reads a year of an account's posts and lays them out as a glossy PDF magazine with themes, high points, the people and places that recur, and patterns the account may not have noticed. Built for creators, fans and brands who want the year in print.",
      category="creative",
      features=["Year-in-review as a PDF magazine", "Themes and recurring people surfaced", "Print-ready layout"],
      url="https://x.ai/bot/vjKL4in4XL6KM7Ib74bRZ",
      source="https://x.com/BrianRoemmele/status/2121635168314441948"),
]

bots = json.load(open(BOTS))
have = {b['url'] for b in bots}
for n in new:
    if n['url'] in have:
        sys.exit(f"DUPLICATE URL {n['url']}")
    n['addedAt'] = '2026-11-15'
    n['status'] = 'published'
    bots.append(n)
json.dump(bots, open(BOTS, 'w'), ensure_ascii=False, indent=2)
open(BOTS, 'a').write('\n')

# candidates: append then keep 50 newest
cand = json.load(open(CANDS))
from urllib.parse import urlparse
for n in new:
    cand.append(dict(name=n['name'], bot_id=urlparse(n['url']).path.rsplit('/', 1)[-1], url=n['url'],
                     builder_x_handle=n['builder']['x'],
                     one_line_desc=n['tagline'],
                     source_post_url=n['source'], found_at=FOUND,
                     found_via="grokbots.best sitemap lastmod 2026-11-14/15, x.ai page re-read, fxtwitter source post",
                     status="verified + queued to ops/scout-pending"))
cand = cand[-50:]
json.dump(cand, open(CANDS, 'w'), ensure_ascii=False, indent=1)
open(CANDS, 'a').write('\n')
print(f"bots {len(bots)} (+{len(new)}), candidates {len(cand)}")
