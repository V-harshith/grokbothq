import { ImageResponse } from "next/og";
import { guideMap } from "@/data/guides";
import { SITE } from "@/data/site";

export const alt = "GrokBot HQ guide";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default async function Image({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const guide = guideMap.get(slug);
  const accent = "#9d9da8";
  const title = guide?.title ?? "Grok Bot Guides";
  const sub = guide?.quickAnswer ?? "How to create, write instructions for, and combine Grok bots";

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
        <span style={{ color: accent }}>&nbsp;· GUIDE</span>
      </div>
      <div
        style={{
          marginTop: 24,
          fontSize: title.length > 32 ? 56 : 72,
          fontWeight: 700,
          maxWidth: 950,
          textAlign: "center",
        }}
      >
        {title}
      </div>
      <div style={{ marginTop: 20, fontSize: 28, color: "#9d9da8", maxWidth: 900, textAlign: "center" }}>
        {sub}
      </div>
      <div style={{ marginTop: 40, fontSize: 26, fontFamily: "monospace", color: "#f5f5f5" }}>
        {`${SITE.domain}/guides/${slug}`}
      </div>
    </div>,
    size
  );
}
