"use client";

import { useState } from "react";
import { SITE } from "@/data/site";

const CATEGORIES = [
  "assistants",
  "engineering",
  "research",
  "money",
  "sales",
  "creative",
  "life",
  "productivity",
];

const input =
  "w-full rounded-lg border border-border bg-surface px-3.5 py-2.5 text-sm outline-none placeholder:text-muted focus:border-accent";

export function SubmitForm() {
  const [name, setName] = useState("");
  const [url, setUrl] = useState("");
  const [category, setCategory] = useState("assistants");
  const [pitch, setPitch] = useState("");
  const [instructions, setInstructions] = useState("");
  const [features, setFeatures] = useState("");
  const [bestFor, setBestFor] = useState("");
  const [xHandle, setXHandle] = useState("");

  const githubMode = Boolean(SITE.githubRepo);

  function submit(e: React.FormEvent) {
    e.preventDefault();
    if (githubMode) {
      // Structured submission → GitHub issue → automation turns it into a content PR.
      const params = new URLSearchParams({
        template: "bot-submission.yml",
        title: `Bot submission: ${name}`,
        name,
        url,
        category,
        pitch,
        x_handle: xHandle,
      });
      if (instructions) params.set("instructions", instructions);
      if (features) params.set("features", features);
      if (bestFor) params.set("best_for", bestFor);
      window.location.href = `https://github.com/${SITE.githubRepo}/issues/new?${params.toString()}`;
    } else {
      const subject = `Bot submission: ${name}`;
      const body = `Bot name: ${name}\nx.ai/bot link: ${url}\nCategory: ${category}\nOne-sentence pitch: ${pitch}\nBuilder X: @${xHandle}\n\nSubmitted via ${SITE.domain}`;
      window.location.href = `mailto:${SITE.submitEmail}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    }
  }

  return (
    <form onSubmit={submit} className="card mt-8 grid gap-4 p-6 md:p-8">
      <div className="grid gap-4 md:grid-cols-2">
        <label className="grid gap-1.5 text-sm font-medium">
          Bot name
          <input required value={name} onChange={(e) => setName(e.target.value)} placeholder="e.g. Invoice Hunter" className={input} />
        </label>
        <label className="grid gap-1.5 text-sm font-medium">
          x.ai/bot link
          <input required type="url" value={url} onChange={(e) => setUrl(e.target.value)} placeholder="https://x.ai/bot/your-bot" className={input} />
        </label>
      </div>
      <div className="grid gap-4 md:grid-cols-2">
        <label className="grid gap-1.5 text-sm font-medium">
          Category
          <select value={category} onChange={(e) => setCategory(e.target.value)} className={input}>
            {CATEGORIES.map((c) => (
              <option key={c} value={c}>
                {c.charAt(0).toUpperCase() + c.slice(1)}
              </option>
            ))}
          </select>
        </label>
        <label className="grid gap-1.5 text-sm font-medium">
          Your X handle
          <input value={xHandle} onChange={(e) => setXHandle(e.target.value)} placeholder="yourhandle" className={input} />
        </label>
      </div>
      <label className="grid gap-1.5 text-sm font-medium">
        One-sentence pitch
        <input required value={pitch} onChange={(e) => setPitch(e.target.value)} placeholder="What does it do, and who will love it?" className={input} />
      </label>
      <label className="grid gap-1.5 text-sm font-medium">
        Core instructions <span className="font-normal text-muted">(optional - builds trust, speeds up review)</span>
        <textarea rows={3} value={instructions} onChange={(e) => setInstructions(e.target.value)} placeholder="The persona/rules that power the bot" className={input} />
      </label>
      <div className="grid gap-4 md:grid-cols-2">
        <label className="grid gap-1.5 text-sm font-medium">
          Features <span className="font-normal text-muted">(one per line, optional)</span>
          <textarea rows={3} value={features} onChange={(e) => setFeatures(e.target.value)} placeholder={"Refund claim emails\nRanked by payout ÷ effort"} className={input} />
        </label>
        <label className="grid gap-1.5 text-sm font-medium">
          Best for <span className="font-normal text-muted">(one per line, optional)</span>
          <textarea rows={3} value={bestFor} onChange={(e) => setBestFor(e.target.value)} placeholder={"Freelancers\nAgencies"} className={input} />
        </label>
      </div>
      <button type="submit" className="btn btn-accent justify-self-start !px-6 !py-3">
        {githubMode ? "Submit for review (free)" : "Submit for review (free)"}
      </button>
      <p className="text-xs text-muted">
        {githubMode
          ? "You'll be redirected to a pre-filled submission form. Reviews take about 48 hours; approved bots go live automatically."
          : "This opens your email client with everything pre-filled. Reviews usually take 48 hours."}
        {" "}
        <a href={`mailto:${SITE.submitEmail}?subject=${encodeURIComponent("Bot submission")}`} className="underline underline-offset-2 hover:text-foreground">
          Prefer plain email?
        </a>
      </p>
    </form>
  );
}
