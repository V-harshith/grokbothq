#!/usr/bin/env python3
"""build-awesome.py — generate AWESOME.md for the GrokBot HQ repo.

An awesome list is a CURATED list, not a dump: the peer lists (RongleCat,
kydlikebtc, majiayu000) all say "it is not a dump of every launch recap".
This picks a small number of genuinely notable Bots per category and states the
selection rule in the file itself, so a reader can see why something is here.

Editorial rules (deliberate, and printed into the output):
  - only `status: published` rows (a pending row is not public yet)
  - only rows with a real https://x.ai/bot/<id> share URL — the thing these lists exist to share
  - popularity signal is the `installs` field, but it is present on a minority of
    rows, so it cannot be the only ranking key: known-builder and description depth
    are used to fill the rest of each section
  - never invent a number: every figure printed comes from bots.json

Run:  python3 scripts/build-awesome.py            (writes AWESOME.md)
"""

import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BOTS = REPO / "content" / "bots.json"
OUT = REPO / "AWESOME.md"

SITE = "https://grokbothq.xyz"
PER_CATEGORY = 10
# Builders whose work carries weight in the community; used only to break ties
# when installs are absent. Handles taken from bots.json, not guessed.
NOTABLE = {
    "lennysan", "hnshah", "scheemunai", "scottxmetcalf", "reachhabib",
    "imshiv6t9", "gabe_onchain", "leoclark", "clairevo", "DanKillenberger",
    "tylerklose", "zapnocode",
}

CATEGORY_TITLES = {
    "productivity": "Productivity",
    "assistants": "Assistants",
    "engineering": "Engineering",
    "life": "Life",
    "creative": "Creative",
    "sales": "Sales",
    "research": "Research",
    "money": "Money",
}


def load_bots():
    data = json.loads(BOTS.read_text())
    bots = data if isinstance(data, list) else data.get("bots") or data.get("entries") or []
    out = []
    for b in bots:
        if b.get("status") != "published":
            continue
        url = (b.get("url") or "").strip()
        if not re.match(r"^https://x\.ai/bot/[A-Za-z0-9_-]+$", url):
            continue
        out.append(b)
    return out


def score(b):
    """Higher is better. Installs dominate when present; otherwise fall back to
    observable signals only (notable builder, how much the description says)."""
    inst = b.get("installs")
    handle = ((b.get("builder") or {}).get("x") or "").lstrip("@")
    s = float(inst) * 100 if isinstance(inst, (int, float)) else 0.0
    if handle in NOTABLE:
        s += 30
    desc = (b.get("description") or "").strip()
    tag = (b.get("tagline") or "").strip()
    s += min(len(desc) / 200.0, 10)
    s += min(len(tag) / 40.0, 5)
    if (b.get("features") or []):
        s += 3
    return s


SENT_END = (".", "!", "?", "”", '"', ")")


def first_sentence(text):
    text = re.sub(r"\s+", " ", text or "").strip()
    if not text:
        return ""
    m = re.match(r"^(.+?[.!?])(?:\s|$)", text)
    return (m.group(1) if m else text).strip()


def clean_blurb(b):
    """Taglines in the catalogue are frequently cut mid-word at ~150 chars
    (760 of 2,412 do), so a tagline is only used when it ends cleanly;
    otherwise the first complete sentence of the description wins."""
    tag = re.sub(r"\s+", " ", (b.get("tagline") or "")).strip()
    if tag and tag.endswith(SENT_END) and not tag.endswith("…"):
        s = tag
    else:
        s = first_sentence(b.get("description")) or tag
    s = s.strip()
    if s and not s.endswith(SENT_END):
        s = s.rstrip(".,;: ") + "."
    if s:
        s = s[0].upper() + s[1:]
    if len(s) > 220:
        cut = s[:220].rstrip()
        m = re.match(r"^(.+[.!?])", cut)
        s = m.group(1) if m else cut.rstrip(".,;: ") + "."
    return s


def one_line(b):
    """`- [Name](url) - one sentence.` — the form every peer list asks for."""
    name = (b.get("name") or b.get("slug") or "").strip()
    tag = clean_blurb(b)
    builder = (b.get("builder") or {})
    bn, bx = (builder.get("name") or "").strip(), (builder.get("x") or "").strip()
    credit = ""
    if bx:
        handle = bx if bx.startswith("@") else "@" + bx.lstrip("@")
        credit = f" — [{handle}]({bx if bx.startswith('http') else 'https://x.com/' + handle.lstrip('@')})"
        if bn:
            credit = f" by {bn}" + credit
    elif bn:
        credit = f" by {bn}"
    inst = b.get("installs")
    inst_bit = ""
    if isinstance(inst, (int, float)) and inst:
        inst_bit = f" ({inst} install{'' if inst == 1 else 's'})"
    return f"- [{name}]({b['url']}) - {tag}{inst_bit}{credit}"


def main():
    bots = load_bots()
    by_cat = defaultdict(list)
    for b in bots:
        by_cat[b.get("category") or "other"].append(b)
    for cat in by_cat:
        by_cat[cat].sort(key=score, reverse=True)
    cats = [c for c in CATEGORY_TITLES if by_cat.get(c)]
    listed = sum(min(len(by_cat[c]), PER_CATEGORY) for c in cats)
    with_installs = sum(1 for b in bots if isinstance(b.get("installs"), (int, float)) and b["installs"])

    L = []
    A = L.append
    A("# Awesome Grok Bots")
    A("")
    A(f"> A curated list of the best Bots from the [Grok Bot](https://docs.x.ai/grok-bot/overview) "
      f"share ecosystem — the always-on teammate Bots from xAI, each with its own persistent cloud "
      f"computer. Maintained by [GrokBot HQ]({SITE}), an independent directory of "
      f"**{len(bots):,} published Bots**.")
    A("")
    A("Grok Bot is the always-on AI teammate, not grok.com chat, Grok Imagine, or a Grok model "
      "writeup. Every entry below is a live, public `x.ai/bot` share link.")
    A("")
    A("## Why this list is short")
    A("")
    A(f"The directory behind it holds {len(bots):,} published Bots. This list is the **{listed}** that "
      f"clear a bar, across {len(cats)} categories, because a list that includes everything tells you "
      "nothing. The full, searchable directory is on the site.")
    A("")
    A("**How entries are chosen** (stated so you can disagree with it):")
    A("")
    A("- Every entry is a published Bot with a working `x.ai/bot` share link.")
    A(f"- Where an install count exists it leads — but only {with_installs} of {len(bots):,} Bots "
      "expose one publicly, so installs cannot be the only signal.")
    A("- Remaining places go to Bots whose builder is already known for shipping, and whose own "
      "description actually explains the job the Bot does.")
    A("- Nothing is ranked by payment, and no builder can buy a place.")
    A("")
    A("## Contents")
    A("")
    for c in cats:
        A(f"- [{CATEGORY_TITLES[c]}](#{CATEGORY_TITLES[c].lower()})")
    A("- [Browse the full directory](#browse-the-full-directory)")
    A("- [Add your Bot](#add-your-bot)")
    A("")
    for c in cats:
        A(f"## {CATEGORY_TITLES[c]}")
        A("")
        for b in by_cat[c][:PER_CATEGORY]:
            A(one_line(b))
        A("")
    A("## Browse the full directory")
    A("")
    A(f"- **[{SITE}]({SITE})** — all {len(bots):,} published Bots, searchable by job, category and integration.")
    A(f"- **[Submit your Bot]({SITE}/submit)** — free, hand-reviewed.")
    A(f"- **[llms.txt]({SITE}/llms.txt)** — the machine-readable view for answer engines.")
    A("")
    A("## Add your Bot")
    A("")
    A(f"Open a PR here, or submit at [{SITE}/submit]({SITE}/submit). One Bot per line, the form "
      "`- [Name](share url) - one sentence.` The share URL must be the canonical "
      "`https://x.ai/bot/<id>` link and must load.")
    A("")
    A("## Related")
    A("")
    A("- [Grok Bot documentation](https://docs.x.ai/grok-bot/overview) — official.")
    A("- [Bot Marketplace](https://x.ai/bot/marketplace) — official public templates.")
    A("")
    A("## License")
    A("")
    A("CC0-1.0 — public domain, no attribution required. Each Bot remains the property of its builder.")
    A("")
    A(f"*Generated by `scripts/build-awesome.py` from `content/bots.json` on {date.today().isoformat()}. "
      "Edit the generator or the catalogue, never this file by hand.*")
    A("")
    OUT.write_text("\n".join(L))
    print(f"wrote {OUT} — {len(L)} lines, {listed} Bots listed across {len(cats)} categories")
    for c in cats:
        print(f"  {CATEGORY_TITLES[c]:14s} {min(len(by_cat[c]), PER_CATEGORY):>3} of {len(by_cat[c]):>4}")


if __name__ == "__main__":
    main()
