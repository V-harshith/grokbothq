"use client";

import { useEffect } from "react";
import { usePathname } from "next/navigation";

/**
 * Site-wide scroll reveal: elements with [data-reveal] fade/rise in once as
 * they enter the viewport. Re-scans on every route change (client-side
 * navigation renders fresh nodes - without this, navigated-to pages would
 * stay invisible until a hard reload). Transform/opacity only, disabled
 * under prefers-reduced-motion.
 */
export function ScrollReveal() {
  const pathname = usePathname();

  useEffect(() => {
    const els = Array.from(document.querySelectorAll<HTMLElement>("[data-reveal]:not(.reveal-in)"));
    if (!els.length) return;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      els.forEach((el) => el.classList.add("reveal-in"));
      return;
    }

    const io = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            entry.target.classList.add("reveal-in");
            io.unobserve(entry.target);
          }
        }
      },
      // any pixel entering the viewport (minus a 10% strip) reveals -
      // tall sections can never get stuck hidden
      { threshold: 0, rootMargin: "0px 0px -10% 0px" }
    );

    // elements already on screen reveal immediately (navigation to middle of page)
    for (const el of els) {
      const r = el.getBoundingClientRect();
      if (r.top < window.innerHeight && r.bottom > 0) {
        el.classList.add("reveal-in");
      } else {
        io.observe(el);
      }
    }

    return () => io.disconnect();
  }, [pathname]);

  return null;
}
