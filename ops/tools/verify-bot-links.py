#!/usr/bin/env python3
"""Verify x.ai/bot share links live: 200 + extractable name/description."""
import json, re, subprocess, sys, html, concurrent.futures

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"


def fetch(bid):
    url = f"https://x.ai/bot/{bid}"
    r = subprocess.run(['curl', '-sL', '--max-time', '30', '-A', UA, '-w', '\n%{http_code}', url],
                       capture_output=True, text=True)
    raw = r.stdout
    code = raw.rsplit('\n', 1)[-1].strip()
    h = raw.rsplit('\n', 1)[0]
    name = author = desc = title = ''
    m = re.search(r'<h1 title="([^"]*)"[^>]*>', h)
    if m:
        name = html.unescape(m.group(1)).strip()
    else:
        m = re.search(r'<title>(.*?)</title>', h, re.S)
        if m:
            title = html.unescape(m.group(1)).strip()
            name = re.sub(r'\s+by\s+.*$', '', title).strip()
    m = re.search(r'</h1><p class="text-primary text-sm">by\s*([^<]*)</p>', h)
    if m:
        author = html.unescape(m.group(1)).strip()
    m = re.search(r'<p title="([^"]*)" class="text-primary mt-3', h)
    if m:
        desc = html.unescape(m.group(1)).strip()
    if not desc:
        m = re.search(r'<meta property="og:description" content="([^"]*)"', h)
        if m:
            desc = html.unescape(m.group(1)).strip()
    thirdparty = 'created by a third-party user' in h
    ok = code == '200' and bool(name) and (bool(desc) or bool(author))
    return {'bot_id': bid, 'url': url, 'code': code, 'bytes': len(h), 'name': name,
            'author': author, 'desc': desc, 'third_party': thirdparty, 'ok': ok}


if __name__ == '__main__':
    ids = [l.strip() for l in sys.stdin if l.strip()]
    out = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for r in ex.map(fetch, ids):
            out.append(r)
    for r in out:
        print(json.dumps(r, ensure_ascii=False))
    json.dump(out, open('/tmp/verified.json', 'w'), ensure_ascii=False)
