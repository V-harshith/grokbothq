#!/usr/bin/env python3
"""2026-11-10 14:45 IST scout append: 53 verified bots from grokbots.best Nov 9-10 rows."""
import json, re, unicodedata

ROOT = "/root/grokbothq"
SCR = "/root/.hermes/cache/scratch"
TODAY = "2026-11-10"

# exact-name twins of existing listings -> not added (logged, not pushed)
TWINS = {
    "fHUfj7QKrEt6_QHBDbRwX",   # Forge (existing: DanKillenberger)
    "8IX7glL-Aj73k3I8Q2M__",   # Personal CFO Lite
    "O60Icbx5BlKTkHBCrAgDe",   # X Growth Bot
    "vxICDdg7chCZWnDX6FL0T",   # Inbox Cleanup
    "5Ov0WI-Ad7vtb3yfWT7sP",   # Unstuck
    "b5laG_FLu5mM2XhHgFHGV",   # Usage Optimizer
    "DRdlYas_qcUcMFuhtHMox",   # Marketing Manager
}
# held on editorial grounds
HOLD = {
    "HdP5C0zOBXXRQaUAugAnS": "campaign petition tool; directory stays neutral on political agendas",
}

CAT = {
    "9x8L2b2K8GSlEILhIXt53": "money",
    "XvhWkfMugCBcScHY2TzZ3": "productivity",
    "zqbNleWyIEhz8EoF1TnyB": "life",
    "ZkYt-p7_BweHRkUoqUD_d": "life",
    "SwPnn9g6m32pNIL-NvJ65": "life",
    "KWkMaZUFZmvpp-_xbAVTI": "life",
    "BFu4bKaA8u0LgxqnyCHzC": "productivity",
    "Vui7gf2M2iVLgwAieHJeh": "creative",
    "u1MG6utY3VGmo52GPs7-x": "creative",
    "L4jZ1_tYlmA45l9w6mbiw": "creative",
    "IcxcdVLPyz9jYSMSbrY8h": "creative",
    "7e9Ndk0OiQjuJh3TW4S4-": "creative",
    "VOfh5y4jlFGbZQMxbGsyh": "money",
    "zdBkQ_7mp77gFyt20d3N0": "productivity",
    "wZ0PqEbJCTJizVYNK9Ohs": "engineering",
    "3NyjtdIRmgx38jmpzwgok": "engineering",
    "ffy9_7mBUraesvnoSouFC": "productivity",
    "Z9pFzBV8qhJ9OuzaaD61P": "research",
    "BrbKNtkNv4OTa19Z-2BZy": "sales",
    "m6tmgTZ2-05pAQTZlxo4N": "money",
    "msLKed5U8fgbmAklgMXIb": "life",
    "upxjn-OAkVd4inGzuXkVQ": "life",
    "0f-Z9DWyIAprL_LwFdy3N": "life",
    "XdgOlUq4DUnWxdsARJP0H": "life",
    "QGzcRNttvHwx5SmBdtPz4": "life",
    "sMUSA5hUoMTVv5fLl9HRS": "life",
    "wdX5jvYVioJTtfrSZlf0C": "life",
    "sW-PgV6cP58CPwb7uI5zB": "life",
    "FVf1ZEHebCd4Hk84YYKbr": "life",
    "EVpdEsK65UDSLosfm-nKD": "life",
    "47M19lHzzYvmD8hsqGcvN": "research",
    "YN0Rtn1ZDLjd7TFBOl9aq": "life",
    "2XM4Fx9qncL9CEwM2lJns": "productivity",
    "BpFiwpiSRR3tE55bNkYBO": "productivity",
    "LMtfvwubXj9nqDm9cQXr2": "productivity",
    "OnybhGfwbfR3ahaa6RBwI": "engineering",
    "KXS8-NWpwI0YgR3N__Q-u": "engineering",
    "ZhJV6mmms23wDCds1Foih": "life",
    "DV1Icl-5UdIg_hlLaQRSA": "productivity",
    "8HkaY3kazSO4mRKj35zfG": "research",
    "sYCu3Tox5M_9QWABK2RaF": "engineering",
    "yl1-5MQXPh_X9bt4TMGIk": "sales",
    "ZSCcusHqQECg8-spF-gqc": "creative",
    "CmH_g5v4_0MaKN8tbexdj": "research",
    "oZao5NkFiaZku3eACtTBh": "money",
    "jbfSjKQxfXzNK0XD-MXFv": "sales",
    "9YiGEyzIDGXQeIy2zjXAY": "productivity",
    "N9lHT95-WFHk7t1BgHMFm": "research",
    "onHl-oBaSNXAZAN7h2GHK": "life",
    "Nqt4psehr8wub79l_Z_1k": "engineering",
    "tVI02-lI_WZ-Hv_v_iPF_": "life",
    "Gysg6ozItOXWp_BquycFU": "life",
}

# English rewrites where the page text is not English or too long for a tagline
OVERRIDE = {
    "BrbKNtkNv4OTa19Z-2BZy": (
        "Spanish-language content assistant for X that learns your voice from your own posts.",
        "Learns how you write from your own posts, then sends a daily plan with a ready post, quote-post ideas and replies in Spanish.",
    ),
    "m6tmgTZ2-05pAQTZlxo4N": (
        "Portuguese reminders for Brazil's MEI tax deadlines and rules.",
        "Reminds a Brazilian micro-entrepreneur about the DAS payment and the annual DASN declaration, and explains 2027 deadlines and rules in plain Portuguese with official sources. Does not replace an accountant.",
    ),
    "Nqt4psehr8wub79l_Z_1k": (
        "Korean onboarding bot that sets up a Linux Grok Bot computer for herdr and coding CLIs.",
        "A Korean-language setup bot for a Linux Grok Bot computer: installs herdr, coding CLIs, the GitHub CLI and the Vercel CLI, then walks a Grok newcomer through picking the main orchestrator and signing in to their own accounts so collaboration works right away.",
    ),
    "VOfh5y4jlFGbZQMxbGsyh": (
        "Trading agent with guardrails that runs the open-source mangrove-agent locally.",
        "Runs the open-source mangrove-agent on your own machine for strategy research, backtesting and paper or live trading, with guardrails that keep execution and confirmations under your control.",
    ),
}


def slugify(name):
    s = unicodedata.normalize("NFKD", name)
    s = s.encode("ascii", "ignore").decode()
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "bot"


def first_sentence(text, limit=140):
    t = re.sub(r"\s+", " ", (text or "").strip())
    m = re.match(r"(.+?[.!?])(\s|$)", t)
    cand = m.group(1) if m else t
    if len(cand) > limit:
        cut = cand[:limit]
        cut = cut[: cut.rfind(" ")].rstrip(" ,;:-")
        cand = cut
    return cand


def main():
    bots = json.load(open(f"{ROOT}/content/bots.json"))
    have_urls = {b.get("url", "").lower() for b in bots}
    have_slugs = {b["slug"] for b in bots}
    good = json.load(open(f"{SCR}/strict-2026-11-10-1445.json"))
    good.sort(key=lambda g: g.get("created_at", ""), reverse=True)

    added, skipped = [], []
    for g in good:
        bid = g["bot_id"]
        if bid in TWINS:
            skipped.append({"name": g["name"], "bot_id": bid, "reason": "exact name twin of an existing listing"})
            continue
        if bid in HOLD:
            skipped.append({"name": g["name"], "bot_id": bid, "reason": HOLD[bid]})
            continue
        url = f"https://x.ai/bot/{bid}"
        if url.lower() in have_urls:
            skipped.append({"name": g["name"], "bot_id": bid, "reason": "url already listed"})
            continue
        cat = CAT.get(bid)
        if not cat:
            skipped.append({"name": g["name"], "bot_id": bid, "reason": "no category assigned"})
            continue
        name = g["name"]
        tag, desc = OVERRIDE.get(bid, (None, None))
        if not tag:
            tag = first_sentence(g["page_description"])
            desc = re.sub(r"\s+", " ", g["page_description"]).strip()
        slug = slugify(name)
        base, n = slug, 2
        while slug in have_slugs:
            slug = f"{base}-{n}"
            n += 1
        have_slugs.add(slug)
        have_urls.add(url.lower())
        entry = {
            "slug": slug,
            "name": name,
            "builder": {"name": g.get("page_sharerName") or "", "x": ""},
            "tagline": tag,
            "description": desc,
            "category": cat,
            "url": url,
            "addedAt": TODAY,
            "status": "published",
            "source": g.get("gb_source") or "",
        }
        added.append(entry)

    bots.extend(added)
    json.dump(bots, open(f"{ROOT}/content/bots.json", "w"), indent=1, ensure_ascii=False)
    json.dump({"added": added, "skipped": skipped}, open(f"{SCR}/added-2026-11-10-1445.json", "w"),
              indent=1, ensure_ascii=False)
    print(f"added={len(added)} skipped={len(skipped)} total={len(bots)}")
    for s in skipped:
        print(" skip:", s["name"], "-", s["reason"])
    for a in added:
        print(f" {a['slug']} | {a['name']} | {a['category']} | {a['tagline'][:70]}")


if __name__ == "__main__":
    main()
