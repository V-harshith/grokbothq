import Link from "next/link";
import { EmailLink } from "./email-link";
import { stats } from "@/data/bots";

export function Footer() {
  return (
    <footer className="border-t border-border py-10 pb-14">
      <div className="container-x">
        <div className="flex flex-wrap justify-between gap-8">
          <p className="max-w-[52ch] text-[12.5px] text-muted">
            GrokBot HQ is an independent directory. Not affiliated with xAI. ‘Grok’ is a trademark of xAI, used here descriptively.
          </p>
          <div className="flex flex-wrap gap-5">
            <Link href="/submit" className="text-[12.5px] text-muted transition-[color] duration-[180ms] ease-out hover:text-foreground">
              Submit a bot
            </Link>
            <Link href="/about" className="text-[12.5px] text-muted transition-[color] duration-[180ms] ease-out hover:text-foreground">
              About
            </Link>
            <Link href="/faq" className="text-[12.5px] text-muted transition-[color] duration-[180ms] ease-out hover:text-foreground">
              FAQ
            </Link>
            <EmailLink className="text-[12.5px] text-muted transition-[color] duration-[180ms] ease-out hover:text-foreground">
              hello@grokbothq.xyz
            </EmailLink>
          </div>
        </div>
        <p className="mt-[26px] font-mono text-[11.5px] tracking-[0.02em] text-muted">
          grokbothq.xyz · {stats.bots} bots indexed · every listing opened by hand
        </p>
      </div>
    </footer>
  );
}
