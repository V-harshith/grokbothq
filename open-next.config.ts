import { defineCloudflareConfig } from "@opennextjs/cloudflare";

// Default config: pages are built once and served from Workers assets.
// ISR revalidation is a no-op until an incremental cache (R2/KV) is bound.
export default defineCloudflareConfig();
