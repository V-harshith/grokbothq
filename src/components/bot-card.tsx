import Link from "next/link";
import type { Bot } from "@/data/bots";
import { categoryMap } from "@/data/categories";
import { BotFace } from "./bot-face";
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
  const category = categoryMap.get(bot.category);
  const fresh = Date.now() - new Date(bot.addedAt).getTime() < 7 * 86_400_000;
  return (
    <article className="card card-hover flex flex-col p-5">
      <div className="flex items-start justify-between gap-3">
        <div className="flex min-w-0 items-start gap-3">
          <BotFace slug={bot.slug} name={bot.name} />
          <div className="min-w-0">
            <div className="flex flex-wrap items-center gap-2">
              <Link href={`/bots/${bot.slug}`} className="truncate text-base font-semibold hover:text-accent">
                {bot.name}
              </Link>
              {bot.trending && <span className="badge badge-accent">Trending</span>}
            </div>
            {bot.builder.x && (
              <p className="mt-0.5 text-xs text-muted">
                by{" "}
                <a href={`https://x.com/${bot.builder.x}`} target="_blank" rel="noopener noreferrer" className="hover:text-foreground">
                  @{bot.builder.x}
                </a>
              </p>
            )}
          </div>
        </div>
        {category && (
          <Link href={`/bots/category/${category.slug}`} className="badge shrink-0 hover:text-accent">
            {category.name}
          </Link>
        )}
      </div>

      <p className="mt-3 flex-1 text-sm leading-relaxed text-muted">{bot.tagline}</p>

      <div className="mt-4 flex items-center justify-between gap-3">
        <div className="flex items-center gap-2.5 text-xs text-muted">
          <Link href={`/bots/${bot.slug}`} className="font-medium underline-offset-4 hover:text-foreground hover:underline">
            Details
          </Link>
          {typeof bot.installs === "number" && bot.installs > 0 && (
            <span title="Installs reported by the source directory">
              <strong className="font-mono font-semibold text-foreground">{bot.installs}</strong> installs
            </span>
          )}
          {fresh && <span className="badge-accent rounded-full px-2 py-0.5 font-semibold">new · {relDate(bot.addedAt)}</span>}
        </div>
        <OpenButton bot={bot} small />
      </div>
    </article>
  );
}
