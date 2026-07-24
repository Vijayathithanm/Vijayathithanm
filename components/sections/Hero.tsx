'use client';

import { useEffect, useState } from 'react';
import { ChevronLeft, ChevronRight, Play, Pause } from 'lucide-react';
import { hero } from '@/content/site';
import { audioEngine } from '@/lib/audio';
import { scrollToHash, asset } from '@/lib/utils';
import { useReducedMotion } from '@/lib/hooks';

/**
 * Hero — big title + subtitle, a crossfading banner carousel (prev/next), and
 * the play/pause control that makes the 3D sound ribbon react to audio.
 */
export default function Hero() {
  const [index, setIndex] = useState(0);
  const [playing, setPlaying] = useState(false);
  const reduced = useReducedMotion();
  const count = hero.banners.length;

  // Auto-advance the carousel (paused under reduced motion).
  useEffect(() => {
    if (reduced) return;
    const id = setInterval(() => setIndex((i) => (i + 1) % count), 6000);
    return () => clearInterval(id);
  }, [reduced, count]);

  const prev = () => setIndex((i) => (i - 1 + count) % count);
  const next = () => setIndex((i) => (i + 1) % count);

  const toggleAudio = async () => {
    if (playing) {
      audioEngine.pause();
      setPlaying(false);
    } else {
      await audioEngine.play();
      setPlaying(true);
    }
  };

  return (
    <section
      id="home"
      className="relative flex min-h-[100svh] items-center pt-28 pb-16"
      aria-label="Hero"
    >
      <div className="mx-auto grid w-full max-w-content gap-10 px-5 md:px-8 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
        {/* Left: title + controls */}
        <div className="reveal">
          <p className="mb-4 text-xs uppercase tracking-widest2 text-gold">
            Isaignani · The Maestro
          </p>
          <h1 className="font-display text-6xl font-black leading-[0.95] text-ink sm:text-7xl md:text-8xl">
            {hero.title}
          </h1>
          <p className="mt-6 max-w-xl text-base leading-relaxed text-muted md:text-lg">
            {hero.subtitle}
          </p>

          <div className="mt-9 flex flex-wrap items-center gap-4">
            <a
              href={hero.cta.href}
              onClick={(e) => {
                e.preventDefault();
                scrollToHash(hero.cta.href);
              }}
              className="interactive rounded-full bg-ink px-7 py-3 text-sm font-medium text-white transition-colors hover:bg-gold"
            >
              {hero.cta.label}
            </a>

            {/* Play/pause — drives the audio-reactive ribbon */}
            <button
              type="button"
              onClick={toggleAudio}
              aria-pressed={playing}
              className="interactive group flex items-center gap-3 rounded-full border border-line px-5 py-3 text-sm font-medium text-ink transition-colors hover:border-gold hover:text-gold"
            >
              <span className="flex h-7 w-7 items-center justify-center rounded-full bg-ink text-white transition-colors group-hover:bg-gold">
                {playing ? <Pause size={14} /> : <Play size={14} className="ml-0.5" />}
              </span>
              {playing ? 'Pause theme' : 'Play theme'}
            </button>
          </div>
          <p className="mt-3 text-xs text-faint">
            Play to let the ribbon dance to the music — pause for calm motion.
          </p>
        </div>

        {/* Right: crossfading banner carousel */}
        <div className="reveal">
          <div className="interactive relative aspect-[4/3] overflow-hidden rounded-2xl border border-line bg-white shadow-[0_30px_80px_-40px_rgba(0,0,0,0.35)]">
            {hero.banners.map((b, i) => (
              // SWAP: replace placeholder banners with real artwork (see content/site.ts)
              // eslint-disable-next-line @next/next/no-img-element
              <img
                key={b.src}
                src={asset(b.src)}
                alt={b.alt}
                loading={i === 0 ? 'eager' : 'lazy'}
                className={`absolute inset-0 h-full w-full object-cover transition-opacity duration-700 ${
                  i === index ? 'opacity-100' : 'opacity-0'
                }`}
              />
            ))}

            <div className="pointer-events-none absolute inset-x-0 bottom-0 flex items-center justify-between bg-gradient-to-t from-black/40 to-transparent p-4">
              <span className="text-xs font-medium text-white">
                {hero.banners[index].caption}
              </span>
              <span className="text-xs text-white/80">
                {index + 1} / {count}
              </span>
            </div>

            <button
              type="button"
              onClick={prev}
              aria-label="Previous banner"
              className="interactive absolute left-3 top-1/2 -translate-y-1/2 rounded-full bg-white/85 p-2 text-ink transition-colors hover:bg-gold hover:text-white"
            >
              <ChevronLeft size={18} />
            </button>
            <button
              type="button"
              onClick={next}
              aria-label="Next banner"
              className="interactive absolute right-3 top-1/2 -translate-y-1/2 rounded-full bg-white/85 p-2 text-ink transition-colors hover:bg-gold hover:text-white"
            >
              <ChevronRight size={18} />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
