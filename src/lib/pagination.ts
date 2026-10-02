/**
 * Pagination arithmetic for the directory hubs, kept out of the React component so server route
 * handlers (the sitemap) can use the same numbers without pulling the component in.
 */

/** Listings per server-rendered page. 60 keeps each document small and the series crawlable. */
export const PAGE_SIZE = 60;

export function totalPagesFor(count: number, size = PAGE_SIZE): number {
  return Math.max(1, Math.ceil(count / size));
}

/** Parse `?page=`, clamped to the valid range. Returns 1 for anything malformed. */
export function pageNumber(raw: string | string[] | undefined, totalPages: number): number {
  const value = Array.isArray(raw) ? raw[0] : raw;
  const n = Number.parseInt(value ?? "1", 10);
  if (!Number.isFinite(n) || n < 1) return 1;
  return Math.min(n, Math.max(1, totalPages));
}

/** The page's own URL, for a self-referential canonical. */
export function pageHref(basePath: string, page: number): string {
  return page <= 1 ? basePath : `${basePath}?page=${page}`;
}
