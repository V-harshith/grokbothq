import Link from "next/link";

export function Breadcrumbs({ items }: { items: { name: string; path?: string }[] }) {
  return (
    <nav aria-label="Breadcrumb" className="mb-6">
      <ol className="flex flex-wrap items-center gap-1.5 text-xs text-muted">
        {items.map((item, i) => (
          <li key={item.path ?? item.name} className="flex items-center gap-1.5">
            {i > 0 && <span aria-hidden>/</span>}
            {item.path ? (
              <Link href={item.path} className="hover:text-foreground">
                {item.name}
              </Link>
            ) : (
              <span className="text-foreground">{item.name}</span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}

export function SectionHeader({
  kicker,
  title,
  description,
  link,
  linkLabel,
}: {
  kicker?: string;
  title: string;
  description?: string;
  link?: string;
  linkLabel?: string;
}) {
  return (
    <div className="mb-8 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
      <div className="max-w-2xl">
        {kicker && <p className="kicker">{kicker}</p>}
        <h2 className="mt-2 text-2xl font-semibold tracking-tight md:text-3xl">{title}</h2>
        {description && <p className="mt-2 text-sm leading-relaxed text-muted">{description}</p>}
      </div>
      {link && (
        <Link href={link} className="btn btn-ghost shrink-0">
          {linkLabel ?? "View all"}
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
            <path d="M5 12h14m-6-6 6 6-6 6" />
          </svg>
        </Link>
      )}
    </div>
  );
}
