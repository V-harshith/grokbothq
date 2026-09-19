#!/usr/bin/env python3
"""Scout harvest: collect x.ai/bot/<id> ids from free sources + fxtwitter posts.

Zero paid API calls. Prints JSON summary to stdout.
Usage: python3 ops/tools/scout-harvest.py <repo_root> [--posts posts.json]
"""
import json, os, re, subprocess, sys, time, urllib.request, urllib.error, hashlib

REPO = sys.argv[1] if len(sys.argv) > 1 else "/root/grokbothq"
BOT_RE = re.compile(r"x\.ai/bot/([A-Za-z0-9_-]{10,})")
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def fetch(url, timeout=40, headers=None):
    """curl-based fetch: several of these hosts (Cloudflare) reject bare urllib."""
    cmd = ["curl", "-sL", "--compressed", "--max-time", str(timeout), "-A", UA,
           "-H", "Accept: application/json,text/html,*/*"]
    for k, v in (headers or {}).items():
        cmd += ["-H", f"{k}: {v}"]
    cmd += ["-w", "\n%{http_code}", url]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 15).stdout
    except Exception as e:
        return 0, f"ERR {e}"
    body, _, code = out.rpartition("\n")
    return int(code or 0), body


def ids_in(text):
    return set(m.group(1).rstrip("/").rstrip(".") for m in BOT_RE.finditer(text))


def load_existing():
    known = set()
    for p in ["content/bots.json"]:
        fp = os.path.join(REPO, p)
        if os.path.exists(fp):
            for b in json.load(open(fp)):
                for i in ids_in(b.get("url", "")):
                    known.add(i)
    for p in ["ops/scout-candidates.json", "ops/scout-rejected.json"]:
        fp = os.path.join(REPO, p)
        if os.path.exists(fp):
            try:
                data = json.load(open(fp))
            except Exception:
                continue
            for c in data if isinstance(data, list) else []:
                for i in ids_in(c.get("url", "") or ""):
                    known.add(i)
    qp = os.path.join(REPO, "ops/scout-queue-state.json")
    if os.path.exists(qp):
        try:
            q = json.load(open(qp))
            blob = json.dumps(q)
            known |= ids_in(blob)
        except Exception:
            pass
    return known


def main():
    known = load_existing()
    found = {}  # id -> source

    def add(ids, src):
        for i in ids:
            if i in known:
                continue
            found.setdefault(i, src)

    sources = []
    # Directory catalogs (one fetch each, no hammering)
    for name, url in [
        ("grokbot.dev feed", "https://grokbot.dev/api/v1/feed.json"),
        ("grokbot.dev templates", "https://grokbot.dev/api/v1/templates.json"),
        ("grokbot.dev marketplace", "https://grokbot.dev/marketplace/"),
        ("grokbots.best", "https://grokbots.best/"),
        ("grokbots.page", "https://grokbots.page/"),
        ("chatbottle templates", "https://chatbottle.co/grok-bot-template"),
        ("awesome-grokbot-templates", "https://raw.githubusercontent.com/cs68614-hash/awesome-grokbot-templates/main/data/templates.json"),
        ("awesome-grok-bot catalog", "https://raw.githubusercontent.com/majiayu000/awesome-grok-bot/main/catalog.json"),
    ]:
        st, body = fetch(url)
        ids = ids_in(body)
        add(ids, url)
        sources.append({"source": name, "url": url, "status": st, "bytes": len(body), "ids": len(ids)})

    # X posts via fxtwitter (free, no auth)
    posts = []
    if "--posts" in sys.argv:
        posts = json.load(open(sys.argv[sys.argv.index("--posts") + 1]))
    post_found = {}
    for status_url in posts:
        time.sleep(1.5)
        parts = status_url.rstrip("/").split("/")
        handle, sid = parts[-3], parts[-1]
        st, body = fetch(f"https://api.fxtwitter.com/{handle}/status/{sid}")
        if st == 200 and not body.lstrip().startswith("{"):
            time.sleep(3)
            st, body = fetch(f"https://api.fxtwitter.com/{handle}/status/{sid}")
        if st != 200:
            post_found[status_url] = {"status": st}
            continue
        try:
            j = json.loads(body)
        except Exception:
            post_found[status_url] = {"status": st, "err": "bad json", "raw": body[:200]}
            continue
        t = j.get("tweet", {})
        text = t.get("text", "") or ""
        media = json.dumps(t.get("media", {}) or {})
        ids = ids_in(text) | ids_in(media)
        add(ids, status_url)
        post_found[status_url] = {
            "status": st,
            "handle": (t.get("author") or {}).get("screen_name"),
            "views": t.get("views"),
            "bookmarks": t.get("bookmarks"),
            "likes": t.get("likes"),
            "created": t.get("created_at"),
            "ids": sorted(ids),
            "text_head": text[:400],
        }

    out = {
        "existing_ids": len(known),
        "sources": sources,
        "new_ids": {i: found[i] for i in sorted(found)},
        "new_count": len(found),
        "posts": post_found,
    }
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
