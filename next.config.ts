import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // the workspace sits inside a parent git repo; pin the root so Turbopack
  // stops warning about an external yarn.lock on every build
  turbopack: {
    root: __dirname,
  },
  // AEO/GEO: plain-text (markdown) variants of key pages. Runs after filesystem
  // routes but before dynamic pages, so /bots/foo.md maps here while /bots/foo
  // still resolves to the bot page.
  async rewrites() {
    return [
      { source: "/bots/:slug([a-z0-9-]+)\\.md", destination: "/md/bots/:slug" },
      { source: "/guides/:slug([a-z0-9-]+)\\.md", destination: "/md/guides/:slug" },
      { source: "/guides\\.md", destination: "/md/guides" },
      { source: "/use-cases\\.md", destination: "/md/use-cases" },
    ];
  },
};

export default nextConfig;
