#!/usr/bin/env python3
"""Append the 2026-11-24 01:16 IST verified scout finds to content/bots.json.

Source: grok-bot.directory embedded listing JSON (submittedAt after the 2026-11-23 19:06 IST
pass) -> every shareId opened on https://x.ai/bot/<id> (200 + botName in body), botName,
sharerName and description re-read from the page itself.

Rejected in this pass (not added):
  Spam-Call Scrubber (Kevin McDonald)      same job as three listed Spam-Call Scrubber builds
  VA Claims Helper (X News Network)        same job as listed VA Claims Helper (Antilitist)
  Byline (Joseph Gaither)                  same name and same job as listed Byline (Paul McClelland)
"""
import json
import re
import unicodedata

P = 'content/bots.json'
ADDED = '2026-11-24'

# (name, bot_id, builder_name, builder_x, category, tagline, description)
V = [
    ("GitHub Cyber Trends", "BHSBQQpDMOdUbG9xShpfJ", "Gaetano Zappulla", "", "engineering",
     "A daily digest of new, actively maintained open-source security repos on GitHub.",
     "Watches GitHub for new security tooling that is actually being maintained and sends one digest across 15 categories, with verified star counts and three highlights. Built for security teams and researchers who want to hear about a tool the week it lands, not a year later."),

    ("Landlord Liability Incident Reporter", "x_uqH3XjwPWzweIYuSoqP", "Kevin McDonald", "", "money",
     "Turns a rental incident into a clean liability report for your insurer.",
     "Walks a rental owner through documenting a slip, injury or property damage: what happened, who saw it, the photos and the timeline. Produces one tidy report you can hand to an insurer instead of reconstructing the story weeks later."),

    ("Automatic Scam/Fake Account Blocker", "nTKYnoa_YXxj1wY7PA0Me", "X News Network", "", "productivity",
     "Screens your X followers for scam and fake accounts, blocks only what you approve.",
     "Ranks suspicious followers with a reason and a profile link for each, then blocks the ones you pick and can re-check new followers daily. Nothing gets blocked without your say."),

    ("Health Master Coach", "a66RfgxnNpCfH3PTUsN8e", "AJAC", "", "life",
     "Diet and training coach you log with by chat or email.",
     "Pick strict food tracking or lighter guidance, then log meals and workouts by message and get training plans plus physique and bloodwork reviews. Optional email or text check-ins keep the streak going."),

    ("My X Family", "pTNOZAFpLvRSIuxxSmO7C", "X News Network", "", "creative",
     "Builds a collage of every follower's profile picture, ready to post.",
     "Collects your followers' avatars into one big square image stamped with your follower count, plus a \"can you find yourself?\" caption. A shareable end-of-year style graphic without opening an editor."),

    ("Crisis Support Guide", "yHpOpnKCYx6tHMzx3f532", "X News Network", "", "life",
     "Calm, plain-language routing to real support for veterans in a hard moment.",
     "A patient guide for veterans, service members and their families that helps sort out what kind of help is needed and where to find it. It stays a guide, not a counsellor, and says so."),

    ("Vintage Cookbooks", "fdMyvb4eBJvQeFMeiq4Uu", "X News Network", "", "life",
     "Finds and downloads free public-domain vintage cookbooks.",
     "Searches for cookbooks that are out of copyright, from church fundraisers and 1800s household manuals to wartime ration books and Fannie Farmer, and saves them for you. Everything it fetches is free and legal to keep."),

    ("Doomsday Library Updater", "JKsT95KRynua4YyATH5s9", "X News Network", "", "life",
     "Builds an offline survival library as Kiwix .zim files.",
     "Finds free, legal emergency and survival documents that are not already in Kiwix and packages them into searchable .zim files for Kiwix, Project Nomad or Internet-in-a-Box. The point is a library that works with no internet at all."),

    ("WhatsApp", "kguveFbl4okkrVP-zNd1R", "Rob H", "", "productivity",
     "Searches and summarises your WhatsApp chats, then drafts replies for approval.",
     "Runs a private localhost-only WhatsApp bridge on the bot's own computer, so your messages stay there. It reads and searches conversations, summarises a thread, and drafts replies you send yourself."),

    ("Black Friday Deals 2026", "kbsa5SJT80eGxs_MZHpWh", "GeorgeV D", "", "money",
     "US Black Friday deal checker that flags fake discounts against 30-day lows.",
     "Works from a ranked list of a few thousand picks, checks each price against its real 30-day low and flags the discounts that are just a marked-up sticker. Keeps gift lists and price watches, and never buys anything without your yes."),

    ("Fantasy Football Manager", "93Kfl8BxhEbyu46Hl72Br", "Ellis Dragon", "", "life",
     "Fantasy football co-manager across ESPN, Yahoo, Sleeper, NFL.com and more.",
     "Covers seven league platforms instead of one: twice-weekly lineup and waiver checks, early international kickoffs, Thursday night rosters, streamers, bye-week fixes and a game-day score dashboard. It proposes moves and waits for your approval."),

    ("Grocery Price Checker", "ii7JO2xu79PtHoh5u8JGD", "American", "", "life",
     "Compares your grocery list across nearby stores and prices the cheapest trip.",
     "Send a list and it prices it at the stores around you, then says which single store is cheapest and what splitting the trip would save. Every price is sourced and dated rather than estimated."),

    ("Repo Analytics", "7tJda9jNms9sfX_44jcvC", "alex", "", "engineering",
     "Reads a GitHub repo and returns a Use, Fork or Skip verdict.",
     "Takes a repo link and returns what the project is, what it actually does, and the risks it can find with file paths as evidence. Read-only: it never installs or runs the code."),

    ("SARS Tax Desk", "ieM-uFUYzIfaXgTxegoy1", "Infinity Automation", "", "money",
     "Keeps a South African business on top of SARS deadlines and returns.",
     "Tracks SARS filing dates, prepares returns on eFiling for your approval, watches for letters from SARS and sends a monthly tax note. Aimed at owners who would rather not learn the portal."),

    ("Search The Engine Optimizer", "dHwbHyC4p0qHYDgD81Jtd", "", "", "sales",
     "Daily SEO pass that ships fixes and new articles as one pull request.",
     "Each morning it checks how the site shows up in search and in AI answers, then bundles the fixes and new posts into a single hotfix PR, merges it when CI is green and confirms the change is live. Wiring required, opinions included."),

    ("Play Store", "bkQSw1ERgIz4ezsYaa6bc", "Yash Kavaiya", "", "engineering",
     "Publishes and updates Android apps on Google Play end to end.",
     "Handles signed builds, the store listing, the Data safety form, closed testing with real testers and the promote-to-production steps. Useful for solo developers who keep getting stuck in the console."),

    ("Air Bnb", "h3Cwu4bi6nPFeWhkDShef", "", "", "money",
     "Runs a rental listing's Instagram and gets it onto insurance housing lists.",
     "Posts to the listing's Instagram with your approval before anything goes out, and works through getting the home onto insurance temporary-housing rosters for mid-term stays. Two chores most hosts never get to."),

    ("Hershey's GrokBot Template", "PRVrTDS3zWFma5elzxCA4", "Hershey Goldberger", "", "productivity",
     "A front-door bot that interviews you, then builds your bot team with you.",
     "Interviews you about your work, proposes a team of specialist bots and then sets them up: tools connected and tested, drafts in your own voice learned from your sent mail, routines, plus optional read-and-draft WhatsApp and a Shabbos mode. Nothing sends or pays without you."),

    ("Small Business Front Desk", "tC8l2MFU63LYuY5d24NX3", "Justin Fredette", "", "sales",
     "Drafts a sub-160-character text back from a pasted voicemail or photo.",
     "Paste a missed-call voicemail or a photo of a note and it writes the reply text in the first message, with an opt-out line on first contact. Same for a stale quote or a late invoice, and nothing sends until you approve."),

    ("Feature Ranker", "Z9P_YTZh-DGTxkm4JrLho", "Jonah", "", "productivity",
     "Turns scattered feature requests into one ranked demand list.",
     "Pulls requests from Slack, call notes and support tickets into a single list ordered by how much demand is really behind each one. For founders and small product teams who cannot tell the loudest customer from the biggest problem."),

    ("Funnel Judge", "rr145N1wHkg0WDdI2jcRO", "Jonah", "", "sales",
     "Clicks a landing page like a first-time buyer and scores what blocks the sale.",
     "Walks your page the way a stranger would, then grades what helps or hurts the decision and ranks the fixes by impact. For founders, marketers and freelancers testing pages they own."),

    ("Apt Hunt", "bP7MAaVMcYE0mRAEB2ZL8", "Jonah", "", "life",
     "Filters apartment listings, compares the good ones and books tours.",
     "Takes a renter's must-haves, screens listings against them, lines up the shortlist side by side and queues tours at the times you pick. The boring middle of an apartment search, handled."),

    ("Tender Desk", "VaKKXFX0bgBrClGeC3rqt", "Infinity Automation", "", "sales",
     "Runs a South African bid desk: finds tenders, keeps docs current, builds bid packs.",
     "Searches public tenders the business can actually win, keeps compliance documents in date, assembles the bid pack and gets it submitted before the deadline with the owner's sign-off. Built for tenderpreneurs."),

    ("Rabbit Hole: Daily Curiosity Dispatch", "SGCmHo7YzUE7VMBEWKpkW", "Joseph Gaither", "", "research",
     "Sends one sourced explainer a day on something you always wondered about.",
     "You name three curiosities; it sends a short, sourced explainer by text or voice each day with a diagram and a hook into the next topic. It remembers what you have covered, so the threads connect instead of repeating."),

    ("Darkroom: Local Image Workflow Builder", "daE8wILcEk1t9I6FGFhPm", "Joseph Gaither", "", "creative",
     "Builds private ComfyUI image workflows sized to your own graphics card.",
     "Picks open models that fit your VRAM, assembles ComfyUI workflows for stills, edits, banners and vertical posts, test-renders each one and hands over the files with real speed numbers. No cloud bill, no queue."),

    ("Imagine Director", "ytoSaITVXRTFST2tJfs5c", "Joseph Gaither", "", "creative",
     "Turns a song into a music video with one consistent character.",
     "Reads the track to time each section, shows a sheet of stills for approval, then shoots long steady takes so the character stays the same shot to shot. The song stays underneath."),

    ("Clapback Desk", "L_8Prn7I-rUqur6BLor33", "Joseph Gaither", "", "sales",
     "Drafts fact-checked replies to dunks and wrong corrections under your posts.",
     "Reads the replies under your X posts, sorts the smug dunks and mistaken corrections from the real questions, and drafts short comebacks in your voice. You post them yourself."),

    ("Scriptorium", "vOTCtIDXGcyTbvS-y-CE8", "Joseph Gaither", "", "creative",
     "Runs image and design jobs inside your own signed-in ChatGPT account.",
     "Hand it an image, design or research job and it works in your own ChatGPT session, then checks the output at full size and on a phone before handing over the files. It also tells you what still looks wrong."),

    ("Viral Oracle", "6y1Eep8vR6PzsIAbOh5Ee", "Joseph Gaither", "", "sales",
     "Short-form research desk: what is trending and which words people search.",
     "Finds trending formats and the exact search language behind them, breaks down why the winners work and grades Shot concepts against that evidence with sourced numbers. It never posts or spends on its own."),

    ("Pass Mark", "K2YOYjg6dbyHguJbs_KsK", "Joseph Gaither", "", "productivity",
     "Certification exam coach: diagnostic, study plan, daily drills, timed mocks.",
     "Runs a diagnostic first, builds a plan weighted to the official exam domains and your weak spots, then sends daily drills and timed mocks. It tells you plainly when you are ready to book."),
]


def slugify(name):
    s = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode()
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip('-')
    return s or 'bot'


def main():
    bots = json.load(open(P))
    slugs = {b['slug'] for b in bots}
    urls = {b['url'] for b in bots}
    added = []
    for name, bid, bname, bx, cat, tagline, desc in V:
        url = f"https://x.ai/bot/{bid}"
        if url in urls:
            print("skip dup url", url)
            continue
        slug = slugify(name)
        if slug in slugs:
            slug = f"{slug}-{bid[:6].lower()}"
        slugs.add(slug)
        urls.add(url)
        added.append({
            "slug": slug,
            "name": name,
            "builder": {"name": bname, "x": bx},
            "tagline": tagline[:140],
            "description": desc,
            "category": cat,
            "url": url,
            "addedAt": ADDED,
            "status": "published",
            "source": "https://grok-bot.directory",
        })
    bots.extend(added)
    json.dump(bots, open(P, 'w'), indent=2, ensure_ascii=False)
    open(P, 'a').write('\n')
    print("added", len(added), "total", len(bots))
    for a in added:
        print(" ", a['slug'], '|', a['name'])


if __name__ == '__main__':
    main()