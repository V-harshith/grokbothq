"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";

/**
 * The brand link. Same-route click (logo on the homepage while scrolled to
 * the footer) is a no-op in the router - so we scroll to top ourselves.
 */
export function HomeLink({ className, children }: { className?: string; children: ReactNode }) {
  const pathname = usePathname();

  return (
    <Link
      href="/"
      className={className}
      aria-label="GrokBot HQ - back to top"
      onClick={() => {
        if (pathname === "/") {
          window.scrollTo({ top: 0, behavior: "smooth" });
        }
      }}
    >
      {children}
    </Link>
  );
}
