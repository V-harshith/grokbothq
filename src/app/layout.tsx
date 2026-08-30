import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Header } from "@/components/header";
import { Footer } from "@/components/footer";
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
    default: `${SITE.name} — The Hand-Reviewed Directory of Grok Bots`,
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
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable} dark h-full antialiased`}>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body className="flex min-h-full flex-col">
        <JsonLd data={[websiteJsonLd(), organizationJsonLd()]} />
        <Header />
        <main className="flex-1">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
