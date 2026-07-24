'use client';

import type { Title } from '@/content/site';
import { cn } from '@/lib/utils';
import { useTitleModal } from '@/components/ui/TitleModal';
import Img from '@/components/ui/Img';

/**
 * A single catalogue card. Images are treated in grayscale for a cohesive,
 * editorial look and bloom into colour on hover. Clicking opens the details.
 */
export default function Card({ title, variant = 'poster' }: { title: Title; variant?: 'poster' | 'wide' }) {
  const { open } = useTitleModal();
  const wide = variant === 'wide';

  return (
    <button
      type="button"
      onClick={() => open(title)}
      aria-label={`${title.title} — details`}
      className={cn(
        'group relative shrink-0 snap-start text-left',
        wide ? 'w-[280px] md:w-[340px]' : 'w-[160px] md:w-[200px]',
      )}
    >
      <div className={cn('relative overflow-hidden rounded-sm bg-panel', wide ? 'aspect-[16/10]' : 'aspect-[3/4]')}>
        <Img
          src={title.poster}
          alt={title.title}
          className="h-full w-full object-cover grayscale transition-[filter,transform] duration-700 ease-out group-hover:scale-[1.04] group-hover:grayscale-0"
          fallback="/placeholder-post-1.svg"
        />
        {/* Thin gold frame appears on hover */}
        <div className="pointer-events-none absolute inset-0 rounded-sm ring-1 ring-inset ring-transparent transition-colors duration-300 group-hover:ring-gold/70" />
        {wide && (
          <>
            <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent" />
            <p className="absolute bottom-3 left-4 right-4 font-display text-xl text-white">{title.title}</p>
          </>
        )}
      </div>

      {!wide && (
        <div className="pt-3">
          <p className="font-display text-lg leading-tight text-ink transition-colors group-hover:text-gold">{title.title}</p>
          <p className="mt-0.5 text-xs uppercase tracking-wide text-faint">{title.meta}</p>
        </div>
      )}
    </button>
  );
}
