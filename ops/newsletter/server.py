#!/usr/bin/env python3
"""GrokBot HQ newsletter service.
POST /api/subscribe  {email}  -> stores subscriber in SQLite + notifies owner.
GET  /health                 -> liveness.
GET  /api/subscribers?token=  -> admin listing (owner token, X-Admin-Token header).
VPS port 8333, fronted by Traefik as gbq-news-tb.harshithvelneni.com.
"""
import json, os, sqlite3, re, smtplib, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DB = os.environ.get("GBQ_NEWS_DB", "/data/gbq-newsletter/subscribers.db")
OWNER_EMAIL = os.environ.get("GBQ_OWNER_EMAIL", "harshithwm@gmail.com")
SMTP_HOST = os.environ.get("GBQ_SMTP_HOST", "127.0.0.1")
SMTP_PORT = int(os.environ.get("GBQ_SMTP_PORT", "25"))
ADMIN_TOKEN = os.environ.get("GBQ_ADMIN_TOKEN", "")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

os.makedirs(os.path.dirname(DB), exist_ok=True)

def db():
    c = sqlite3.connect(DB)
    c.execute("CREATE TABLE IF NOT EXISTS subs (email TEXT PRIMARY KEY, ip TEXT, ua TEXT, created TEXT DEFAULT CURRENT_TIMESTAMP)")
    return c

def notify_owner(email):
    """Best-effort SMTP notify to owner via local mail agent (port 25)."""
    try:
        s = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
        msg = f"From: gbq-newsletter@vps.local\r\nTo: {OWNER_EMAIL}\r\nSubject: [GrokBot HQ] new newsletter subscriber\r\n\r\n{email}\r\n"
        s.sendmail("gbq-newsletter@vps.local", [OWNER_EMAIL], msg)
        s.quit()
    except Exception:
        pass  # best-effort; the DB row is the source of truth

class H(BaseHTTPRequestHandler):
    def _json(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "https://grokbothq.xyz")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_OPTIONS(self):
        self._json(204, {})

    def do_GET(self):
        if self.path == "/health":
            self._json(200, {"ok": True})
        elif self.path.startswith("/api/subscribers"):
            if not ADMIN_TOKEN or self.headers.get("X-Admin-Token") != ADMIN_TOKEN:
                self._json(403, {"error": "forbidden"})
                return
            with db() as c:
                rows = c.execute("SELECT email, created FROM subs ORDER BY created DESC").fetchall()
            self._json(200, {"count": len(rows), "subscribers": rows})
        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/api/subscribe":
            self._json(404, {"error": "not found"})
            return
        try:
            n = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            self._json(400, {"error": "bad request"})
            return
        email = (body.get("email") or "").strip().lower()
        if not EMAIL_RE.match(email) or len(email) > 254:
            self._json(400, {"error": "invalid email"})
            return
        with db() as c:
            c.execute("INSERT OR IGNORE INTO subs (email, ip, ua) VALUES (?,?,?)",
                       (email, self.client_address[0], self.headers.get("User-Agent", "")[:200]))
            was_new = c.total_changes > 0
        if was_new:
            threading.Thread(target=notify_owner, args=(email,), daemon=True).start()
        self._json(200, {"ok": True, "new": was_new})

    def log_message(self, *a):
        pass

if __name__ == "__main__":
    # Bind to the docker-bridge gateway: Traefik reaches it via 10.0.0.1,
    # the public internet cannot. Same pattern as AdGuard/LeadVerify host services.
    bind = "10.0.0.1"
    try:
        srv = ThreadingHTTPServer((bind, 8333), H)
    except OSError:
        srv = ThreadingHTTPServer(("0.0.0.0", 8333), H)
    srv.serve_forever()
