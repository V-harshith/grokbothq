import Link from "next/link";
import { SITE } from "@/data/site";
import { ThemeToggle } from "./theme-toggle";

const nav = [
  { href: "/bots", label: "Bots" },
  { href: "/use-cases", label: "Use cases" },
  { href: "/groups", label: "Combos" },
  { href: "/guides", label: "Guides" },
  { href: "/compare", label: "Compare" },
  { href: "/new", label: "New" },
  { href: "/faq", label: "FAQ" },
];

export function Header() {
  return (
    <header className="sticky top-0 z-50 border-b border-border bg-background/70 backdrop-blur-xl backdrop-saturate-150">
      <div className="container-x flex h-14 items-center justify-between gap-4">
        <Link href="/" className="flex items-center gap-2.5 font-semibold tracking-tight" aria-label={`${SITE.name} home`}>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src="/logo.svg" alt="" width={24} height={24} className="rounded-md" />
          <span>
            GrokBot<span className="text-accent">HQ</span>
          </span>
        </Link>

        <nav className="hidden items-center gap-5 md:flex" aria-label="Main">
          {nav.map((item) => (
            <Link key={item.href} href={item.href} className="text-sm text-muted transition-colors hover:text-foreground">
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <ThemeToggle />
          <Link href="/submit" className="btn btn-accent hidden sm:inline-flex">
            Submit a bot
          </Link>
        </div>
      </div>

      {/* mobile nav */}
      <details className="border-t border-border md:hidden">
        <summary className="container-x flex h-10 cursor-pointer list-none items-center text-sm text-muted">
          Menu
        </summary>
        <nav className="container-x grid gap-1 pb-3" aria-label="Mobile">
          {nav.map((item) => (
            <Link key={item.href} href={item.href} className="rounded-md px-2 py-2 text-sm text-muted hover:bg-elevated hover:text-foreground">
              {item.label}
            </Link>
          ))}
          <Link href="/submit" className="btn btn-accent mt-1">
            Submit a bot
          </Link>
        </nav>
      </details>
    </header>
  );
}
