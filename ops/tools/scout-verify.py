#!/usr/bin/env python3
"""Scout verify: confirm x.ai/bot/<id> pages are live AND that the bot name
actually appears in the page body (a 200 alone is not proof — x.ai serves a
generic shell for unknown ids on some paths).

Usage:
  python3 ops/tools/scout-verify.py candidates.json            # verify + report
  candidates.json = [{name, url, builder_x_handle, one_line_desc, source_post_url}]

Prints JSON list of verified candidates (with `verified: true` and the page
title) to stdout. Nothing is written to disk.
"""
import json, re, subprocess, sys, time

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")
BOT_ID = re.compile(r"x\.ai/bot/([A-Za-z0-9_-]{10,})")


def curl(url, timeout=45):
    cmd = ["curl", "-sL", "--compressed", "--max-time", str(timeout), "-A", UA,
           "-w", "\n%{http_code}", url]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True,
                             timeout=timeout + 15).stdout
    except Exception as e:
        return 0, f"ERR {e}"
    body, _, code = out.rpartition("\n")
    return int(code or 0), body


def norm(s):
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def main():
    cands = json.load(open(sys.argv[1]))
    verified, failed = [], []
    for c in cands:
        url = c["url"]
        st, body = curl(url)
        title = ""
        m = re.search(r"<title>(.*?)</title>", body, re.S)
        if m:
            title = re.sub(r"\s+", " ", m.group(1)).strip()
        name = c.get("name", "")
        name_ok = bool(name) and norm(name) in norm(body)
        title_ok = bool(title) and norm(name.split(" by ")[0]) in norm(title)
        if st == 200 and (name_ok or title_ok):
            c = dict(c, verified=True, page_title=title, http_status=st)
            verified.append(c)
        else:
            failed.append({"url": url, "name": name, "http_status": st,
                           "page_title": title, "name_in_body": name_ok,
                           "bytes": len(body)})
        time.sleep(1.2)
    print(json.dumps({"verified": verified, "failed": failed}, indent=1))


if __name__ == "__main__":
    main()
