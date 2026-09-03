import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { BotCard } from "@/components/bot-card";
import { Breadcrumbs, SectionHeader } from "@/components/ui";
import { JsonLd } from "@/components/json-ld";
import { allIntegrations, integrationBySlug } from "@/lib/integrations";
import { botMap } from "@/data/bots";
import type { Bot } from "@/data/bots";
import { pageMetadata, botListJsonLd, breadcrumbsJsonLd, collectionPageJsonLd } from "@/lib/seo";

type Props = { params: Promise<{ tool: string }> };

export function generateStaticParams() {
  return allIntegrations().map((i) => ({ tool: i.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { tool } = await params;
  const intg = integrationBySlug(tool);
  if (!intg) return {};
  return pageMetadata({
    title: `${intg.count} Grok Bot${intg.count === 1 ? "" : "s"} That Work With ${intg.name}`,
    description: `Every hand-reviewed Grok bot that connects to ${intg.name}. Real listings, tested before they were published - open any of them in Grok with one click.`,
    path: `/integrations/${intg.slug}`,
    keywords: [`grok bots for ${intg.name}`, `${intg.name} grok bot`, `${intg.name} grok integration`],
  });
}

export default async function IntegrationPage({ params }: Props) {
  const { tool } = await params;
  const intg = integrationBySlug(tool);
  if (!intg) notFound();

  const list = intg.bots.map((s) => botMap.get(s)).filter((b): b is Bot => Boolean(b));
  const others = allIntegrations().filter((i) => i.slug !== intg.slug).slice(0, 8);

  return (
    <div className="container-x max-w-5xl py-12">
      <JsonLd
        data={[
          botListJsonLd(list, `/integrations/${intg.slug}`),
          collectionPageJsonLd(`Grok bots that work with ${intg.name}`, `Listed Grok bots connecting to ${intg.name}`, `/integrations/${intg.slug}`),
          breadcrumbsJsonLd([{ name: "Home", path: "/" }, { name: "Integrations", path: "/integrations" }, { name: intg.name, path: `/integrations/${intg.slug}` }]),
        ]}
      />
      <Breadcrumbs items={[{ name: "Home", path: "/" }, { name: "Integrations", path: "/integrations" }, { name: intg.name }]} />

      <header className="max-w-3xl">
        <p className="kicker">Works with</p>
        <h1 className="mt-2 text-3xl md:text-4xl font-semibold tracking-tighter md:text-5xl">
          Grok bots that work with {intg.name}
        </h1>
        <p className="mt-3 text-base leading-relaxed text-muted">
          {list.length === 1
            ? `One hand-reviewed Grok bot connects to ${intg.name}.`
            : `${list.length} hand-reviewed Grok bots connect to ${intg.name}.`}{" "}
          Integration data comes from each bot&apos;s own source listing - open one, connect the tool, and it works.
        </p>
      </header>

      <div className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {list.map((bot) => (
          <BotCard key={bot.slug} bot={bot} />
        ))}
      </div>

      <section className="mt-14">
        <SectionHeader kicker="Keep browsing" title="Other integrations" />
        <div className="flex flex-wrap gap-2">
          {others.map((i) => (
            <Link key={i.slug} href={`/integrations/${i.slug}`} className="badge hover:border-accent hover:text-accent">
              {i.name} {i.count}
            </Link>
          ))}
          <Link href="/bots" className="badge hover:border-accent hover:text-accent">All bots</Link>
        </div>
      </section>
    </div>
  );
}
