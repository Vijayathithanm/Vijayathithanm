'use client';

import { latestPosts } from '@/content/site';
import { scrollToHash } from '@/lib/utils';
import TiltCard from '@/components/ui/TiltCard';

/**
 * Latest Posts — three floating tilt cards. (These same three also appear as
 * spinning vinyl records in the 3D gallery behind the page.)
 */
export default function LatestPosts() {
  return (
    <section id="latest-posts" className="relative py-24 md:py-32" aria-label="Latest posts">
      <div className="mx-auto max-w-content px-5 md:px-8">
        <header className="reveal mb-14 text-center">
          <p className="mb-3 text-xs uppercase tracking-widest2 text-gold">Fresh from the studio</p>
          <h2 className="font-display text-4xl font-extrabold text-ink md:text-5xl">
            {latestPosts.heading}
          </h2>
        </header>

        <div className="grid gap-7 md:grid-cols-3">
          {latestPosts.cards.map((card) => (
            <TiltCard key={card.title} className="reveal p-0">
              <a
                href={card.href}
                onClick={(e) => {
                  e.preventDefault();
                  scrollToHash(card.href);
                }}
                className="block overflow-hidden rounded-xl"
              >
                <div className="relative aspect-[4/3] overflow-hidden">
                  {/* SWAP: replace placeholder with a real post image (content/site.ts) */}
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={card.image}
                    alt={card.title}
                    loading="lazy"
                    className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                  />
                  <span className="absolute left-4 top-4 rounded-full bg-white/90 px-3 py-1 text-[10px] font-semibold uppercase tracking-widest text-gold">
                    Coming soon
                  </span>
                </div>
                <div className="p-6">
                  <h3 className="font-display text-xl font-bold text-ink">{card.title}</h3>
                  <p className="mt-2 text-sm leading-relaxed text-muted">{card.blurb}</p>
                </div>
              </a>
            </TiltCard>
          ))}
        </div>
      </div>
    </section>
  );
}
