import type { Metadata } from "next";
import Script from "next/script";
import { Analytics } from "@vercel/analytics/next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Header } from "@/components/header";
import { Footer } from "@/components/footer";
import { ScrollReveal } from "@/components/scroll-reveal";
import { SponsorRail } from "@/components/sponsor-rail";
import { AgentNudge } from "@/components/agent-nudge";
import { SiteKeys } from "@/components/site-keys";
import { JsonLd } from "@/components/json-ld";
import { SITE } from "@/data/site";
import { organizationJsonLd, websiteJsonLd } from "@/lib/seo";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL(SITE.url),
  title: {
    default: `${SITE.name} - The Hand-Reviewed Directory of Grok Bots`,
    template: `%s | ${SITE.name}`,
  },
  description: SITE.description,
  applicationName: SITE.name,
  keywords: [
    "grok bots",
    "grok bot directory",
    "best grok bots",
    "xai grok bots",
    "grok bot list",
    "grok bot guides",
    "custom grok assistants",
  ],
  authors: [{ name: SITE.founder, url: SITE.url }],
  creator: SITE.name,
  publisher: SITE.name,
  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true, "max-image-preview": "large", "max-snippet": -1 },
  },
  openGraph: {
    type: "website",
    locale: SITE.locale,
    siteName: SITE.name,
    url: SITE.url,
  },
  twitter: { card: "summary_large_image", site: SITE.twitter },
  formatDetection: { telephone: false },
};

/** Applies the saved theme before first paint to avoid a flash. */
const themeScript = `
try {
  var t = localStorage.getItem('gbh-theme');
  var dark = t ? t === 'dark' : true;
  document.documentElement.classList.toggle('dark', dark);
} catch (e) {}
`;

export default function RootLayout({ children }: LayoutProps<"/">) {
  const umamiUrl = process.env.NEXT_PUBLIC_UMAMI_URL;
  const umamiId = process.env.NEXT_PUBLIC_UMAMI_WEBSITE_ID;
  return (
    <html lang="en" data-scroll-behavior="smooth" className={`${geistSans.variable} ${geistMono.variable} dark h-full antialiased`}>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
        <noscript><style>{`[data-reveal]{opacity:1 !important;transform:none !important}`}</style></noscript>
      </head>
      <body className="flex min-h-full flex-col">
        {umamiUrl && umamiId && (
          <Script defer src={umamiUrl} data-website-id={umamiId} />
        )}
        <JsonLd data={[websiteJsonLd(), organizationJsonLd()]} />
        <ScrollReveal />
        <Header />
        <SponsorRail />
        <AgentNudge />
        <SiteKeys />
        <main className="flex-1">{children}</main>
        <Footer />
        <Analytics />
      </body>
    </html>
  );
}
