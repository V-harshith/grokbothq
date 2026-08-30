import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { BotCard } from "@/components/bot-card";
import { Breadcrumbs } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { combos, comboMap, comboBots } from "@/data/combos";
import { pageMetadata, breadcrumbsJsonLd, howToJsonLd } from "@/lib/seo";

type Props = { params: Promise<{ slug: string }> };

export function generateStaticParams() {
  return combos.map((c) => ({ slug: c.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const combo = comboMap.get(slug);
  if (!combo) return {};
  return pageMetadata({
    title: `${combo.name} — ${combo.tagline}`,
    description: `${combo.description} The combo: ${comboBots(combo).map((b) => b.name).join(" + ")}.`,
    path: `/groups/${combo.slug}`,
    type: "article",
    publishedTime: combo.addedAt,
  });
}

export default async function ComboPage({ params }: Props) {
  const { slug } = await params;
  const combo = comboMap.get(slug);
  if (!combo) notFound();

  const bots = comboBots(combo);

  return (
    <div className="container-x max-w-4xl py-12">
      <JsonLd
        data={[
          howToJsonLd(`${combo.name} workflow`, combo.description, combo.steps, combo.addedAt),
          breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Combos", path: "/groups" }, { name: combo.name, path: `/groups/${combo.slug}` }]),
        ]}
      />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Combos", path: "/groups" }, { name: combo.name }]} />

      <header>
        <span className="text-4xl" aria-hidden>{combo.emoji}</span>
        <h1 className="mt-3 text-3xl font-semibold tracking-tight md:text-4xl">{combo.name}</h1>
        <p className="mt-2 text-lg text-muted">{combo.tagline}</p>
      </header>

      <section className="prose-block mt-8">
        <p className="text-[15px] leading-relaxed text-muted">{combo.description}</p>
      </section>

      <section className="mt-10">
        <h2 className="text-xl font-semibold tracking-tight">The workflow</h2>
        <ol className="mt-4 space-y-4">
          {combo.steps.map((step, i) => (
            <li key={step.name} className="card flex gap-4 p-5">
              <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-accent font-mono text-sm font-bold text-accent-foreground" aria-hidden>
                {i + 1}
              </span>
              <div>
                <h3 className="font-semibold">{step.name}</h3>
                <p className="mt-1 text-sm leading-relaxed text-muted">{step.text}</p>
              </div>
            </li>
          ))}
        </ol>
      </section>

      <section className="mt-10">
        <h2 className="text-xl font-semibold tracking-tight">The bots in this combo</h2>
        <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {bots.map((bot) => (
            <BotCard key={bot.slug} bot={bot} />
          ))}
        </div>
      </section>

      <section className="mt-10 card p-6">
        <h2 className="text-lg font-semibold">Best for</h2>
        <div className="mt-3 flex flex-wrap gap-2">
          {combo.bestFor.map((b) => (
            <span key={b} className="badge !normal-case">{b}</span>
          ))}
        </div>
        <p className="mt-4 text-sm leading-relaxed text-muted">
          New to chaining? Read <a href="/guides/how-to-chain-grok-bots" className="text-accent hover:underline">How to Chain Grok Bots</a> for the paste-discipline that makes combos smooth.
        </p>
      </section>
    </div>
  );
}
