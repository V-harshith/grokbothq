import type { Guide } from "./types";
import guidesJson from "../../content/guides.json";

export type { Guide, GuideSection } from "./types";

export const guides: Guide[] = guidesJson as Guide[];

export const guideMap = new Map(guides.map((g) => [g.slug, g]));
