'use client';

import { facets } from '@/content/site';
import { scrollToHash } from '@/lib/utils';
import TiltCard from '@/components/ui/TiltCard';

/**
 * Facets — three interactive cards that lift and glow gold on hover/focus.
 * Content is always visible (fully accessible, reduced-motion safe). These
 * same three facets also appear as flip-to-reveal vinyl records in the 3D
 * gallery behind the page.
 */
export default function Facets() {
  return (
    <section id="facets" className="relative py-24 md:py-32" aria-label="Facets">
      <div className="mx-auto max-w-content px-5 md:px-8">
        <header className="reveal mb-12 text-center">
          <p className="mb-3 text-xs uppercase tracking-widest2 text-gold">Many voices, one maestro</p>
          <h2 className="font-display text-4xl font-extrabold text-ink md:text-5xl">
            {facets.heading}
          </h2>
          <p className="mx-auto mt-5 max-w-2xl text-base leading-relaxed text-muted">
            {facets.intro}
          </p>
        </header>

        <div className="grid gap-7 md:grid-cols-3">
          {facets.cards.map((card) => (
            <TiltCard key={card.title} className="reveal p-0" max={6}>
              <a
                href={card.href}
                onClick={(e) => {
                  e.preventDefault();
                  scrollToHash(card.href);
                }}
                className="block overflow-hidden rounded-xl"
              >
                <div className="relative aspect-[4/3] overflow-hidden">
                  {/* SWAP: replace placeholder with a real facet image (content/site.ts) */}
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img
                    src={card.image}
                    alt={card.title}
                    loading="lazy"
                    className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                  />
                  {/* Gold sweep on hover */}
                  <span className="pointer-events-none absolute inset-0 bg-gradient-to-t from-gold/25 to-transparent opacity-0 transition-opacity duration-500 group-hover:opacity-100" />
                </div>
                <div className="p-6">
                  <h3 className="font-display text-xl font-bold text-ink transition-colors group-hover:text-gold">
                    {card.title}
                  </h3>
                  <p className="mt-2 text-sm leading-relaxed text-muted">{card.blurb}</p>
                  <span className="mt-4 inline-block text-xs uppercase tracking-widest text-gold opacity-0 transition-opacity duration-300 group-hover:opacity-100">
                    Learn more →
                  </span>
                </div>
              </a>
            </TiltCard>
          ))}
        </div>
      </div>
    </section>
  );
}
