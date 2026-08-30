import type { Category } from "./types";
import categoriesJson from "../../content/categories.json";

export const categories: Category[] = categoriesJson as Category[];

export const categoryMap = new Map(categories.map((c) => [c.slug, c]));
