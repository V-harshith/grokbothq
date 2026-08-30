import Link from "next/link";
import type { Combo } from "@/data/combos";
import { comboBots } from "@/data/combos";

export function ComboCard({ combo }: { combo: Combo }) {
  const bots = comboBots(combo);
  return (
    <article className="card card-hover flex flex-col p-5">
      <div className="flex items-center gap-3">
        <span className="grid h-10 w-10 shrink-0 place-items-center rounded-lg bg-elevated text-xl" aria-hidden>
          {combo.emoji}
        </span>
        <div>
          <Link href={`/groups/${combo.slug}`} className="font-semibold hover:text-accent">
            {combo.name}
          </Link>
          <p className="text-xs text-muted">
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
