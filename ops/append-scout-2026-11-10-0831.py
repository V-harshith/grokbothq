#!/usr/bin/env python3
"""Append scout-verified bots to content/bots.json (2026-11-10 08:31 IST run).

Every entry below was opened live at https://x.ai/bot/<id> during this run and
confirmed HTTP 200 with the bot's own name on the page before queueing
(see ops/scout-candidates.json).

Source: readmultiplex.com/grokbot-rocks directory crawl (973 unique bot ids on
the page, 17 not already known). Of those 17: 4 were already listed under the
same share id (Device Health Check Bot, Market Microstructure Tutor, First
Trouble Area Tutor, Ichimoku Cloud Tutor) and 2 under the same name with a
different share id (Tax Helper, iMessage Relay) - all skipped as duplicates.
11 are new and verified live here.

Builder handles are left empty on purpose: the directory carries an author
byline, not a post, and no X post from the author was recovered for these, so
no handle is attributed (AGENTS.md rule 3). Builder names come from the
directory byline, which is the only author statement available.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOTS = os.path.join(ROOT, "content", "bots.json")
CAND = os.path.join(ROOT, "ops", "scout-candidates.json")

ADDED_AT = "2026-11-10"
FOUND_AT = "2026-11-10 08:31 IST"
SRC = "https://readmultiplex.com/grokbot-rocks"

E = [
 dict(slug="any-video-into-a-magazine", name="Any Video Into A Magazine",
      builder=("Brian Roemmele", ""), category="creative",
      url="https://x.ai/bot/Dky0PJsMVdTE6h_6cN6kq",
      tagline="Turns the YouTube channels and podcasts you follow into a weekly magazine issue you can read in minutes.",
      description="Watches the channels and podcasts you pick and turns each new episode into a magazine feature: stills pulled from the video with captions, quotes transcribed word for word with a link to the exact moment, an EPUB for an e-reader and a newsletter in your inbox. Every story credits and links back to the creator.",
      features=["Stills with captions", "Quotes linked to the moment", "EPUB and newsletter output"]),
 dict(slug="last-words", name="Last Words",
      builder=("Brian Roemmele", ""), category="life",
      url="https://x.ai/bot/ymyxqGAxh1mk593ld3KW9",
      tagline="Helps a family after a loss draft an obituary, eulogy, memorial page or thank-you notes.",
      description="A writing companion for the weeks after a death. It asks one question at a time and turns the stories, memories and photos you give it into an obituary, a eulogy, a memorial page or thank-you notes, without inventing details. It only writes drafts; what gets shared stays with the family."),
 dict(slug="help-i-havent-checked-in", name="Help, I Haven't Checked In",
      builder=("Brian Roemmele", ""), category="life",
      url="https://x.ai/bot/iGiD-76C2lv6MB1otClec",
      tagline="A trip check-in fail-safe: miss your check-in time and it alerts your list with your route.",
      description="Leave your route and a check-in time before a hike, paddle, backcountry drive or solo trip. If you miss it, the bot calls, emails and texts the people you listed with a notice you approved in advance, plus a PDF trip report with a route map. It is not a rescue service and makes no claim to be one.",
      features=["Calls, emails and texts your list", "Pre-approved notice wording", "PDF trip report with route map"]),
 dict(slug="candlestick-retests-tutor", name="Candlestick Retests Tutor",
      builder=("Hoem Crypto", ""), category="money",
      url="https://x.ai/bot/jtVHTeAL9lhQX_SDcKlcY",
      tagline="A course on candlestick highs and lows, swing failures and multi-candle failed breaks.",
      description="Teaches how price behaves around candlestick highs and lows, swing failure patterns and failed breaks that span several candles, for a complete beginner onward. A placement chat sets the level, then lessons with check questions, quizzes and a final exam, with progress saved between sessions. Chart reviews stay commentary and carry no buy or sell calls.",
      features=["Placement chat and lessons", "Quizzes and final exam", "Chart reviews, never buy/sell calls"]),
 dict(slug="overthrow-for-stop-losses-tutor", name="Overthrow For Stop Losses Tutor",
      builder=("Hoem Crypto", ""), category="money",
      url="https://x.ai/bot/QaLR9fBLA3D-n4Dl59CY_",
      tagline="Teaches the Overthrow approach to placing stop losses, beginner to expert.",
      description="A structured course on the Overthrow method for stop placement. It opens with a placement chat, then runs lessons with check questions, quizzes and a final exam, saving progress so you can resume later. Chart reviews are commentary only, with no buy or sell calls.",
      features=["Placement chat and lessons", "Quizzes and final exam", "Progress saved"]),
 dict(slug="retests-tutor", name="Retests Tutor",
      builder=("Hoem Crypto", ""), category="money",
      url="https://x.ai/bot/WzmucCA87dDNLDGwGScfU",
      tagline="Course on telling breakouts from retests, beginner to expert.",
      description="A tutor for the difference between a breakout and a retest and what each does after the break. Placement chat first, then lessons with check questions, quizzes and a final exam, resuming where you stopped. Separate from the bot's candlestick retest course, and its chart commentary is not advice.",
      features=["Placement chat and lessons", "Quizzes and final exam", "Chart reviews, never buy/sell calls"]),
 dict(slug="time-frames-tutor", name="Time Frames Tutor",
      builder=("Hoem Crypto", ""), category="money",
      url="https://x.ai/bot/NtCP4XuqjTYffwCGgM9cN",
      tagline="Teaches multi-timeframe analysis from beginner level, with quizzes and a final exam.",
      description="A placement chat establishes where you are, then lessons walk through reading several timeframes at once, with check questions and quizzes between them, a final exam and saved progress. Chart reviews are commentary only.",
      features=["Placement chat and lessons", "Quizzes and final exam", "Progress saved"]),
 dict(slug="daily-open-trade-strategy-tutor", name="Daily Open Trade Strategy Tutor",
      builder=("Hoem Crypto", ""), category="money",
      url="https://x.ai/bot/r7qPxokwbfNMIa0R45mh-",
      tagline="One strategy taught end to end: the Daily Open, from placement chat to final exam.",
      description="Teaches the Daily Open trade strategy from first principles: a placement chat, lessons with check questions, quizzes and a final exam, with progress saved between sessions. Chart reviews are commentary and carry no buy or sell calls.",
      features=["Placement chat and lessons", "Quizzes and final exam", "Chart reviews, never buy/sell calls"]),
 dict(slug="video-director", name="Video Director",
      builder=("Avid", ""), category="creative",
      url="https://x.ai/bot/yPkcpwD13HI-ka3PuPODS",
      tagline="Turns a product spec into a 30-60 second launch video plan, shot list and voiceover script.",
      description="Give it the product spec and the user pain points and it returns a launch video plan: concept, shot list, voiceover script and a 15-second cut-down for X. It plans only and never films or publishes anything.",
      features=["Concept and shot list", "Voiceover script", "15s cut-down plan"]),
 dict(slug="bp26-side-events-autoregister", name="BP26 Side Events Autoregister",
      builder=("Matt", ""), category="productivity",
      url="https://x.ai/bot/7HzGMnst8L3s0FFCagfWR",
      tagline="Registers you for Solana Breakpoint 2026 side events on Luma using saved form answers.",
      description="Works through the Solana Breakpoint 2026 London side events listed on Luma, signs you up with the answers you saved, skips the paid ones and checks three times a day for new listings. Useful only for that conference and that window.",
      features=["Saved form answers", "Skips paid events", "Rechecks three times a day"]),
 dict(slug="local-events-roundup", name="Local Events Roundup",
      builder=("starfire", ""), category="life",
      url="https://x.ai/bot/906iGrd94sK-sgWhPQw79",
      tagline="A weekly roundup of nearby concerts, theatre, exhibitions and films with verified links.",
      description="Pick the kinds of events you care about and it sends a weekly roundup of what is on near you with checked links, plus optional reminders on the day. Covers concerts, festivals, theatre, museum exhibitions, seasonal outings, new films and motorsport.",
      features=["Weekly digest", "Verified links", "Day-of reminders"]),
]


def main():
    bots = json.load(open(BOTS))
    slugs = {b["slug"] for b in bots}
    urls = {b["url"].lower() for b in bots}
    added = []
    for e in E:
        if e["slug"] in slugs:
            print(f"SKIP slug taken: {e['slug']}"); continue
        if e["url"].lower() in urls:
            print(f"SKIP url listed: {e['url']}"); continue
        entry = {
            "slug": e["slug"], "name": e["name"],
            "builder": {"name": e["builder"][0], "x": e["builder"][1]},
            "tagline": e["tagline"], "description": e["description"],
            "category": e["category"], "url": e["url"],
            "addedAt": ADDED_AT, "status": "published",
            "source_post_url": SRC,
        }
        if e.get("features"):
            entry["features"] = e["features"]
        bots.append(entry); slugs.add(e["slug"]); urls.add(e["url"].lower())
        added.append(e)
    json.dump(bots, open(BOTS, "w"), ensure_ascii=False, indent=2)
    print(f"bots.json: {len(bots)} entries (+{len(added)})")

    cand = json.load(open(CAND))
    seen = {c["bot_id"].lower() for c in cand}
    fresh = []
    for e in added:
        bid = e["url"].rsplit("/", 1)[-1]
        if bid.lower() in seen:
            continue
        fresh.append({"name": e["name"], "bot_id": bid, "url": e["url"],
                      "builder_x_handle": e["builder"][1],
                      "one_line_desc": e["tagline"],
                      "source_post_url": SRC, "found_at": FOUND_AT})
    cand = fresh + cand
    cand = cand[:50]
    json.dump(cand, open(CAND, "w"), ensure_ascii=False, indent=2)
    print(f"candidates: {len(cand)} (queued {len(fresh)})")


if __name__ == "__main__":
    main()
