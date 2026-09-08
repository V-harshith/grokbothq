"use client";

import type { KeyboardEvent as ReactKeyboardEvent, MouseEvent as ReactMouseEvent, ReactNode } from "react";
import { SITE } from "@/data/site";

const [USER, DOMAIN] = SITE.email.split("@");

function address(to: string): string {
  const [user, domain] = to.split("@");
  return `${user ?? USER}@${domain ?? DOMAIN}`;
}

export function EmailLink({
  to = SITE.email,
  subject,
  className,
  children,
}: {
  to?: string;
  subject?: string;
  className?: string;
  children?: ReactNode;
}) {
  const label = children ?? address(to);
  const open = () => {
    const query = subject ? `?subject=${encodeURIComponent(subject)}` : "";
    window.location.href = `mailto:${address(to)}${query}`;
  };
  return (
    <a
      className={className}
      tabIndex={0}
      role="link"
      onClick={(e: ReactMouseEvent<HTMLAnchorElement>) => {
        e.preventDefault();
        open();
      }}
      onKeyDown={(e: ReactKeyboardEvent<HTMLAnchorElement>) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          open();
        }
      }}
    >
      {label}
    </a>
  );
}
