import { ImageResponse } from "next/og";

export const alt = "GrokBot HQ - the hand-reviewed directory of Grok bots";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OpengraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          background: "#0a0a0b",
          backgroundImage: "radial-gradient(circle at 50% 0%, rgba(255,255,255,0.08), transparent 60%)",
          color: "#f4f4f5",
          fontFamily: "sans-serif",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 18,
            fontSize: 34,
            letterSpacing: 6,
            color: "#f5f5f5",
            textTransform: "uppercase",
            fontWeight: 600,
          }}
        >
          GROKBOT HQ
        </div>
        <div style={{ display: "flex", fontSize: 76, fontWeight: 700, marginTop: 24, textAlign: "center", maxWidth: 950 }}>
          Find a Grok bot worth opening
        </div>
        <div style={{ display: "flex", fontSize: 30, color: "#9d9da8", marginTop: 28, textAlign: "center", maxWidth: 820 }}>
          The hand-reviewed directory of Grok bots
        </div>
        <div style={{ display: "flex", fontSize: 26, color: "#f5f5f5", marginTop: 40, fontFamily: "monospace" }}>
          grokbothq.xyz
        </div>
      </div>
    ),
    size
  );
}
