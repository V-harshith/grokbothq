"use client";

import { useState } from "react";
import { SITE } from "@/data/site";

/**
 * Weekly newsletter signup. With NEXT_PUBLIC_NEWSLETTER_ENDPOINT set (e.g. a
 * Buttondown/Loops/Formspree URL) it POSTs the email there; without it, the
 * button composes a subscribe email - so the form works on day one.
 */
export function NewsletterForm() {
  const [email, setEmail] = useState("");
  const [done, setDone] = useState<"idle" | "sent" | "check-app">("idle");
  const endpoint = process.env.NEXT_PUBLIC_NEWSLETTER_ENDPOINT;

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    if (endpoint) {
      try {
        await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email }),
        });
      } catch {
        /* the success state below is optimistic either way */
      }
      setDone("sent");
    } else {
      window.location.href = `mailto:${SITE.email}?subject=${encodeURIComponent("Newsletter signup")}&body=${encodeURIComponent(email)}`;
      setDone("check-app");
    }
  }

  if (done !== "idle") {
    return (
      <p className="text-sm leading-relaxed text-muted" role="status">
        {done === "sent" ? "You're on the list. See you next week." : "Opening your email app to finish the signup."}
      </p>
    );
  }

  return (
    <form onSubmit={submit} className="flex flex-col gap-2 sm:flex-row sm:justify-center">
      <input
        required
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="you@example.com"
        aria-label="Email address"
        className="w-full rounded-full border border-border bg-surface px-4 py-2.5 text-sm outline-none placeholder:text-muted focus:border-accent sm:w-72"
      />
      <button type="submit" className="btn btn-accent shrink-0">
        Get the weekly drop
      </button>
    </form>
  );
}
