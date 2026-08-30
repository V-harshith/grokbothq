import Link from "next/link";
import type { Bot } from "@/data/bots";
import { categoryMap } from "@/data/categories";
import { BotFace } from "./bot-face";

export function OpenButton({ bot, small }: { bot: Bot; small?: boolean }) {
  return (
    <a
      href={bot.url}
      target="_blank"
      rel="noopener noreferrer nofollow"
      className={`btn btn-accent ${small ? "!px-3 !py-1.5 !text-xs" : ""}`}
      aria-label={`Open ${bot.name} in Grok`}
    >
      Open in Grok
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
        <path d="M7 17 17 7M9 7h8v8" />
      </svg>
    </a>
  );
}

export function BotCard({ bot }: { bot: Bot }) {
  const category = categoryMap.get(bot.category);
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
        <Link href={`/bots/${bot.slug}`} className="text-xs font-medium text-muted underline-offset-4 hover:text-foreground hover:underline">
          Details
        </Link>
        <OpenButton bot={bot} small />
      </div>
    </article>
  );
}
