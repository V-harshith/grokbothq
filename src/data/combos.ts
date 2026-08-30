import { botMap } from "./bots";
import type { Bot, Combo } from "./types";
import combosJson from "../../content/combos.json";

export type { Combo };

export const combos: Combo[] = combosJson as Combo[];

export const comboMap = new Map(combos.map((c) => [c.slug, c]));

export function comboBots(combo: Combo): Bot[] {
  return combo.botSlugs.map((s) => botMap.get(s)).filter((b): b is Bot => Boolean(b));
}
