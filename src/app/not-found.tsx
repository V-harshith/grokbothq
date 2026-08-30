import Link from "next/link";

export default function NotFound() {
  return (
    <div className="container-x flex max-w-xl flex-col items-center py-28 text-center">
      <p className="kicker">404</p>
      <h1 className="mt-3 text-3xl font-semibold tracking-tight">This bot slipped the net</h1>
      <p className="mt-3 text-sm leading-relaxed text-muted">
        The page you&apos;re looking for doesn&apos;t exist - it may have been a delisted bot or a mistyped link. The
        directory is a click away.
      </p>
      <div className="mt-6 flex gap-3">
        <Link href="/bots" className="btn btn-accent">Browse all bots</Link>
        <Link href="/" className="btn btn-ghost">Go home</Link>
      </div>
    </div>
  );
}
