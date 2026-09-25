#!/usr/bin/env python3
"""Read the share record from an x.ai/bot/<id> page via its own og:/canonical meta tags.

Why not the escaped RSC payload: the double-escaped JSON has nulls and
variable field order, so a fixed-order regex over it reports false negatives
(and, if written loosely, swallows the rest of the page). The rendered head is
plain HTML and carries the same facts.

A link counts as a live public template when the page is 200 AND
  og:title is "<Name> by <sharer>" with a non-empty Name that is not the
  platform default ("Grok Bot"), AND the meta description is non-empty,
AND the canonical URL points at the same bot id.

Usage: python3 ops/tools/fetch_share_meta.py id1 id2 ...   (prints JSONL, one per id)
"""
import html
import json
import re
import subprocess
import sys
import concurrent.futures as cf

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")


def meta(body, attr, key):
    m = re.search(r'<meta[^>]+%s="%s"[^>]+content="(.*?)"' % (attr, re.escape(key)), body, re.S)
    if not m:
        m = re.search(r'<meta[^>]+content="(.*?)"[^>]+%s="%s"' % (attr, re.escape(key)), body, re.S)
    return html.unescape(m.group(1)).strip() if m else ""


def fetch(bid):
    url = f"https://x.ai/bot/{bid}"
    rec = {"bot_id": bid, "url": url}
    try:
        p = subprocess.run(["curl", "-sL", "--max-time", "30", "-w", "\n@@%{http_code}", "-A", UA, url],
                           capture_output=True, text=True, timeout=45)
        body = p.stdout
        rec["status"] = body.rsplit("\n@@", 1)[-1].strip()
        title = meta(body, "property", "og:title")
        desc = meta(body, "name", "description")
        canon = meta(body, "rel", "canonical")
        m = re.search(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', body)
        canon = m.group(1) if m else canon
        rec.update({"og_title": title, "desc": desc, "canonical": canon})
        name, sharer = (title.rsplit(" by ", 1) + [""])[:2] if " by " in title else (title, "")
        rec["name"], rec["sharer"] = name.strip(), sharer.strip()
        bad = []
        if rec["status"] != "200":
            bad.append(f"http {rec['status']}")
        if not name.strip() or name.strip().lower() == "grok bot":
            bad.append("no template name (draft/team-only)")
        if not desc:
            bad.append("empty description")
        if bid not in canon:
            bad.append("canonical id mismatch")
        rec["ok"] = not bad
        if bad:
            rec["reason"] = "; ".join(bad)
        return rec
    except Exception as e:  # noqa: BLE001
        rec.update({"ok": False, "reason": f"error {e}"})
        return rec


if __name__ == "__main__":
    ids = sys.argv[1:]
    n_ok = 0
    with cf.ThreadPoolExecutor(max_workers=10) as ex:
        for r in ex.map(fetch, ids):
            print(json.dumps(r, ensure_ascii=False), flush=True)
            n_ok += 1 if r["ok"] else 0
    print(f"checked={len(ids)} live={n_ok}", file=sys.stderr)
