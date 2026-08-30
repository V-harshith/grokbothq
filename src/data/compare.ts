import type { ComparePage } from "./types";
import compareJson from "../../content/compare.json";

export const comparePages: ComparePage[] = compareJson as ComparePage[];

export const compareMap = new Map(comparePages.map((c) => [c.slug, c]));
