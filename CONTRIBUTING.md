# Contributing to GrokBot HQ

Thanks for your interest in improving the directory. Contributions of all sizes are welcome: a one-line data fix is as valuable as a new feature.

## Ways to contribute

| Type | How |
|---|---|
| Submit a bot | [Issue template](https://github.com/V-harshith/grokbothq/issues/new?template=bot-submission.yml) — no PR needed, the pipeline handles the rest |
| Fix or enrich a listing | Edit the entry in `content/bots.json` and open a PR |
| Report a bug | Open an issue with steps to reproduce (or the deployed URL) |
| Change code | Open a PR — see the checklist below |

## Ground rules

- **Content = `content/*.json`.** Bots, categories, combos, guides, comparisons, FAQs, news, and the ad slot are all data. Page code reads the typed loaders in `src/data/*.ts` — don't hardcode content into components.
- **Respect the review bar.** Every listing must be a real, working Grok bot (`https://x.ai/bot/…` URL), with a description that matches what the bot actually does. Misleading descriptions and dead links get delisted.
- **Keep the site static.** No new server dependencies; the directory must keep rebuilding from JSON in seconds.
- **No spam.** The submission validator's blocklist (crypto, casino, SEO services, …) applies to PRs too.

## Code checklist

1. `npm install`
2. `npm run dev` and verify your change in the browser
3. `npm run build` — must pass (CI enforces this on every PR)
4. `npm run lint` — no new warnings

If your change adds a page, make sure it appears in the generated `sitemap.xml` (add it to `src/app/sitemap.ts`) and, where relevant, in the `llms.txt` route list.

## Review process

A maintainer reviews content PRs for accuracy and code PRs for correctness and consistency with the existing patterns. CI must be green before merge. Merges to `main` deploy automatically.

## Licensing

By contributing, you agree that your contributions are licensed under the repository's licenses: code under [MIT](LICENSE) and content under [CC BY 4.0](LICENSE-CONTENT.md).
