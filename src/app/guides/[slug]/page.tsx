import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { GuideCard } from "@/components/guide-card";
import { Breadcrumbs } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { guides, guideMap } from "@/data/guides";
import { SITE } from "@/data/site";
import { pageMetadata, breadcrumbsJsonLd, articleJsonLd, howToJsonLd } from "@/lib/seo";

type Props = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return guides.map((g) => ({ slug: g.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const guide = guideMap.get(slug);
  if (!guide) return {};
  return pageMetadata({
    title: guide.seoTitle,
    description: guide.description,
    path: `/guides/${guide.slug}`,
    type: "article",
    publishedTime: guide.updatedAt,
    tags: guide.tags,
  });
}

export default async function GuidePage({ params }: Props) {
  const { slug } = await params;
  const guide = guideMap.get(slug);
  if (!guide) notFound();

  const howTo = guide.sections.find((s) => s.steps);
  const others = guides.filter((g) => g.slug !== guide.slug).slice(0, 3);

  return (
    <div className="container-x max-w-3xl py-12">
      <JsonLd
        data={[
          articleJsonLd({
            title: guide.title,
            description: guide.description,
            path: `/guides/${guide.slug}`,
            dateModified: guide.updatedAt,
            author: SITE.name,
            tags: guide.tags,
          }),
          ...(howTo?.steps ? [howToJsonLd(guide.title, guide.description, howTo.steps, guide.updatedAt)] : []),
          breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Guides", path: "/guides" }, { name: guide.title, path: `/guides/${guide.slug}` }]),
        ]}
      />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Guides", path: "/guides" }, { name: guide.title }]} />

      <article>
        <header>
          <div className="flex items-center gap-2 text-xs text-muted">
            <span className="badge">{guide.readingMinutes} min read</span>
            <span>Updated {new Date(guide.updatedAt).toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })}</span>
          </div>
          <h1 className="mt-3 text-3xl md:text-4xl font-semibold tracking-tighter md:text-5xl">{guide.title}</h1>
        </header>

        {/* Quick answer - optimized for answer engines and AI citations */}
        <section className="card mt-8 border-accent/40 p-5" aria-label="Quick answer">
          <p className="kicker !text-xs">Quick answer</p>
          <p className="mt-2 text-[15px] leading-relaxed">{guide.quickAnswer}</p>
        </section>

        <div className="prose-block mt-10">
          <p className="text-[15px] leading-relaxed text-muted">{guide.intro}</p>
        </div>

        {guide.sections.map((section) => (
          <section key={section.heading} className="mt-10">
            <h2 className="text-xl font-semibold tracking-tight">{section.heading}</h2>
            <div className="prose-block mt-3">
              {(section.body ?? []).map((p) => (
                <p key={p.slice(0, 24)} className="text-[15px] leading-relaxed text-muted">{p}</p>
              ))}
            </div>
            {section.list && (
              <ul className="mt-4 space-y-2">
                {section.list.map((item) => (
                  <li key={item.slice(0, 24)} className="flex items-start gap-2.5 text-[15px] leading-relaxed text-muted">
                    <svg className="mt-1.5 shrink-0 text-accent" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
                      <path d="M20 6 9 17l-5-5" />
                    </svg>
                    {item}
                  </li>
                ))}
              </ul>
            )}
            {section.steps && (
              <ol className="mt-4 space-y-3">
                {section.steps.map((step, i) => (
                  <li key={step.name} className="card flex gap-4 p-4">
                    <span className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-accent font-mono text-xs font-bold text-accent-foreground" aria-hidden>
                      {i + 1}
                    </span>
                    <div>
                      <h3 className="text-sm font-semibold">{step.name}</h3>
                      <p className="mt-1 text-sm leading-relaxed text-muted">{step.text}</p>
                    </div>
                  </li>
                ))}
              </ol>
            )}
          </section>
        ))}
      </article>

      <section className="mt-14 border-t border-border pt-8">
        <h2 className="text-lg font-semibold tracking-tight">Keep reading</h2>
        <div className="mt-4 grid gap-4 sm:grid-cols-3">
          {others.map((g) => (
            <GuideCard key={g.slug} guide={g} />
          ))}
        </div>
        <p className="mt-6 text-sm text-muted">
          Ready to browse? <Link href="/bots" className="text-accent hover:underline">Open the directory</Link>.
        </p>
      </section>
    </div>
  );
}
