'use client';

import dynamic from 'next/dynamic';
import { useState } from 'react';
import { Play, Pause, Info } from 'lucide-react';
import { featured, latestNews, type Title } from '@/content/site';
import { audioEngine } from '@/lib/audio';
import { useTitleModal } from '@/components/ui/TitleModal';
import Img from '@/components/ui/Img';

/* The 3D ribbon is code-split & client-only so it never blocks first paint. */
const HeroCanvas = dynamic(() => import('@/components/three/HeroCanvas'), { ssr: false, loading: () => null });

const featuredTitle: Title = {
  id: 'featured',
  title: featured.title,
  meta: featured.meta,
  description: featured.description,
  poster: featured.backdrop,
  backdrop: featured.backdrop,
  badge: featured.kicker,
};

export default function Hero() {
  const [playing, setPlaying] = useState(false);
  const { open } = useTitleModal();

  const togglePlay = async () => {
    if (playing) {
      audioEngine.pause();
      setPlaying(false);
    } else {
      await audioEngine.play();
      setPlaying(true);
    }
  };

  return (
    <section id="home" className="relative flex min-h-[100svh] items-center overflow-hidden bg-paper" aria-label="Featured">
      {/* HD backdrop, feathered into the white canvas */}
      <div className="absolute inset-y-0 right-0 w-full md:w-[68%]">
        <Img src={featured.backdrop} alt="" loading="eager" className="h-full w-full object-cover" fallback="/placeholder-hero-1.svg" />
        <div className="absolute inset-0 scrim-left" />
        <div className="absolute inset-x-0 bottom-0 h-36 scrim-bottom" />
      </div>

      {/* 3D audio-reactive ribbon floats over the stage */}
      <div className="pointer-events-none absolute inset-0 z-10">
        <HeroCanvas />
      </div>

      {/* Content */}
      <div className="relative z-20 mx-auto w-full max-w-content px-5 pt-24 md:px-12">
        <div className="max-w-2xl reveal">
          <p className="mb-4 flex items-center gap-2 text-sm font-bold uppercase tracking-widest2 text-red">
            <span className="font-display text-lg tracking-normal">N</span> {featured.kicker}
          </p>
          <h1 className="font-display text-6xl leading-[0.92] tracking-wide text-ink sm:text-7xl md:text-8xl">
            {featured.title}
          </h1>
          <p className="mt-3 text-lg font-semibold text-gold md:text-2xl">{featured.tagline}</p>
          <p className="mt-5 max-w-xl text-sm leading-relaxed text-muted md:text-base">
            {featured.description}
          </p>

          <div className="mt-8 flex flex-wrap items-center gap-3">
            <button
              type="button"
              onClick={togglePlay}
              aria-pressed={playing}
              className="flex items-center gap-2 rounded bg-red px-7 py-3 text-base font-bold text-white transition-colors hover:bg-red-dark"
            >
              {playing ? <Pause size={20} fill="currentColor" /> : <Play size={20} fill="currentColor" />}
              {playing ? 'Pause' : 'Play'}
            </button>
            <button
              type="button"
              onClick={() => open(featuredTitle)}
              className="flex items-center gap-2 rounded bg-ink/5 px-7 py-3 text-base font-semibold text-ink ring-1 ring-inset ring-line transition-colors hover:bg-ink/10"
            >
              <Info size={20} /> More Info
            </button>
          </div>
          <p className="mt-3 text-xs text-faint">
            Press Play to let the sound ribbon dance to the score.
          </p>
        </div>
      </div>

      {/* Quality chip */}
      <div className="absolute bottom-24 right-0 z-20 hidden items-center gap-3 border-l-2 border-red bg-paper/70 py-1.5 pl-3 pr-8 text-sm text-ink backdrop-blur-sm md:flex">
        {latestNews.feature.kicker}
      </div>
    </section>
  );
}
