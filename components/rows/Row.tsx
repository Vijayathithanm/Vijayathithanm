'use client';

import { useRef } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import type { Title } from '@/content/site';
import Card from './Card';

/**
 * A horizontally-scrolling content row with hover arrow controls. Uses native
 * scroll + snap (touch/trackpad friendly); arrows page by ~90% of the viewport.
 */
export default function Row({
  heading,
  items,
  variant = 'poster',
  id,
}: {
  heading: string;
  items: Title[];
  variant?: 'poster' | 'wide';
  id?: string;
}) {
  const track = useRef<HTMLDivElement>(null);

  const page = (dir: 1 | -1) => {
    const el = track.current;
    if (!el) return;
    el.scrollBy({ left: dir * el.clientWidth * 0.9, behavior: 'smooth' });
  };

  return (
    <section id={id} className="reveal group/row relative py-5" aria-label={heading}>
      <div className="mx-auto max-w-content px-4 md:px-8">
        <h2 className="mb-3 font-display text-xl tracking-wide text-ink md:text-2xl">
          {heading}
        </h2>
      </div>

      <div className="relative">
        {/* Arrows (desktop, appear on row hover) */}
        <button
          type="button"
          onClick={() => page(-1)}
          aria-label={`Scroll ${heading} left`}
          className="absolute left-0 top-0 z-20 hidden h-full w-12 items-center justify-center bg-gradient-to-r from-white via-white/80 to-transparent text-ink opacity-0 transition-opacity group-hover/row:opacity-100 md:flex"
        >
          <ChevronLeft size={30} />
        </button>
        <button
          type="button"
          onClick={() => page(1)}
          aria-label={`Scroll ${heading} right`}
          className="absolute right-0 top-0 z-20 hidden h-full w-12 items-center justify-center bg-gradient-to-l from-white via-white/80 to-transparent text-ink opacity-0 transition-opacity group-hover/row:opacity-100 md:flex"
        >
          <ChevronRight size={30} />
        </button>

        <div
          ref={track}
          className="no-scrollbar flex snap-x gap-2.5 overflow-x-auto px-4 pb-2 md:gap-3 md:px-8"
        >
          {items.map((t) => (
            <Card key={t.id} title={t} variant={variant} />
          ))}
        </div>
      </div>
    </section>
  );
}
