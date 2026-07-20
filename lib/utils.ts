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
