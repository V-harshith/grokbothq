import { ImageResponse } from "next/og";
import { siteStats } from "@/lib/site-stats";
import { SITE } from "@/data/site";

export const alt = "State of Grok Bots - GrokBot HQ directory statistics";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OpengraphImage() {
  const s = siteStats();
  const cells = [
    { label: "Grok bots", value: String(s.totals.bots) },
    { label: "builders", value: String(s.totals.builders) },
    { label: "categories", value: String(s.totals.categories) },
    { label: "reported installs", value: String(s.totals.installs) },
  ];

  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          background: "#050505",
          color: "#f5f5f5",
          padding: "0 90px",
          fontFamily: "sans-serif",
        }}
      >
        <div style={{ display: "flex", fontSize: 26, letterSpacing: 6, color: "#f5f5f5", opacity: 0.6, textTransform: "uppercase" }}>
          STATE OF GROK BOTS
        </div>
        <div style={{ display: "flex", fontSize: 64, fontWeight: 700, marginTop: 18 }}>
          The directory, measured daily
        </div>
        <div style={{ display: "flex", gap: 24, marginTop: 54 }}>
          {cells.map((c) => (
            <div
              key={c.label}
              style={{
                display: "flex",
                flexDirection: "column",
                gap: 8,
                padding: "22px 30px",
                borderRadius: 18,
                border: "1px solid #2a2a2e",
                background: "#101012",
              }}
            >
              <span style={{ fontSize: 52, fontWeight: 700, color: "#f5f5f5" }}>{c.value}</span>
              <span style={{ fontSize: 22, color: "#9c9ca3" }}>{c.label}</span>
            </div>
          ))}
        </div>
        <div style={{ display: "flex", fontSize: 22, color: "#9c9ca3", marginTop: 50 }}>
          grokbothq.xyz/stats · updated {s.updated} · data licensed CC BY 4.0
        </div>
      </div>
    ),
    size
  );
}
