export function cn(...classes: (string | false | null | undefined)[]) {
  return classes.filter(Boolean).join(' ');
}

/**
 * Prefix a public asset path with the deployment base path so links work
 * both at the domain root and under a GitHub Pages sub-path (/Vijayathithanm).
 */
export function asset(path: string) {
  const base = process.env.NEXT_PUBLIC_BASE_PATH ?? '';
  return `${base}${path}`;
}

/**
 * Smoothly scroll to an in-page anchor (e.g. "#facets"). Honours
 * `prefers-reduced-motion` by jumping instantly. Returns true if handled.
 */
export function scrollToHash(hash: string): boolean {
  if (typeof document === 'undefined' || !hash.startsWith('#') || hash === '#') return false;
  const el = document.querySelector(hash);
  if (!el) return false;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  el.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
  return true;
}
