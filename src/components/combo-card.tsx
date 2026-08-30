import Link from "next/link";
import type { Combo } from "@/data/combos";
import { comboBots } from "@/data/combos";
import { BotFace } from "./bot-face";

export function ComboCard({ combo }: { combo: Combo }) {
  const bots = comboBots(combo);
  return (
    <article className="card card-hover flex flex-col p-5">
      <div className="flex items-center gap-3">
        <div className="flex -space-x-2.5" aria-hidden>
          {bots.map((b) => (
            <div key={b.slug} className="rounded-lg bg-surface p-0.5 ring-1 ring-border">
              <BotFace slug={b.slug} name={b.name} size={30} />
            </div>
          ))}
        </div>
        <div className="min-w-0">
          <Link href={`/groups/${combo.slug}`} className="block truncate font-semibold hover:text-accent">
            {combo.name}
          </Link>
          <p className="truncate text-xs text-muted">
            {bots.map((b) => b.name).join(" + ")}
          </p>
        </div>
      </div>
      <p className="mt-3 flex-1 text-sm leading-relaxed text-muted">{combo.tagline}</p>
      <Link href={`/groups/${combo.slug}`} className="mt-4 text-xs font-medium text-accent hover:underline">
        See the workflow →
      </Link>
    </article>
  );
}
