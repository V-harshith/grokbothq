import { revalidatePath } from "next/cache";
import { NextRequest, NextResponse } from "next/server";

/**
 * On-demand revalidation gate. After content changes (bot added, delisted,
 * news written), Hermes calls this once and every page regenerates instantly
 * - no redeploy needed.
 *
 *   POST/GET /api/revalidate?secret=<REVALIDATE_TOKEN>
 *
 * Set REVALIDATE_TOKEN in Vercel env vars; requests without the correct
 * secret are rejected with 401.
 */
const TOKEN = process.env.REVALIDATE_TOKEN;

export async function GET(req: NextRequest) {
  return handle(req);
}
export async function POST(req: NextRequest) {
  return handle(req);
}

async function handle(req: NextRequest) {
  const secret = req.nextUrl.searchParams.get("secret");
  if (!TOKEN || secret !== TOKEN) {
    return NextResponse.json({ ok: false, error: "invalid secret" }, { status: 401 });
  }

  // revalidate the whole site (layout-level) - a few hundred fast static paths
  revalidatePath("/", "layout");

  return NextResponse.json({
    ok: true,
    revalidated: "all pages",
    now: new Date().toISOString(),
  });
}
