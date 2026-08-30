import type { Faq } from "@/data/faqs";

export function FaqList({ faqs }: { faqs: Faq[] }) {
  return (
    <div className="divide-y divide-border">
      {faqs.map((faq) => (
        <details key={faq.q} className="group py-4">
          <summary className="flex cursor-pointer list-none items-center justify-between gap-4 text-[15px] font-medium [&::-webkit-details-marker]:hidden">
            <h3 className="text-[15px] font-medium">{faq.q}</h3>
            <svg
              className="shrink-0 text-muted transition-transform group-open:rotate-45"
              width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden
            >
              <path d="M12 5v14M5 12h14" />
            </svg>
          </summary>
          <p className="mt-3 max-w-3xl text-sm leading-relaxed text-muted">{faq.a}</p>
        </details>
      ))}
    </div>
  );
}
