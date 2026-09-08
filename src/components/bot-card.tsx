import Link from "next/link";
import type { Bot } from "@/data/bots";
import { botOpens } from "@/data/bots";
import { OpenButton } from "./open-button";

export { OpenButton };

function relDate(iso: string): string {
  const days = Math.floor((Date.now() - new Date(iso).getTime()) / 86_400_000);
  if (days <= 0) return "today";
  if (days === 1) return "yesterday";
  if (days < 7) return `${days}d ago`;
  return new Date(iso).toLocaleDateString("en-US", { month: "short", day: "numeric" });
}

export function BotCard({ bot }: { bot: Bot }) {
  const fresh = Date.now() - new Date(bot.addedAt).getTime() < 7 * 86_400_000;
  const opens = botOpens(bot.slug);
  const installs = typeof bot.installs === "number" ? bot.installs : null;
  const hasMeta = Boolean(bot.builder.x || bot.builder.name) || opens > 0 || (installs !== null && installs > 0);

  return (
    <article className="card card-hover relative flex flex-col gap-3 p-[22px]">
      <div className="flex items-center justify-between gap-[10px]">
        <h3 className="text-base font-medium tracking-[-0.01em]">
          <Link href={`/bots/${bot.slug}`} className="stretched">
            {bot.name}
          </Link>
        </h3>
        <span className="whitespace-nowrap rounded-md border border-border px-2 py-[3px] font-mono text-[10.5px] uppercase tracking-[0.08em] text-muted">
          {bot.category}
        </span>
      </div>

      <p className="flex-1 text-[13.5px] text-muted">
        {bot.tagline}{" "}
        {fresh && <span className="font-medium text-accent">new · {relDate(bot.addedAt)}</span>}
      </p>

      {hasMeta && (
      <div className="flex items-center justify-between border-t border-border pt-3 text-[12.5px] text-muted">
        {bot.builder.x ? (
          <a
            href={`https://x.com/${bot.builder.x}`}
            target="_blank"
            rel="noopener noreferrer"
            className="relative z-10 transition-[color] duration-[180ms] ease-out hover:text-foreground"
          >
            by @{bot.builder.x}
          </a>
        ) : (
          <span>{bot.builder.name}</span>
        )}
        {opens > 0 ? (
          <span title="Opens from GrokBot HQ readers" className="tnum font-mono text-foreground">
            {opens} opens
          </span>
        ) : installs !== null && installs > 0 ? (
          <span title="Installs reported by the source directory" className="tnum font-mono text-foreground">
            {installs} installs
          </span>
        ) : (
          <span />
        )}
      </div>
      )}

      <div className="flex items-center justify-between gap-3">
        <Link
          href={`/bots/${bot.slug}`}
          className="text-xs font-medium text-muted underline-offset-4 hover:text-foreground hover:underline"
        >
          Details
        </Link>
        <span className="relative z-10">
          <OpenButton bot={bot} small />
        </span>
      </div>
    </article>
  );
}
