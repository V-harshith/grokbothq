"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { HomeLink } from "./home-link";

const nav = [
  { href: "/bots", label: "Bots" },
  { href: "/use-cases", label: "Use cases" },
  { href: "/guides", label: "Guides" },
  { href: "/agent", label: "Agent" },
  { href: "/compare", label: "Compare" },
  { href: "/news", label: "News" },
];

export function Header() {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-background">
      <div className="container-x flex h-[60px] items-center justify-between gap-4">
        <HomeLink className="text-[15px] font-semibold tracking-[-0.01em]">
          <span>
            GrokBot<span className="font-semibold text-muted">HQ</span>
          </span>
        </HomeLink>

        <nav className="hidden items-center gap-[26px] md:flex" aria-label="Main">
          {nav.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`text-[13.5px] transition-[color] duration-[180ms] ease-out hover:text-foreground ${pathname === item.href ? "text-foreground" : "text-muted"}`}
            >
              {item.label}
            </Link>
          ))}
        </nav>
      </div>

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
          </nav>
        )}
      </div>
    </header>
  );
}
