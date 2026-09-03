import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Breadcrumbs } from "@/components/ui";
import { FaqList } from "@/components/faq-list";
import { JsonLd } from "@/components/json-ld";
import { comparePages, compareMap } from "@/data/compare";
import { pageMetadata, breadcrumbsJsonLd, articleJsonLd, faqJsonLd, } from "@/lib/seo";
import { SITE } from "@/data/site";

type Props = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return comparePages.map((c) => ({ slug: c.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const page = compareMap.get(slug);
  if (!page) return {};
  return pageMetadata({
    title: page.seoTitle,
    description: page.description,
    path: `/compare/${page.slug}`,
    type: "article",
    publishedTime: page.updatedAt,
    tags: ["grok bots", page.other],
    keywords: [`grok vs ${page.other}`, `grok bots vs ${page.other}`],
  });
}

export default async function CompareDetailPage({ params }: Props) {
  const { slug } = await params;
  const page = compareMap.get(slug);
  if (!page) notFound();

  return (
    <div className="container-x max-w-4xl py-12">
      <JsonLd
        data={[
          faqJsonLd(page.faqs, { dateModified: page.updatedAt }),
          articleJsonLd({ title: page.title, description: page.description, path: `/compare/${page.slug}`, dateModified: page.updatedAt, author: SITE.name }),
          breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Compare", path: "/compare" }, { name: page.title, path: `/compare/${page.slug}` }]),
        ]}
      />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Compare", path: "/compare" }, { name: page.title }]} />

      <article>
        <header>
          <p className="kicker">Comparison</p>
          <h1 className="mt-2 text-3xl md:text-4xl font-semibold tracking-tighter md:text-5xl">{page.title}</h1>
          <p className="mt-2 text-xs text-muted">Updated {new Date(page.updatedAt).toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" })}</p>
        </header>

        <section className="card mt-8 border-accent/40 p-6" aria-label="Verdict">
          <p className="kicker !text-xs">The verdict</p>
          <p className="mt-2 text-[15px] leading-relaxed">{page.verdict.summary}</p>
        </section>

        <section className="mt-10">
          <h2 className="text-xl font-semibold tracking-tight">Side by side</h2>
          <div className="mt-4 overflow-x-auto">
            <table className="w-full min-w-[560px] border-collapse text-sm">
              <thead>
                <tr className="border-b border-border text-left">
                  <th className="py-3 pr-4 font-medium text-muted">Aspect</th>
                  <th className="py-3 pr-4 font-semibold text-accent">Grok Bots</th>
                  <th className="py-3 font-medium text-muted">{page.other}</th>
                </tr>
              </thead>
              <tbody>
                {page.rows.map((row) => (
                  <tr key={row.aspect} className="border-b border-border align-top">
                    <td className="py-3 pr-4 font-medium">{row.aspect}</td>
                    <td className="py-3 pr-4 text-muted">{row.grok}</td>
                    <td className="py-3 text-muted">{row.other}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="mt-10 grid gap-4 md:grid-cols-2">
          <div className="card p-5">
            <h3 className="font-semibold text-accent">Choose Grok bots if…</h3>
            <ul className="mt-3 space-y-2">
              {page.verdict.chooseGrokBots.map((item) => (
                <li key={item.slice(0, 24)} className="flex items-start gap-2 text-sm leading-relaxed text-muted">
                  <svg className="mt-1 shrink-0 text-accent" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden>
                    <path d="M20 6 9 17l-5-5" />
                  </svg>
                  {item}
                </li>
              ))}
            </ul>
          </div>
          <div className="card p-5">
            <h3 className="font-semibold">Choose {page.other} if…</h3>
            <ul className="mt-3 space-y-2">
              {page.verdict.chooseOther.map((item) => (
                <li key={item.slice(0, 24)} className="flex items-start gap-2 text-sm leading-relaxed text-muted">
                  <span className="mt-1 shrink-0 text-muted" aria-hidden>-</span>
                  {item}
                </li>
              ))}
            </ul>
          </div>
        </section>

        {page.sections.map((section) => (
          <section key={section.heading} className="mt-10">
            <h2 className="text-xl font-semibold tracking-tight">{section.heading}</h2>
            <div className="prose-block mt-3">
              {section.body.map((p) => (
                <p key={p.slice(0, 24)} className="text-[15px] leading-relaxed text-muted">{p}</p>
              ))}
            </div>
          </section>
        ))}

        <section className="mt-10 max-w-3xl">
          <h2 className="text-xl font-semibold tracking-tight">FAQ</h2>
          <div className="mt-2">
            <FaqList faqs={page.faqs} />
          </div>
        </section>
      </article>

      <section className="mt-14 border-t border-border pt-8">
        <h2 className="text-lg font-semibold tracking-tight">Next step: find a bot worth opening</h2>
        <div className="mt-4 flex flex-wrap gap-3">
          <Link href="/bots" className="btn btn-accent">Browse the directory</Link>
          <Link href="/compare" className="btn btn-ghost">All comparisons</Link>
        </div>
      </section>
    </div>
  );
}
