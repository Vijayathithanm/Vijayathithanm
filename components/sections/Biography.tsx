'use client';

import { biography } from '@/content/site';
import { scrollToHash } from '@/lib/utils';

/** Biography — intro film placeholder + short copy + CTA. */
export default function Biography() {
  return (
    <section id="biography" className="relative py-24 md:py-32" aria-label="Biography">
      <div className="mx-auto grid max-w-content gap-12 px-5 md:px-8 lg:grid-cols-2 lg:items-center">
        {/* Intro video (placeholder) */}
        <div className="reveal interactive overflow-hidden rounded-2xl border border-line bg-white shadow-[0_30px_80px_-45px_rgba(0,0,0,0.4)]">
          {/* SWAP: drop a real intro film at /public/video/intro.mp4 (see content/site.ts).
              The poster shows until the visitor presses play. */}
          <video
            className="aspect-video w-full bg-black/5"
            controls
            preload="none"
            poster={biography.video.poster}
          >
            <source src={biography.video.src} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>

        {/* Copy */}
        <div className="reveal">
          <p className="mb-3 text-xs uppercase tracking-widest2 text-gold">The Maestro</p>
          <h2 className="font-display text-4xl font-extrabold text-ink md:text-5xl">
            {biography.heading}
          </h2>
          <p className="mt-6 max-w-xl text-base leading-relaxed text-muted md:text-lg">
            {biography.intro}
          </p>
          <a
            href={biography.cta.href}
            onClick={(e) => {
              e.preventDefault();
              scrollToHash(biography.cta.href);
            }}
            className="interactive mt-8 inline-flex items-center gap-2 border-b-2 border-gold pb-1 text-sm font-medium text-ink transition-colors hover:text-gold"
          >
            {biography.cta.label} →
          </a>
        </div>
      </div>
    </section>
  );
}
