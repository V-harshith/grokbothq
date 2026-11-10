#!/usr/bin/env python3
"""Strict re-verification: page botName must equal candidate name; capture creator fields."""
import json, re, sys, urllib.request, html as ihtml, time

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
SCR = "/root/.hermes/cache/scratch"


def get(url, timeout=45):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.getcode(), r.read().decode("utf-8", "replace")


def field(txt, name):
    t = txt.replace('\\"', '"')
    m = re.search(r'"%s"\s*:\s*"((?:[^"\\]|\\.)*)"' % name, t)
    return m.group(1) if m else ""


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def main():
    cands = json.load(open(f"{SCR}/verified-2026-11-10-1445.json"))
    good, bad = [], []
    for c in cands:
        url = f"https://x.ai/bot/{c['bot_id']}"
        try:
            code, body = get(url)
        except Exception as e:
            bad.append({**c, "reason": f"fetch {e}"})
            continue
        bn = field(body, "botName")
        sn = field(body, "sharerName")
        desc = field(body, "description")
        handle = field(body, "sharerHandle") or field(body, "ownerHandle") or field(body, "handle")
        if code != 200:
            bad.append({**c, "reason": f"http {code}"})
        elif norm(bn) != norm(c["name"]):
            bad.append({**c, "reason": f"name mismatch page={bn!r}"})
        else:
            good.append({**c, "page_botName": bn, "page_sharerName": sn,
                         "page_description": ihtml.unescape(desc), "page_handle": handle})
        time.sleep(0.15)
    json.dump(good, open(f"{SCR}/strict-2026-11-10-1445.json", "w"), indent=1, ensure_ascii=False)
    json.dump(bad, open(f"{SCR}/strict-rejects-2026-11-10-1445.json", "w"), indent=1, ensure_ascii=False)
    print(f"strict_ok={len(good)} strict_bad={len(bad)}", file=sys.stderr)
    for b in bad:
        print("BAD", b["bot_id"], b["name"], "|", b["reason"])
    handles = [g for g in good if g["page_handle"]]
    print("pages exposing a handle field:", len(handles), file=sys.stderr)


if __name__ == "__main__":
    main()
