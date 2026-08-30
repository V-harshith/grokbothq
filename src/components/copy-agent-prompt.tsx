"use client";

import { useState } from "react";

const PROMPT = `You are my Grok Bot directory assistant. Fetch the JSON at
https://grokbothq.xyz/api/v1/index.json.

It contains every hand-reviewed Grok bot: name, category, tagline, integrations, install counts, and the x.ai/bot link.

When I describe a task, pick the 3 best-matching bots. For each, give me: name, one-line why it fits, the page link, and the open link. If nothing fits well, say so plainly instead of forcing a match.`;

/**
 * Hero CTA: copies the agent routine to the clipboard. One click and your
 * Grok Bot can read the whole directory - the shortest path from visitor
 * to "this site works for my bot too".
 */
export function CopyAgentPrompt() {
  const [copied, setCopied] = useState(false);

  async function copy() {
    try {
      await navigator.clipboard.writeText(PROMPT);
    } catch {
      /* clipboard blocked - the button still shows where to find it */
    }
    setCopied(true);
    setTimeout(() => setCopied(false), 2400);
  }

  return (
    <button type="button" onClick={copy} className="btn btn-ghost !px-6 !py-3 !text-base">
      {copied ? "Copied - paste it into your Grok Bot" : "Copy the agent prompt"}
    </button>
  );
}
