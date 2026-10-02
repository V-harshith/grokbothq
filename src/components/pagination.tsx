import Link from "next/link";
import { pageHref } from "@/lib/pagination";

export { PAGE_SIZE, pageNumber, pageHref, totalPagesFor } from "@/lib/pagination";

/**
 * Crawlable pagination.
 *
 * The directory hubs used to expose their children only through client-side slicing
 * (`filtered.slice(0, visible)` behind a "Show more" button), so `/bots` — the page carrying ~85% of
 * the site's impressions — passed about 60 real links to 2,524 bot pages, and the rest of the
 * directory was reachable only from `/new` and the category pages. These are plain anchors: every
 * page of the series is reachable and followable without JavaScript.
 */
export function Pagination({
  basePath,
  page,
  totalPages,
  label = "Listings",
}: {
  basePath: string;
  page: number;
  totalPages: number;
  label?: string;
}) {
  if (totalPages <= 1) return null;

  // A window of nearby pages rather than all of them: at 43 pages a full list would be its own
  // link farm, and the first/last plus neighbours is what a reader (and a crawler) uses.
  const window = 2;
  const numbers = new Set<number>([1, totalPages, page]);
  for (let i = 1; i <= window; i += 1) {
    if (page - i >= 1) numbers.add(page - i);
    if (page + i <= totalPages) numbers.add(page + i);
    if (page - i * 5 >= 1 && i === 1) numbers.add(page - 5);
    if (page + i * 5 <= totalPages && i === 1) numbers.add(page + 5);
  }
  const sorted = [...numbers].sort((a, b) => a - b);

  let previous = 0;
  const items: (number | "gap")[] = [];
  for (const n of sorted) {
    if (previous && n - previous > 1) items.push("gap");
    items.push(n);
    previous = n;
  }

  return (
    <nav aria-label={`${label} pagination`} className="mt-8 flex flex-col items-center gap-3">
      <div className="flex flex-wrap items-center justify-center gap-2">
        {page > 1 && (
          <Link href={pageHref(basePath, page - 1)} rel="prev" className="btn btn-ghost">
            ← Previous
          </Link>
        )}
        {items.map((item, i) =>
          item === "gap" ? (
            <span key={`gap-${i}`} className="px-1 text-sm text-muted" aria-hidden>
              …
            </span>
          ) : (
            <Link
              key={item}
              href={pageHref(basePath, item)}
              aria-current={item === page ? "page" : undefined}
              className={`rounded-lg border px-3 py-1.5 text-sm ${
                item === page
                  ? "border-accent bg-accent text-accent-foreground"
                  : "border-border text-muted hover:border-[var(--border-hov)] hover:text-foreground"
              }`}
            >
              {item}
            </Link>
          )
        )}
        {page < totalPages && (
          <Link href={pageHref(basePath, page + 1)} rel="next" className="btn btn-ghost">
            Next →
          </Link>
        )}
      </div>
      <p className="text-xs text-muted">
        Page {page} of {totalPages}
      </p>
    </nav>
  );
}
