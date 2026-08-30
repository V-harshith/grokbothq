import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // the workspace sits inside a parent git repo; pin the root so Turbopack
  // stops warning about an external yarn.lock on every build
  turbopack: {
    root: __dirname,
  },
};

export default nextConfig;
