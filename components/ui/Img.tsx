'use client';

import { useState } from 'react';
import { asset, cn } from '@/lib/utils';

/**
 * Image with a guaranteed fallback. `src` is usually a real HD URL from the
 * internet; if it ever fails to load, we swap to a bundled local placeholder
 * so the page never shows a broken image. Both paths run through `asset()`
 * (external URLs pass through untouched; local paths get the base-path prefix).
 */
export default function Img({
  src,
  fallback = '/placeholder-hero-1.svg',
  alt,
  className,
  loading = 'lazy',
}: {
  src: string;
  fallback?: string;
  alt: string;
  className?: string;
  loading?: 'lazy' | 'eager';
}) {
  const [failed, setFailed] = useState(false);
  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={asset(failed ? fallback : src)}
      alt={alt}
      loading={loading}
      onError={() => setFailed(true)}
      className={cn(className)}
    />
  );
}
