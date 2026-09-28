#!/usr/bin/env python3
"""Rotating dead-link audit: sample N published listings and re-fetch each x.ai/bot URL."""
import json, random, re, subprocess, sys, time

REPO = "/root/grokbothq"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
PUSH = re.compile(r'self\.__next_f\.push\(\[1,("(?:[^"\\]|\\.)*")\]\)')

seed = int(sys.argv[1]) if len(sys.argv) > 1 else 2026092720
n = int(sys.argv[2]) if len(sys.argv) > 2 else 28
bots = json.load(open(REPO + "/content/bots.json"))
if isinstance(bots, dict):
    bots = bots["bots"]
pub = [b for b in bots if b.get("status") == "published"]
random.seed(seed)
sample = random.sample(pub, min(n, len(pub)))

dead, renamed, live = [], [], []
for b in sample:
    url = b["url"]
    p = subprocess.run(["curl", "-sL", "--compressed", "--http1.1", "--max-time", "25",
                        "-w", "\n@@%{http_code}", "-A", UA, url],
                       capture_output=True, text=True, timeout=60)
    out = p.stdout
    code = out.rsplit("\n@@", 1)[-1].strip() if "@@" in out else "?"
    p1 = "".join(json.loads(m.group(1)) for m in PUSH.finditer(out))
    m = re.search(r'"botName":"((?:[^"\\]|\\.)*)"', p1)
    name = json.loads('"' + m.group(1) + '"') if m else None
    if code != "200":
        dead.append((b["slug"], url, code))
    elif not name:
        dead.append((b["slug"], url, "200-no-record"))
    else:
        live.append((b["slug"], name))
        if name.strip().lower() != (b["name"] or "").strip().lower():
            renamed.append((b["slug"], b["name"], name))
    time.sleep(0.25)

print(json.dumps({"seed": seed, "sampled": len(sample), "live": len(live),
                  "dead": dead, "renamed": renamed}, ensure_ascii=False, indent=1))
json.dump({"seed": seed, "sampled": len(sample), "live": len(live), "dead": dead, "renamed": renamed},
          open(f"/root/grokbothq/ops/tools/.rotation-{seed}.json", "w"), ensure_ascii=False, indent=1)
