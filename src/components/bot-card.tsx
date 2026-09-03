import Link from "next/link";
import type { Bot } from "@/data/bots";
import { botOpens } from "@/data/bots";
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
  const opens = botOpens(bot.slug);

  return (
    <article className="card card-hover flex flex-col p-5">
      {/* identity row: face + name + handle only - nothing competes with the name */}
      <div className="flex items-start gap-3">
        <BotFace slug={bot.slug} name={bot.name} hue={bot.hue} />
        <div className="min-w-0 flex-1">
          <Link href={`/bots/${bot.slug}`} className="block text-[15px] font-semibold leading-snug hover:text-accent">
            {bot.name}
          </Link>
          {bot.builder.x && (
            <a
              href={`https://x.com/${bot.builder.x}`}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-0.5 block text-xs text-muted hover:text-foreground"
            >
              @{bot.builder.x}
            </a>
          )}
        </div>
      </div>

      <p className="mt-3 flex-1 text-sm leading-relaxed text-muted">{bot.tagline}</p>

      {/* meta row: category + installs + freshness, all with room to breathe */}
      <div className="mt-3 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-muted">
        {category && (
          <Link href={`/bots/category/${category.slug}`} className="hover:text-foreground">
            {category.name}
          </Link>
        )}
        {opens > 0 ? (
          <span title="Opens from GrokBot HQ readers">
            <strong className="tnum font-mono font-semibold text-foreground">{opens}</strong> opens
          </span>
        ) : typeof bot.installs === "number" && bot.installs > 0 && (
          <span title="Installs reported by the source directory">
            <strong className="tnum font-mono font-semibold text-foreground">{bot.installs}</strong> installs
          </span>
        )}
        {fresh && <span className="font-medium text-accent">new · {relDate(bot.addedAt)}</span>}
      </div>

      <div className="mt-4 flex items-center justify-between gap-3">
        <Link
          href={`/bots/${bot.slug}`}
          className="text-xs font-medium text-muted underline-offset-4 hover:text-foreground hover:underline"
        >
          Details
        </Link>
        <OpenButton bot={bot} small />
      </div>
    </article>
  );
}
