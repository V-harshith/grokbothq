/**
 * Route transition wrapper: re-renders on every navigation, giving each page
 * a quick fade-up entrance. Static HTML is identical for crawlers; motion is
 * CSS-only and disabled under prefers-reduced-motion.
 */
export default function Template({ children }: { children: React.ReactNode }) {
  return <div className="page-enter">{children}</div>;
}
