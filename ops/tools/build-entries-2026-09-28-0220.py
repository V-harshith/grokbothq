#!/usr/bin/env python3
"""Build this pass's verified entries for content/bots.json (2026-09-28 02:20 IST).

Eight bots cleared the bar: HTTP 200 on x.ai/bot/<id> plus a share record carrying
a real botName and a real description (ops/tools/share_record_scan.py). Descriptions
are our own paraphrase; builder.x is set only where the announcing post is the
creator's own and the account matches the share page's creator name.
"""
import json
import re

ROOT = "/root/grokbothq"
SCRATCH = "/root/.hermes/cache/scratch/"

ENTRIES = [
    {
        "slug": "bill-watch",
        "name": "Bill Watch",
        "builder": {"name": "Dennis W", "x": ""},
        "tagline": "Sweeps your email for charges you forgot and returns a Keep, Cut or Check list.",
        "description": "A read-only money sweep across your inbox. It looks for recurring charges, trials about to convert, unused subscriptions and credits left sitting, then hands back a ledger sorted into keep, cut and check. It does not cancel or change anything itself.",
        "category": "money",
        "url": "https://x.ai/bot/doSuUa9J-ChT2mhQt5Iei",
        "source": "https://x.com/DennisW_15",
    },
    {
        "slug": "quartermaster",
        "name": "Quartermaster",
        "builder": {"name": "James", "x": ""},
        "tagline": "Keeps a household budget in a sheet and reports which card earns most.",
        "description": "A household budget and credit card assistant. It runs a zero-sum budget in Google Sheets, sends a daily finance report with an HTML dashboard, and works out which of your cards earns the most on each purchase. The budget itself stays in the sheet you control.",
        "category": "money",
        "url": "https://x.ai/bot/JOeuvpFg4v2VAuYX8H0UM",
        "source": "https://x.com/yoshih543/status/2104072319190859796",
    },
    {
        "slug": "media-ledger",
        "name": "Media Ledger",
        "builder": {"name": "Phillip", "x": "phillipstewart"},
        "tagline": "Catalogues the ebooks, games, films and albums you already own.",
        "description": "It builds a running catalogue of your digital purchases (ebooks, audiobooks, games, films, albums) by reading your email receipts, so you can check what you already have before buying the same title twice.",
        "category": "life",
        "url": "https://x.ai/bot/xpZm4ufgAWoCcYPAbugWE",
        "source": "https://x.com/phillipstewart/status/2104066615734104164",
    },
    {
        "slug": "find-good-stocks",
        "name": "Find Good Stocks",
        "builder": {"name": "chen byte", "x": ""},
        "tagline": "Stress-tests a stock thesis against public information, in Chinese.",
        "description": "A Chinese-language research partner for equity ideas. Give it an investment thesis and it sorts the public evidence into supports it, weakens it, or tells you nothing new, with weekly tracking of catalysts and segment data. It states plainly that it gives no buy or sell advice.",
        "category": "money",
        "url": "https://x.ai/bot/2vgMdaQRj4mBWUMygUThf",
        "source": "https://x.com/TSLARKLBTSM/status/2104065607524384822",
    },
    {
        "slug": "provenance",
        "name": "Provenance",
        "builder": {"name": "riesling29", "x": ""},
        "tagline": "Mines event logs for process bottlenecks and separates fact from inference.",
        "description": "A process analyst for event logs. It maps how work actually flows, checks how closely that matches the intended process, points at the bottlenecks, and helps connect the log sources behind the numbers. What it saw in the data is labelled separately from what it is inferring.",
        "category": "productivity",
        "url": "https://x.ai/bot/BVB4ROqmz6xQon8KskyTI",
        "source": "https://x.com/WaterMixing/status/2104177149179760732",
    },
    {
        "slug": "ho-be-gone",
        "name": "Ho Be Gone",
        "builder": {"name": "Jay GPE", "x": ""},
        "tagline": "Blocks scam and spam accounts around your X follows, with a daily undo list.",
        "description": "Account hygiene for X. It blocks scam, impersonator and spam accounts among your followers and the accounts that interact with you, learns from the corrections you make, and sends a short daily list you can undo with one reply.",
        "category": "life",
        "url": "https://x.ai/bot/zM69z4OgdFDSzWcFNsQqx",
        "source": "https://x.com/TheRetardedELon/status/2104149765562957993",
    },
    {
        "slug": "author",
        "name": "Author",
        "builder": {"name": "Oliver Cote", "x": "OliverRCote"},
        "tagline": "A weekly self-authoring coach that keeps a living roadmap of your goals.",
        "description": "A structured writing coach for adults, working through future, then present, then past. It keeps a living roadmap of the goals you write about and checks in weekly so the plan does not quietly stall.",
        "category": "life",
        "url": "https://x.ai/bot/UYdkpfZSu4O6N8_cRXpJO",
        "source": "https://x.com/OliverRCote/status/2104172756782764494",
    },
    {
        "slug": "lyric-guard",
        "name": "Lyric Guard",
        "builder": {"name": "Jerrod Gamotan", "x": ""},
        "tagline": "Checks a song's lyrics against scripture and cites the lines it judges.",
        "description": "A discernment tool for Christian listeners. Send a title and artist, a link, or an audio file and it fetches the lyrics, rates them 1 to 10 for how risky they are to listen to on repeat, and quotes the lines behind the rating. It will not invent lyrics it cannot find.",
        "category": "life",
        "url": "https://x.ai/bot/l4NfEcvgnDxLpDiS2nSH7",
        "source": "https://x.com/soundecclesia/status/2104128291623862434",
    },
]


def main():
    bots = json.load(open(f"{ROOT}/content/bots.json"))
    have_slug = {b["slug"] for b in bots}
    have_url = {b["url"] for b in bots}
    out = []
    for e in ENTRIES:
        slug = e["slug"]
        n = 2
        while slug in have_slug:
            slug = f"{e['slug']}-{n}"
            n += 1
        if e["url"] in have_url:
            print("SKIP (url listed):", e["name"])
            continue
        e["slug"] = slug
        if not re.fullmatch(r"[a-z0-9-]+", slug):
            raise SystemExit(f"bad slug {slug}")
        have_slug.add(slug)
        have_url.add(e["url"])
        if len(e["tagline"]) > 140:
            raise SystemExit(f"tagline too long: {e['slug']} ({len(e['tagline'])})")
        e["addedAt"] = "2026-09-28"
        e["status"] = "published"
        e["builder"] = {k: v for k, v in e["builder"].items() if v}
        out.append(e)
    json.dump(out, open(SCRATCH + "new_entries.json", "w"), ensure_ascii=False, indent=1)
    print("prepared", len(out), "entries")
    for e in out:
        print("  ", e["slug"], "|", e["name"], "|", e["category"], "|", e["builder"], "|", len(e["tagline"]))


if __name__ == "__main__":
    main()
