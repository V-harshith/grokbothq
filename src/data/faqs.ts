import type { Faq } from "./types";
import faqsJson from "../../content/faqs.json";

export type { Faq } from "./types";

export const faqs: Faq[] = faqsJson as Faq[];
