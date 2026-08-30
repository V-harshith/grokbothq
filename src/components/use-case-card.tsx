import Link from "next/link";
import type { Bot } from "@/data/bots";
import { categoryMap } from "@/data/categories";
import { BotFace } from "./bot-face";

/** A real-world usage example: a listed bot plus the X post that introduced it. */
export function UseCaseCard({ bot }: { bot: Bot }) {
  const category = categoryMap.get(bot.category);
  return (
    <article className="card card-hover flex flex-col p-5">
      <div className="flex items-start gap-3">
        <BotFace slug={bot.slug} name={bot.name} />
        <div className="min-w-0">
          <Link href={`/bots/${bot.slug}`} className="font-semibold leading-snug hover:text-accent">
            {bot.name}
          </Link>
          {category && <p className="text-xs text-muted">{category.name}</p>}
        </div>
      </div>
      <p className="mt-3 flex-1 text-sm leading-relaxed text-muted">{bot.tagline}</p>
      <div className="mt-4 flex flex-wrap items-center gap-3 text-xs font-medium">
        <a href={bot.source} target="_blank" rel="noopener noreferrer" className="text-accent hover:underline">
          View the X post
        </a>
        <a href={bot.url} target="_blank" rel="noopener noreferrer nofollow" className="text-muted hover:text-foreground">
          Open the bot
        </a>
      </div>
    </article>
  );
}
