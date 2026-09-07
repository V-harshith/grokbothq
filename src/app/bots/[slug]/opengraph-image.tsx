import { ImageResponse } from "next/og";
import { botMap } from "@/data/bots";
import { SITE } from "@/data/site";

export const alt = "GrokBot HQ bot listing";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default async function Image({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const bot = botMap.get(slug);
  const accent = bot?.hue != null ? `hsl(${bot.hue} 80% 60%)` : "#9d9da8";
  const name = bot?.name ?? "Grok bots";
  const sub = bot?.tagline ?? "Hand-reviewed bots on xAI's Grok platform";

  return new ImageResponse(
    <div
      style={{
        width: "100%",
        height: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "#0a0a0b",
        backgroundImage: "radial-gradient(circle at 50% 0%, rgba(255,255,255,0.08), transparent 60%)",
        color: "#f4f4f5",
        fontFamily: "sans-serif",
      }}
    >
      <div
        style={{
          display: "flex",
          fontSize: 34,
          letterSpacing: 6,
          fontWeight: 600,
          color: "#f5f5f5",
        }}
      >
        <span>GROKBOT HQ</span>
        <span style={{ color: accent }}>&nbsp;· BOT</span>
      </div>
      <div
        style={{
          marginTop: 24,
          fontSize: name.length > 20 ? 64 : 84,
          fontWeight: 700,
          maxWidth: 950,
          textAlign: "center",
        }}
      >
        {name}
      </div>
      <div style={{ marginTop: 20, fontSize: 30, color: "#9d9da8", maxWidth: 900, textAlign: "center" }}>
        {sub}
      </div>
      <div style={{ marginTop: 40, fontSize: 26, fontFamily: "monospace", color: "#f5f5f5" }}>
        {`${SITE.domain}/bots/${slug}`}
      </div>
    </div>,
    size
  );
}
