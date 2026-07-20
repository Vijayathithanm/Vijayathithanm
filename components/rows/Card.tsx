'use client';

import { Play, ChevronDown } from 'lucide-react';
import type { Title } from '@/content/site';
import { asset, cn } from '@/lib/utils';
import { useTitleModal } from '@/components/ui/TitleModal';

/**
 * A single catalogue card. Hovering scales it up and reveals a quick-actions
 * overlay; clicking (card or the info chevron) opens the details modal.
 */
export default function Card({ title, variant = 'poster' }: { title: Title; variant?: 'poster' | 'wide' }) {
  const { open } = useTitleModal();
  const wide = variant === 'wide';

  return (
    <button
      type="button"
      onClick={() => open(title)}
      aria-label={`${title.title} — more info`}
      className={cn(
        'group relative shrink-0 snap-start overflow-hidden rounded-md border border-transparent bg-panel text-left',
        'transition-transform duration-300 ease-out hover:z-10 hover:scale-[1.06] hover:border-white/15',
        'focus-visible:z-10 focus-visible:scale-[1.06]',
        wide ? 'w-[280px] md:w-[340px]' : 'w-[150px] md:w-[188px]',
      )}
    >
      <div className={cn('relative overflow-hidden', wide ? 'aspect-video' : 'aspect-[2/3]')}>
        {/* SWAP: real artwork — see content/site.ts */}
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={asset(title.poster)}
          alt={title.title}
          loading="lazy"
          className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
        />

        {title.badge && (
          <span className="absolute left-2 top-2 rounded bg-red px-2 py-0.5 text-[10px] font-bold uppercase tracking-wide text-white">
            {title.badge}
          </span>
        )}

        {/* Hover overlay */}
        <div className="absolute inset-0 flex flex-col justify-end bg-gradient-to-t from-black via-black/40 to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100 group-focus-visible:opacity-100">
          <div className="p-3">
            {wide && <p className="mb-1 line-clamp-1 text-sm font-semibold text-white">{title.title}</p>}
            <div className="flex items-center gap-2">
              <span className="flex h-8 w-8 items-center justify-center rounded-full bg-white text-black">
                <Play size={14} fill="currentColor" />
              </span>
              <span className="flex h-8 w-8 items-center justify-center rounded-full border border-white/50 text-white">
                <ChevronDown size={15} />
              </span>
              <span className="ml-auto text-[11px] font-medium text-gold">{title.meta.split(' · ')[0]}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Always-visible caption for posters */}
      {!wide && (
        <div className="px-1 pb-2 pt-2">
          <p className="line-clamp-1 text-sm font-medium text-white">{title.title}</p>
          <p className="line-clamp-1 text-xs text-faint">{title.meta}</p>
        </div>
      )}
    </button>
  );
}
