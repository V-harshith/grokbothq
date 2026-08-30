import Link from "next/link";
import { categories } from "@/data/categories";
import { SITE, DISCLAIMER } from "@/data/site";

export function Footer() {
  return (
    <footer className="border-t border-border bg-surface">
      <div className="container-x grid gap-10 py-12 md:grid-cols-[1.4fr_1fr_1fr_1fr]">
        <div>
          <Link href="/" className="flex items-center gap-2 font-semibold">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src="/logo.svg" alt="" width={22} height={22} className="rounded-md" />
            GrokBot<span className="-ml-1.5 text-accent">HQ</span>
          </Link>
          <p className="mt-3 max-w-xs text-sm leading-relaxed text-muted">
            The independent, hand-reviewed directory of Grok bots. One place to find, combine, and master bots on xAI’s Grok platform.
          </p>
        </div>

        <nav aria-label="Directory">
          <h3 className="text-sm font-semibold">Directory</h3>
          <ul className="mt-3 space-y-2 text-sm text-muted">
            <li><Link href="/bots" className="hover:text-foreground">All bots</Link></li>
            <li><Link href="/new" className="hover:text-foreground">New this week</Link></li>
            <li><Link href="/news" className="hover:text-foreground">Grok news</Link></li>
            <li><Link href="/use-cases" className="hover:text-foreground">Use cases</Link></li>
            <li><Link href="/groups" className="hover:text-foreground">Bot combos</Link></li>
            <li><Link href="/integrations" className="hover:text-foreground">Integrations</Link></li>
            <li><Link href="/submit" className="hover:text-foreground">Submit a bot</Link></li>
            <li><Link href="/featured" className="hover:text-foreground">Sponsor the site</Link></li>
          </ul>
        </nav>

        <nav aria-label="Categories">
          <h3 className="text-sm font-semibold">Categories</h3>
          <ul className="mt-3 space-y-2 text-sm text-muted">
            {categories.slice(0, 6).map((c) => (
              <li key={c.slug}>
                <Link href={`/bots/category/${c.slug}`} className="hover:text-foreground">
                  {c.name} bots
                </Link>
              </li>
            ))}
          </ul>
        </nav>

        <nav aria-label="Learn">
          <h3 className="text-sm font-semibold">Learn</h3>
          <ul className="mt-3 space-y-2 text-sm text-muted">
            <li><Link href="/guides/what-are-grok-bots" className="hover:text-foreground">What are Grok bots?</Link></li>
            <li><Link href="/guides/how-to-create-a-grok-bot" className="hover:text-foreground">Create a Grok bot</Link></li>
            <li><Link href="/agent" className="hover:text-foreground">Point your bot here</Link></li>
            <li><Link href="/compare" className="hover:text-foreground">Grok bots vs the world</Link></li>
            <li><Link href="/faq" className="hover:text-foreground">FAQ</Link></li>
            <li><Link href="/about" className="hover:text-foreground">About</Link></li>
          </ul>
        </nav>
      </div>

      <div className="border-t border-border">
        <div className="container-x flex flex-col gap-2 py-5 text-xs text-muted md:flex-row md:items-center md:justify-between">
          <div>
            <p>
              © {new Date().getFullYear()} {SITE.name}. Last updated{" "}
              {new Date(SITE.lastUpdated).toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })}.
            </p>
            <p className="mt-1">
              Questions? <a href={`mailto:${SITE.email}`} className="underline underline-offset-2 hover:text-foreground">{SITE.email}</a> or{" "}
              <a href={`https://x.com/${SITE.twitter.replace("@", "")}`} target="_blank" rel="noopener noreferrer" className="underline underline-offset-2 hover:text-foreground">
                {SITE.twitter} on X
              </a>
            </p>
          </div>
          <div className="max-w-xl md:text-right">
            <p>{DISCLAIMER}</p>
            <p className="mt-1 space-x-3">
              <Link href="/privacy" className="hover:text-foreground">Privacy</Link>
              <Link href="/terms" className="hover:text-foreground">Terms</Link>
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
