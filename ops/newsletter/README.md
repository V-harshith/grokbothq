# Newsletter backend (private — do not publish)

Self-hosted subscriber service for the site's "Get the weekly drop" form.
Runs on the VPS as `gbq-newsletter.service` (systemd), bound to 10.0.0.1:8333,
fronted by Coolify's Traefik at `https://gbq-news-tb.harshithvelneni.com`
(non-guessable subdomain by design — the URL itself is the first auth layer).

- `POST /api/subscribe {email}` — CORS locked to grokbothq.xyz, dedupes, notifies owner
- `GET  /api/subscribers` — admin list, requires `X-Admin-Token` (in /data/gbq-newsletter/.env on the VPS)
- `GET  /health`

Vercel env `NEXT_PUBLIC_NEWSLETTER_ENDPOINT` points the site form at this service.
Subscribers DB: /data/gbq-newsletter/subscribers.db (SQLite).
Managed by Hermes (daily ops cron reads subscribers when composing the newsletter).
