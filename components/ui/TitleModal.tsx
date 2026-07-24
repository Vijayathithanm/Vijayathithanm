'use client';

import { createContext, useCallback, useContext, useEffect, useState } from 'react';
import { X } from 'lucide-react';
import type { Title } from '@/content/site';
import Img from '@/components/ui/Img';

type Ctx = { open: (t: Title) => void };
const TitleModalContext = createContext<Ctx>({ open: () => {} });

/** Hook used by cards/hero to pop the details modal. */
export const useTitleModal = () => useContext(TitleModalContext);

/**
 * Provides a streaming-style "More Info" modal. Wrap the app once; any child
 * calls `useTitleModal().open(title)`. Closes on Escape / backdrop click and
 * traps page scroll while open.
 */
export function TitleModalProvider({ children }: { children: React.ReactNode }) {
  const [title, setTitle] = useState<Title | null>(null);
  const open = useCallback((t: Title) => setTitle(t), []);
  const close = useCallback(() => setTitle(null), []);

  useEffect(() => {
    if (!title) return;
    const onKey = (e: KeyboardEvent) => e.key === 'Escape' && close();
    document.addEventListener('keydown', onKey);
    document.body.style.overflow = 'hidden';
    return () => {
      document.removeEventListener('keydown', onKey);
      document.body.style.overflow = '';
    };
  }, [title, close]);

  return (
    <TitleModalContext.Provider value={{ open }}>
      {children}
      {title && (
        <div
          className="fixed inset-0 z-[100] flex items-start justify-center overflow-y-auto bg-black/60 p-4 py-10 backdrop-blur-sm"
          role="dialog"
          aria-modal="true"
          aria-label={title.title}
          onClick={close}
        >
          <div
            className="animate-fade-in relative w-full max-w-3xl overflow-hidden rounded-xl border border-line bg-paper shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Media header */}
            <div className="relative aspect-video w-full bg-panel">
              <Img src={title.backdrop ?? title.poster} alt={title.title} className="h-full w-full object-cover" fallback="/placeholder-hero-1.svg" />
              <div className="absolute inset-0 scrim-media" />
              <button
                onClick={close}
                aria-label="Close"
                className="absolute right-4 top-4 flex h-9 w-9 items-center justify-center rounded-full bg-black/60 text-white transition-colors hover:bg-ink"
              >
                <X size={18} />
              </button>
              <div className="absolute bottom-6 left-7 right-7">
                <h2 className="font-display text-5xl font-semibold leading-none text-white drop-shadow-lg md:text-6xl">{title.title}</h2>
              </div>
            </div>
            {/* Details */}
            <div className="p-7 md:p-9">
              <p className="mb-4 text-xs font-semibold uppercase tracking-widest2 text-gold">{title.meta}</p>
              <p className="text-base leading-relaxed text-muted">{title.description}</p>
            </div>
          </div>
        </div>
      )}
    </TitleModalContext.Provider>
  );
}
