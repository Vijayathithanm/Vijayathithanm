'use client';

import dynamic from 'next/dynamic';
import { useState } from 'react';
import { Play, Pause, Music2 } from 'lucide-react';
import { featured, hero } from '@/content/site';
import { audioEngine } from '@/lib/audio';
import { scrollToHash } from '@/lib/utils';
import Img from '@/components/ui/Img';

/* The 3D ribbon is code-split & client-only so it never blocks first paint. */
const HeroCanvas = dynamic(() => import('@/components/three/HeroCanvas'), { ssr: false, loading: () => null });

export default function Hero() {
  const [playing, setPlaying] = useState(false);

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
    <section id="home" className="relative flex min-h-[100svh] items-center overflow-hidden bg-paper" aria-label="Introduction">
      {/* HD portrait, treated in grayscale and feathered into the page */}
      <div className="absolute inset-y-0 right-0 w-full md:w-[62%]">
        <Img
          src={featured.backdrop}
          alt="Ilaiyaraaja in concert"
          loading="eager"
          className="h-full w-full object-cover grayscale [filter:grayscale(1)_contrast(1.05)]"
          fallback="/placeholder-hero-1.svg"
        />
        <div className="absolute inset-0 scrim-left" />
        <div className="absolute inset-x-0 bottom-0 h-40 scrim-bottom" />
      </div>

      {/* Sound ribbon */}
      <div className="pointer-events-none absolute inset-0 z-10">
        <HeroCanvas />
      </div>

      {/* Content */}
      <div className="relative z-20 mx-auto w-full max-w-content px-6 pt-24 md:px-12">
        <div className="max-w-2xl reveal">
          <p className="mb-6 flex items-center gap-2 text-xs font-semibold uppercase tracking-widest2 text-gold">
            <Music2 size={15} aria-hidden /> Isaignani · The Maestro
          </p>
          <h1 className="font-display text-7xl font-semibold leading-[0.95] text-ink sm:text-8xl md:text-[7.5rem]">
            {featured.title}
          </h1>
          <p className="mt-5 max-w-xl font-display text-2xl italic text-muted md:text-3xl">
            A life measured in melodies.
          </p>
          <p className="mt-6 max-w-lg text-sm leading-relaxed text-muted md:text-base">
            {hero.subtitle}
          </p>

          <div className="mt-10 flex flex-wrap items-center gap-6">
            <button
              type="button"
              onClick={togglePlay}
              aria-pressed={playing}
              className="flex items-center gap-3 rounded-full bg-ink px-7 py-3 text-sm font-medium text-white transition-colors hover:bg-black"
            >
              {playing ? <Pause size={16} fill="currentColor" /> : <Play size={16} fill="currentColor" className="ml-0.5" />}
              {playing ? 'Pause the theme' : 'Play the theme'}
            </button>
            <a
              href="#latest-news"
              onClick={(e) => {
                e.preventDefault();
                scrollToHash('#latest-news');
              }}
              className="border-b border-gold pb-1 text-sm font-medium text-ink transition-colors hover:text-gold"
            >
              Read the story
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
