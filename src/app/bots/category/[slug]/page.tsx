import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { BotCard } from "@/components/bot-card";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { FaqList } from "@/components/faq-list";
import { JsonLd } from "@/components/json-ld";
import { botsByCategory } from "@/data/bots";
import { categories, categoryMap } from "@/data/categories";
import { combos } from "@/data/combos";
import { comboBots } from "@/data/combos";
import { pageMetadata, botListJsonLd, breadcrumbsJsonLd, faqJsonLd, collectionPageJsonLd } from "@/lib/seo";

type Props = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return categories.map((c) => ({ slug: c.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const category = categoryMap.get(slug);
  if (!category) return {};
  return pageMetadata({
    title: `${category.name} Grok Bots - Hand-Reviewed Picks`,
    description: `The best ${category.name.toLowerCase()} Grok bots, reviewed by hand. ${category.short}. Open any bot in Grok with one click.`,
    path: `/bots/category/${category.slug}`,
  });
}

export default async function CategoryPage({ params }: Props) {
  const { slug } = await params;
  const category = categoryMap.get(slug);
  if (!category) notFound();

  const list = botsByCategory(category.slug);
  const relatedCombos = combos.filter((c) => c.botSlugs.some((s) => list.some((b) => b.slug === s)));

  return (
    <div className="container-x max-w-5xl py-12">
      <JsonLd
        data={[
          botListJsonLd(list, `/bots/category/${category.slug}`),
          collectionPageJsonLd(`${category.name} Grok bots`, category.intro, `/bots/category/${category.slug}`),
          faqJsonLd(category.faqs),
          breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Bots", path: "/bots" }, { name: category.name, path: `/bots/category/${category.slug}` }]),
        ]}
      />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Bots", path: "/bots" }, { name: category.name }]} />

      <header className="max-w-3xl">
        <p className="kicker">Category</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight md:text-4xl">
          {category.name} Grok Bots <span className="font-mono text-xl text-accent">{list.length}</span>
        </h1>
        <p className="mt-3 text-base leading-relaxed text-muted">{category.intro}</p>
      </header>

      <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {list.map((bot) => (
          <BotCard key={bot.slug} bot={bot} />
        ))}
      </div>

      {relatedCombos.length > 0 && (
        <section className="mt-14">
          <SectionHeader kicker="Combos" title={`${category.name} bots that team up well`} />
          <div className="grid gap-3 sm:grid-cols-2">
            {relatedCombos.map((combo) => (
              <Link key={combo.slug} href={`/groups/${combo.slug}`} className="card card-hover flex items-center gap-3 p-4">
                <span className="text-xl" aria-hidden>{combo.emoji}</span>
                <div>
                  <p className="text-sm font-semibold">{combo.name}</p>
                  <p className="text-xs text-muted">{comboBots(combo).map((b) => b.name).join(" + ")}</p>
                </div>
              </Link>
            ))}
          </div>
        </section>
      )}

      <section className="mt-14 max-w-3xl">
        <SectionHeader kicker="FAQ" title={`${category.name} bot questions`} />
        <FaqList faqs={category.faqs} />
      </section>

      <section className="mt-14">
        <SectionHeader kicker="Keep browsing" title="Other categories" />
        <div className="flex flex-wrap gap-2">
          {categories
            .filter((c) => c.slug !== category.slug)
            .map((c) => (
              <Link key={c.slug} href={`/bots/category/${c.slug}`} className="badge hover:border-accent hover:text-accent">
                {c.name}
              </Link>
            ))}
        </div>
      </section>
    </div>
  );
}
