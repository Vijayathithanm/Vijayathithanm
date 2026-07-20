'use client';

import { latestNews } from '@/content/site';
import { scrollToHash } from '@/lib/utils';

/** Latest News — the Netflix / Stranger Things feature card. */
export default function LatestNews() {
  const f = latestNews.feature;
  return (
    <section id="latest-news" className="relative py-24 md:py-32" aria-label="Latest news">
      <div className="mx-auto max-w-content px-5 md:px-8">
        <header className="reveal mb-14 text-center">
          <p className="mb-3 text-xs uppercase tracking-widest2 text-gold">Headlines</p>
          <h2 className="font-display text-4xl font-extrabold text-ink md:text-5xl">
            {latestNews.heading}
          </h2>
        </header>

        <article className="reveal interactive grid overflow-hidden rounded-2xl border border-line bg-white shadow-[0_30px_80px_-45px_rgba(0,0,0,0.35)] md:grid-cols-2">
          <div className="relative min-h-64 overflow-hidden">
            {/* SWAP: replace placeholder with the real news image (content/site.ts) */}
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={f.image}
              alt={f.title}
              loading="lazy"
              className="h-full w-full object-cover"
            />
          </div>
          <div className="flex flex-col justify-center p-8 md:p-10">
            <p className="mb-3 text-xs uppercase tracking-widest2 text-gold">{f.kicker}</p>
            <h3 className="font-display text-2xl font-bold text-ink md:text-3xl">{f.title}</h3>
            <p className="mt-4 text-sm leading-relaxed text-muted md:text-base">{f.body}</p>
            <a
              href={f.cta.href}
              onClick={(e) => {
                e.preventDefault();
                scrollToHash(f.cta.href);
              }}
              className="mt-7 inline-flex w-fit items-center gap-2 rounded-full bg-ink px-6 py-3 text-sm font-medium text-white transition-colors hover:bg-gold"
            >
              {f.cta.label} →
            </a>
          </div>
        </article>
      </div>
    </section>
  );
}
