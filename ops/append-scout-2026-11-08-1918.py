#!/usr/bin/env python3
"""2026-11-08 19:18 IST scout pass: append verified bots from grokbots.best rows created 00:14-12:16 UTC today."""
import json, sys

ROOT = "/root/grokbothq"

ENTRIES = [
    {
        "slug": "steady-hand",
        "name": "Steady Hand",
        "builder": {"name": "The Seth", "x": ""},
        "tagline": "Admin help for the first weeks after a spouse dies.",
        "description": "Walks through the paperwork that follows a death: what to ask HR, Social Security, Medicare and insurers, and which bills actually belong to the estate. Its answers are checked against the survivor's state law, and the open questions stay in one list instead of scattered across tabs.",
        "category": "life",
        "source": "https://x.com/the_seth_ard/status/2119061185370771888",
        "features": [
            "Checklist for HR, Social Security and insurers",
            "Sorts which bills are yours",
            "Answers checked against state law",
        ],
    },
    {
        "slug": "swole",
        "name": "Swole",
        "builder": {"name": "Adrian Bisson", "x": ""},
        "tagline": "Quiet fitness and diet coach that reads meals, movement and sleep together.",
        "description": "Tracks meals, movement, weight and sleep in one place, taking photos, screenshots or short notes rather than demanding app connections. The guidance is individualized and deliberately low-noise: it speaks up when the pattern changes, not after every snack.",
        "category": "life",
        "source": "https://x.com/Adrian_Bisson/status/2119390018854896028",
        "features": [
            "Photo and screenshot check-ins",
            "Weight, sleep and movement in one view",
            "No required integrations",
        ],
    },
    {
        "slug": "unl",
        "name": "Unl",
        "builder": {"name": "Neil Mortimer", "x": ""},
        "tagline": "Keeps a record of what you decided and why, then hands the work on.",
        "description": "A decision log with a worker attached. It stores what was chosen and the reasoning behind it, passes that context to a team of bots acting on it, and stays quiet until something needs your call.",
        "category": "productivity",
        "source": "https://x.com/unlimitlessai/status/2119345998887870808",
        "features": [
            "Decision and rationale log",
            "Handoffs that carry the reasoning",
            "Speaks up only when blocked",
        ],
    },
    {
        "slug": "meow-meow",
        "name": "냥냥 (Meow Meow)",
        "builder": {"name": "HEEYEONG EOM", "x": ""},
        "tagline": "Photorealistic cat pictures, one yes at a time.",
        "description": "Generates one photorealistic cat scene per request, then asks whether you want another. Settings and moods vary between images, and the captions and invitations come in whichever language you are using.",
        "category": "creative",
        "source": "https://x.com/heeeeeyeeeeeee/status/2119340222806892658",
        "features": [
            "One image per request, with a check-in",
            "Photorealistic cat scenes",
            "Captions in your language",
        ],
    },
    {
        "slug": "gif-animator",
        "name": "Gif Animator",
        "builder": {"name": "Rob H", "x": ""},
        "tagline": "Turns an image or an idea into a looping GIF you can download.",
        "description": "Animates a still image or a written idea into a looping GIF and hands back a downloadable file. It tries free local animation first and asks before spending on a paid generation.",
        "category": "creative",
        "source": "https://x.com/sia14u/status/2119316699618934901",
        "features": [
            "Image or idea in, GIF out",
            "Downloadable file",
            "Asks before paid generation",
        ],
    },
    {
        "slug": "video-prompter",
        "name": "Video Prompter",
        "builder": {"name": "Ali Nasr", "x": ""},
        "tagline": "Turns an approved story into model-specific video prompts and shot cards.",
        "description": "Takes a signed-off story and visual direction and writes prompts for specific video models, plus shot cards for the sequence. It compares models, plans reference images and lists sourced cost estimates before you spend a credit.",
        "category": "creative",
        "source": "https://x.com/AVAZIFY_AI/status/2119292053074931827",
        "features": [
            "Prompts for named video models",
            "Shot cards for the sequence",
            "Cost estimates with sources",
        ],
    },
    {
        "slug": "sat-nmsqt-tutor",
        "name": "SAT & NMSQT Tutor",
        "builder": {"name": "Arav Jain", "x": ""},
        "tagline": "Test-prep tutor that works from your own practice results.",
        "description": "Goes through digital SAT and PSAT/NMSQT practice tests question by question, explains each miss and drills the topics behind them. It then lays out a study plan sized to the weeks left before test day.",
        "category": "life",
        "source": "https://x.com/aravhawk/status/2119282647834722470",
        "features": [
            "Reviews your practice tests",
            "Drills weak topics",
            "Plan built around your test date",
        ],
    },
    {
        "slug": "viz-explainer",
        "name": "Viz Explainer",
        "builder": {"name": "Adem Vessell", "x": ""},
        "tagline": "Story-driven animated explainers with sourced scripts and MP4 delivery.",
        "description": "Turns a complex topic into a short animated explainer: script first with sources, then a reviewed motion pass, then an MP4. Paid generation is optional, and finished files can go to a private Google Drive folder.",
        "category": "creative",
        "source": "https://x.com/AdemVessell/status/2119281531512648134",
        "features": [
            "Script with sources",
            "Reviewed motion pass",
            "MP4 delivered to Drive",
        ],
    },
    {
        "slug": "omarchy-observer",
        "name": "Omarchy Observer",
        "builder": {"name": "Arne Quanbeck", "x": ""},
        "tagline": "Watches Omarchy Linux for security fixes, releases and add-ons you care about.",
        "description": "Follows Omarchy, DHH's Arch and Hyprland setup, for security issues, major releases, themes and plugins. It filters what it finds against the setup you actually run and pings you only when something touches it.",
        "category": "engineering",
        "source": "https://x.com/lutefiskguy/status/2119224236300755388",
        "features": [
            "Security and release watch",
            "Theme and plugin tracking",
            "Filtered to your setup",
        ],
    },
]

CANDS = {
    "steady-hand": ("WNa0UvXDfvRkZ31PmJ93r", "Admin help for the weeks after a spouse dies: HR, Social Security, Medicare, insurers, and which bills are yours."),
    "swole": ("fmgZ9KSqsMnw3OphM2Vkx", "Low-noise fitness and diet coach that reads meals, movement, weight and sleep together."),
    "unl": ("YmYB34ALYI8LUcrIgnOGA", "Decision and rationale log that hands work to a bot team and reports only when blocked."),
    "meow-meow": ("Vjr1Umod5i2JqpyY46Wrk", "One photorealistic cat image per request, with captions in your language."),
    "gif-animator": ("cab9wr2ZA-h6LW4srwwih", "Turns an image or idea into a looping GIF file; asks before any paid generation."),
    "video-prompter": ("MTrDmZ3SY5rK60ukWAN9m", "Model-specific AI video prompts, shot cards and sourced cost estimates."),
    "sat-nmsqt-tutor": ("M0dW-dTfTPHxAsFTcZe__", "Digital SAT and PSAT/NMSQT tutor that reviews practice tests and builds a plan."),
    "viz-explainer": ("lWk8eIHf8obN-j8ihW6_1", "Sourced scripts to animated explainers, reviewed motion, MP4 delivery."),
    "omarchy-observer": ("C0gOVEOQDiHSzmTz60crI", "Watches Omarchy Linux for security issues, releases, themes and plugins."),
}


def main():
    bots = json.load(open(f"{ROOT}/content/bots.json"))
    have_slugs = {b["slug"] for b in bots}
    have_urls = {b.get("url", "").rstrip("/").lower() for b in bots}
    have_names = {(b.get("name") or "").strip().lower() for b in bots}
    added = []
    for e in ENTRIES:
        sid = CANDS[e["slug"]][0]
        url = f"https://x.ai/bot/{sid}"
        if e["slug"] in have_slugs:
            print(f"skip {e['slug']}: slug taken", file=sys.stderr)
            continue
        if url.lower() in have_urls:
            print(f"skip {e['slug']}: url listed", file=sys.stderr)
            continue
        if e["name"].strip().lower() in have_names:
            print(f"skip {e['slug']}: name listed", file=sys.stderr)
            continue
        entry = {
            "slug": e["slug"],
            "name": e["name"],
            "builder": e["builder"],
            "tagline": e["tagline"],
            "description": e["description"],
            "category": e["category"],
            "url": url,
            "addedAt": "2026-11-08",
            "status": "published",
            "features": e["features"],
            "source": e["source"],
        }
        bots.append(entry)
        added.append(entry)
        have_slugs.add(e["slug"])

    assert len({b["slug"] for b in bots}) == len(bots), "duplicate slug"
    new_urls = [a["url"].lower() for a in added]
    assert len(set(new_urls)) == len(new_urls), "duplicate new url"

    open(f"{ROOT}/content/bots.json", "w").write(json.dumps(bots, ensure_ascii=False, indent=1) + "\n")
    print(f"appended {len(added)}; total {len(bots)}")
    for a in added:
        print(" ", a["slug"], "|", a["url"])


if __name__ == "__main__":
    main()
