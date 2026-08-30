import Link from "next/link";
import type { Guide } from "@/data/guides";

export function GuideCard({ guide }: { guide: Guide }) {
  return (
    <article className="card card-hover flex flex-col p-5">
      <div className="flex items-center gap-2 text-xs text-muted">
        <span className="badge">{guide.readingMinutes} min read</span>
        <span>Updated {new Date(guide.updatedAt).toLocaleDateString("en-US", { month: "short", day: "numeric" })}</span>
      </div>
      <h3 className="mt-3 flex-1 text-[15px] font-semibold leading-snug">
        <Link href={`/guides/${guide.slug}`} className="hover:text-accent">
          {guide.title}
        </Link>
      </h3>
      <p className="mt-2 text-sm leading-relaxed text-muted">{guide.description}</p>
    </article>
  );
}
