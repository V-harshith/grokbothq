"use client";

import type { ReactNode } from "react";

type Props = {
  href: string;
  event: string;
  data?: Record<string, string | number>;
  className?: string;
  children: ReactNode;
  external?: boolean;
};

/**
 * Link that fires a Umami event on click when analytics are active.
 * No-op otherwise - measurement is always optional, never blocking.
 */
export function TrackedLink({ href, event, data, className, children, external }: Props) {
  function onClick() {
    const w = window as unknown as { umami?: { track: (name: string, data?: object) => void } };
    try {
      w.umami?.track(event, data);
    } catch {
      /* analytics are optional */
    }
  }

  if (external) {
    return (
      <a href={href} target="_blank" rel="noopener noreferrer sponsored" onClick={onClick} className={className}>
        {children}
      </a>
    );
  }
  return (
    <a href={href} onClick={onClick} className={className}>
      {children}
    </a>
  );
}
