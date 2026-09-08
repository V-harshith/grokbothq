export function sponsorId(href: string): string {
  if (!/^https?:\/\//i.test(href)) return "house";
  try {
    return new URL(href).hostname.replace(/^www\./, "");
  } catch {
    return "house";
  }
}

export function sponsorHref(href: string): string {
  if (!/^https?:\/\//i.test(href)) return href;
  try {
    const u = new URL(href);
    u.searchParams.set("utm_source", "grokbothq.xyz");
    u.searchParams.set("utm_medium", "referral");
    u.searchParams.set("utm_campaign", "sponsor");
    return u.toString();
  } catch {
    return href;
  }
}
