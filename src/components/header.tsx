"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
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
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

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
            <Link
              key={item.href}
              href={item.href}
              className={`text-sm transition-colors hover:text-foreground ${pathname === item.href ? "text-foreground" : "text-muted"}`}
            >
              {item.label}
            </Link>
          ))}
        </nav>

        <div className="flex items-center gap-2">
          <ThemeToggle />
          <Link href="/submit" className="btn btn-accent hidden sm:inline-flex">
            List a bot
          </Link>
        </div>
      </div>

      {/* mobile nav */}
      <div className="border-t border-border md:hidden">
        <button
          type="button"
          onClick={() => setOpen((v) => !v)}
          aria-expanded={open}
          className="container-x flex h-10 w-full items-center justify-between text-left text-sm text-muted"
        >
          Menu
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden className={`transition-transform ${open ? "rotate-180" : ""}`}>
            <path d="m6 9 6 6 6-6" />
          </svg>
        </button>
        {open && (
          <nav className="container-x grid gap-1 pb-3" aria-label="Mobile">
            {nav.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setOpen(false)}
                className={`rounded-md px-2 py-2 text-sm hover:bg-elevated hover:text-foreground ${pathname === item.href ? "text-foreground" : "text-muted"}`}
              >
                {item.label}
              </Link>
            ))}
            <Link href="/submit" onClick={() => setOpen(false)} className="btn btn-accent mt-1">
              List a bot
            </Link>
          </nav>
        )}
      </div>
    </header>
  );
}
