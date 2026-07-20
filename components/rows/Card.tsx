'use client';

import { Play, ChevronDown } from 'lucide-react';
import type { Title } from '@/content/site';
import { cn } from '@/lib/utils';
import { useTitleModal } from '@/components/ui/TitleModal';
import Img from '@/components/ui/Img';

/**
 * A single catalogue card. Hovering scales it up and reveals a quick-actions
 * overlay; clicking opens the details modal. Images are real HD photos with a
 * local fallback (see <Img>).
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
        'group relative shrink-0 snap-start overflow-hidden rounded-lg border border-line bg-panel text-left shadow-sm',
        'transition-transform duration-300 ease-out hover:z-10 hover:scale-[1.06] hover:border-red/40 hover:shadow-xl',
        'focus-visible:z-10 focus-visible:scale-[1.06]',
        wide ? 'w-[280px] md:w-[340px]' : 'w-[150px] md:w-[188px]',
      )}
    >
      <div className={cn('relative overflow-hidden', wide ? 'aspect-video' : 'aspect-[2/3]')}>
        <Img
          src={title.poster}
          alt={title.title}
          className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
          fallback="/placeholder-post-1.svg"
        />

        {title.badge && (
          <span className="absolute left-2 top-2 rounded bg-red px-2 py-0.5 text-[10px] font-bold uppercase tracking-wide text-white shadow">
            {title.badge}
          </span>
        )}

        {/* Hover overlay */}
        <div className="absolute inset-0 flex flex-col justify-end bg-gradient-to-t from-black/85 via-black/20 to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100 group-focus-visible:opacity-100">
          <div className="p-3">
            {wide && <p className="mb-1 line-clamp-1 text-sm font-semibold text-white">{title.title}</p>}
            <div className="flex items-center gap-2">
              <span className="flex h-8 w-8 items-center justify-center rounded-full bg-red text-white">
                <Play size={14} fill="currentColor" />
              </span>
              <span className="flex h-8 w-8 items-center justify-center rounded-full border border-white/70 text-white">
                <ChevronDown size={15} />
              </span>
              <span className="ml-auto text-[11px] font-semibold text-white">{title.meta.split(' · ')[0]}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Caption for posters */}
      {!wide && (
        <div className="px-2 pb-2 pt-2">
          <p className="line-clamp-1 text-sm font-semibold text-ink">{title.title}</p>
          <p className="line-clamp-1 text-xs text-faint">{title.meta}</p>
        </div>
      )}
    </button>
  );
}
