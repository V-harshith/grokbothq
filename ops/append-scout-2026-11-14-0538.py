#!/usr/bin/env python3
"""Append verified scout finds (2026-11-14) to content/bots.json.

Source: grokbotsdirectory.com catalogue payload -> every x.ai/bot/<id> opened,
HTTP 200, bot name read back from the page itself (og:title + embedded
botName/sharerName). Builder handle only where the directory record named the
same creator the x.ai page names.
"""
import json
import re
import sys

DATE = "2026-11-14"
NOW = "2026-11-14 05:38 IST"

# (name, bot_id, creator_name, creator_x, tagline, description, category, slug_hint)
ROWS = [
    ("Christmas Deal Elf", "6949mRuhFtUCnpp5CteeT", "Lightning Mike", "LightningMike23",
     "Holiday gift tracker with budgets, price-drop alerts, and a running deal watch.",
     "Keeps a Christmas gift list with a budget per person, suggests ideas while you shop, and alerts you when a watched gift hits a real deal. Also catches price drops on gifts you already bought.",
     "money", "christmas-deal-elf"),
    ("Tea", "5GTRH5hwa8CEPRye2qN7r", "Mike Yeager", "mikepat711",
     "Story tracker that watches a news story, checks the sources, and pings you only on real updates.",
     "Give it a story and it follows the coverage for you: what actually changed, which sources broke it, and whether the claims hold up. Stays quiet between real developments instead of forwarding every headline.",
     "research", "tea-story-tracker"),
    ("Daily Log", "jU1wuOsk0tEIKcosctKn1", "Nitesh Rijal", "openrijal",
     "Nightly work log written into your notes vault, rolled up into a weekly wiki.",
     "Writes a short entry each night about what you worked on, read-only and redacted, into a notes vault organised with PARA or IPARAW. Distils the week into a wiki page so you can see what actually moved.",
     "productivity", "daily-log-work-wiki"),
    ("Black Friday & Prime Day Deals", "8xnH3QJzC9oovGfx3geh7", "Carlo", "Italianclownz",
     "Tracks Black Friday, Cyber Monday, and Prime Day prices at the stores you pick.",
     "Watches the national and online merchants you choose through the holiday sales calendar: doorbusters, discounts measured against earlier prices, and store hours, then alerts you before the good ones run out.",
     "money", "black-friday-prime-day-deals"),
    ("Tax-Loss Harvest Watch", "RI0qAVJN1gtnOky5lZ2h3", "Thomas Ferriere", "Tferriere",
     "Ranks year-end tax-loss harvest candidates from Robinhood tax lots or a CSV export.",
     "Reads your taxable brokerage lots, ranks the positions worth harvesting, and flags wash-sale timing before you rebuy. Taxable accounts only, and it never touches IRAs.",
     "money", "tax-loss-harvest-watch"),
    ("בַּתּ שֶל שַׁבַּתּ", "mgzlEZQT2A6k7tnsY-__v", "The Bromeliad.", "abromeliad",
     "Weekly Shabbat helper: candle lighting times, shul schedule, parsha notes, and guest lists.",
     "Handles the week's Shabbat prep: candle lighting and havdalah times for your location, the shul schedule, parsha talking points, who is coming for meals, and a Shabbat shalom list.",
     "life", "bat-shel-shabbat"),
    ("Cell Phone Plan Finder", "RJSudgYj7pjh-0xawMGkf", "Alexander Muse", "amuse",
     "Finds the cheapest cell plan that works where you live and fits the data you actually use.",
     "Compares carriers by coverage at your address and the data you really burn, counts device payoff and lost trade-in value in the total, and rechecks the market for a cheaper fit.",
     "money", "cell-phone-plan-finder"),
    ("Internet Plan Finder", "-FHBDFDjhn10ClEiZ-ZVZ", "Alexander Muse", "amuse",
     "Finds the best home internet deal at your address, promo periods and equipment fees included.",
     "Pulls the plans actually available at your address, compares true monthly cost after promo pricing and router rental, and checks back monthly to see if a better deal has appeared.",
     "money", "internet-plan-finder"),
    ("The EU Court Watcher", "4oAqt3dhDAvBKggcvbZTo", "Pal Szilagyi", "szilagyipal",
     "Daily watch on EU Court of Justice and General Court judgments, opinions, and new filings.",
     "Posts each day's new judgments, Advocate General opinions, and freshly filed cases, with the parties, the facts behind the dispute, and links to related coverage.",
     "research", "eu-court-watcher"),
    ("PhotoCut.Rad", "Ef8OSedKVBXv9uaXhA5NO", "RED.", "",
     "Turns ordinary photos into vertical strips for photo-dump and panorama posts.",
     "Cuts your photos into tall strips that flow into one another, sorted by colour or arranged as one wide panorama, sized for posting on X and Instagram.",
     "creative", "photocut-rad"),
    ("Weekly Kids Newspaper", "ApoDzW2Uttwptbim_m_Wa", "Carlos Benavides M.", "Calrornds",
     "Builds a printable weekly kids' newspaper: real news at their level, games, a craft, and a comic.",
     "Assembles a weekly paper for children from real news rewritten for their reading level, plus puzzles, a craft, an ongoing comic, and a family calendar. Exports a PDF and prints it when a printer is configured.",
     "life", "weekly-kids-newspaper"),
    ("Video Champ", "oVHufCJT9H3DmxoS-lWNN", "Cola Cat", "benoit404",
     "Takes a vertical video from concept to script, edit, approved release, and performance review.",
     "Produces 9:16 video with Grok Imagine: brief, script, edit, and a release you approve, then feeds what performed back into the next one. Built for short-form social output.",
     "creative", "video-champ"),
    ("Link Site Builder", "IWsQe95JBW5ECQisKLzXJ", "Brad Smith", "bradsmith",
     "Builds a fast personal-brand page that works like a modern link tree, payments included.",
     "Assembles a one-page site with your photo, follow links, a free training offer, newsletter signup, and inline Stripe checkout, so your links and payments live on a page you own.",
     "productivity", "link-site-builder"),
    ("Second Glance", "3G2Hdxi-rDmsxRLrPix65", "Thomas Ferriere", "Tferriere",
     "Drafts your bio, pinned post, and profile fixes so a stranger gets what you do in five seconds.",
     "Reads your X profile and recent posts, then drafts a bio, a pinned post, and profile edits that make your work legible to someone landing on the profile cold.",
     "sales", "second-glance-profile"),
    ("Action Deck", "bcMBpEEL-Q-Wrhi_ixqib", "Mech Tensa", "GrokTheVote",
     "Turns messy task dumps into two-minute action cards, with XP, streaks, and a pet that grows.",
     "Breaks a brain-dump of tasks into small cards you can start immediately, and keeps you going with XP, levels, gentle streaks, and a pet that evolves as you clear them. Built for people who stall on big lists.",
     "productivity", "action-deck"),
    ("Night Shift Analyst", "PU-WCxHwcHmXaK5rqTPUT", "Bookiroad", "bookiroad1",
     "Korean-language morning report on last night's X work and yesterday's post performance.",
     "Part of a six-bot Korean X night shift. Files a 07:00 report on what shipped overnight and how yesterday's posts performed, kept short enough to read on one phone screen.",
     "creative", "night-shift-analyst"),
    ("Night Shift Publisher", "NnseCgeAtocJHmS4pd5rZ", "Bookiroad", "bookiroad1",
     "Holds approved drafts and covers in an overnight queue and asks when you want them posted.",
     "Takes confirmed drafts and cover images from the rest of the night shift, keeps them queued, checks your X connection at setup, and asks what time in the morning you will approve. Works in Korean.",
     "creative", "night-shift-publisher"),
    ("Night Shift Designer", "0PYMSSBT6freU2hcQyTkR", "Bookiroad", "bookiroad1",
     "Makes one 16:9 cover image per approved draft, in the team's brand colours.",
     "Produces a single X cover image for each draft the ops lead approves: one short headline, brand colours, generous whitespace, and no real people or company logos. Hands the file to the publisher.",
     "creative", "night-shift-designer"),
    ("Night Shift Ops Lead", "6AtSvXCIaSReHc-6IG8MN", "Bookiroad", "bookiroad1",
     "Quality gate for the night shift: pass, one revision, or reject each draft against your rules.",
     "Judges each draft against your rules, from banned topics and words to what counts as good writing and the daily posting cap, checks that links open and numbers match their source, then passes approved work to design.",
     "creative", "night-shift-ops-lead"),
]


def main() -> int:
    bots = json.load(open("content/bots.json"))
    have_ids = set()
    slugs = set()
    names = set()
    for b in bots:
        m = re.search(r"x\.ai/bot/([A-Za-z0-9_\-]+)", b["url"])
        if m:
            have_ids.add(m.group(1))
        slugs.add(b["slug"])
        names.add(b["name"].lower().strip())

    added, skipped = [], []
    for name, bid, creator, handle, tagline, desc, cat, slug_hint in ROWS:
        if bid in have_ids:
            skipped.append((name, "bot id already listed"))
            continue
        if name.lower().strip() in names:
            skipped.append((name, "name already listed"))
            continue
        if len(tagline) > 140:
            print("TAGLINE TOO LONG:", name, len(tagline))
            return 1
        slug = slug_hint
        n = 2
        while slug in slugs:
            slug = f"{slug_hint}-{n}"
            n += 1
        slugs.add(slug)
        names.add(name.lower().strip())
        have_ids.add(bid)
        added.append({
            "slug": slug,
            "name": name,
            "builder": {"name": creator, "x": handle},
            "tagline": tagline,
            "description": desc,
            "category": cat,
            "url": f"https://x.ai/bot/{bid}",
            "addedAt": DATE,
            "status": "published",
        })

    bots.extend(added)
    json.dump(bots, open("content/bots.json", "w"), ensure_ascii=False, indent=2)
    open("content/bots.json", "a").write("\n")

    # queue the finds in the scout ledger, newest first, capped at 50
    cands = json.load(open("ops/scout-candidates.json"))
    queue = []
    for row in added:
        hand = row["builder"]["x"]
        queue.append({
            "name": row["name"],
            "bot_id": row["url"].rsplit("/", 1)[1],
            "url": row["url"],
            "builder_x_handle": hand,
            "one_line_desc": row["tagline"],
            "source_post_url": "",
            "found_at": NOW,
            "found_via": "grokbotsdirectory.com catalogue payload",
            "status": "verified + queued to ops/scout-pending",
        })
    cands = (queue + cands)[:50]
    json.dump(cands, open("ops/scout-candidates.json", "w"), ensure_ascii=False, indent=2)
    open("ops/scout-candidates.json", "a").write("\n")

    print(f"added {len(added)}")
    for r in added:
        print(" +", r["slug"], "|", r["name"], "|", r["category"])
    for s in skipped:
        print(" skipped:", s)
    print("total bots:", len(bots))
    return 0


if __name__ == "__main__":
    sys.exit(main())
