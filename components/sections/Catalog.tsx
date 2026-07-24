'use client';

import { Music2 } from 'lucide-react';
import { films, concerts, facets, latestPosts, latestNews, type Title } from '@/content/site';
import Row from '@/components/rows/Row';
import { useTitleModal } from '@/components/ui/TitleModal';
import Img from '@/components/ui/Img';

/* Map the existing facet / post content onto the shared Title shape. */
const facetTitles: Title[] = facets.cards.map((c, i) => ({
  id: `facet-${i}`,
  title: c.title,
  meta: 'Facet · Ilaiyaraaja',
  description: c.blurb,
  poster: c.image,
  backdrop: c.image,
}));

const postTitles: Title[] = latestPosts.cards.map((c, i) => ({
  id: `post-${i}`,
  title: c.title,
  meta: 'Latest Post · Coming Soon',
  description: c.blurb,
  poster: c.image,
  backdrop: c.image,
}));

const newsTitle: Title = {
  id: 'news-netflix',
  title: latestNews.feature.title,
  meta: `${latestNews.feature.kicker} · 2025`,
  description: latestNews.feature.body,
  poster: latestNews.feature.image,
  backdrop: latestNews.feature.image,
  badge: 'New',
};

export default function Catalog() {
  const { open } = useTitleModal();

  return (
    <div className="relative z-20 space-y-4 pb-12 pt-6">
      <Row id="compositions" heading="Selected Scores" items={films} variant="poster" />

      {/* Featured story — an editorial split, not a billboard */}
      <section id="latest-news" className="reveal mx-auto max-w-content px-6 py-14 md:px-8">
        <div className="grid items-center gap-8 md:grid-cols-2 md:gap-14">
          <button
            type="button"
            onClick={() => open(newsTitle)}
            className="group relative block overflow-hidden rounded-sm bg-panel text-left"
            aria-label={`${newsTitle.title} — details`}
          >
            <div className="relative aspect-[4/3] w-full">
              <Img src={newsTitle.poster} alt={newsTitle.title} className="h-full w-full object-cover grayscale transition-[filter,transform] duration-700 group-hover:scale-[1.03] group-hover:grayscale-0" fallback="/placeholder-news.svg" />
              <div className="pointer-events-none absolute inset-0 ring-1 ring-inset ring-transparent transition-colors group-hover:ring-gold/70" />
            </div>
          </button>
          <div>
            <p className="mb-4 flex items-center gap-2 text-xs font-semibold uppercase tracking-widest2 text-gold">
              <Music2 size={15} aria-hidden /> {latestNews.feature.kicker}
            </p>
            <h3 className="font-display text-4xl font-semibold leading-tight text-ink md:text-5xl">{newsTitle.title}</h3>
            <p className="mt-5 text-sm leading-relaxed text-muted md:text-base">{latestNews.feature.body}</p>
            <button
              type="button"
              onClick={() => open(newsTitle)}
              className="mt-7 border-b border-gold pb-1 text-sm font-medium text-ink transition-colors hover:text-gold"
            >
              Read the full story
            </button>
          </div>
        </div>
      </section>

      <Row id="concerts" heading="On Stage" items={concerts} variant="wide" />
      <Row id="latest-posts" heading="From the Studio" items={postTitles} variant="wide" />
      <Row id="facets" heading="The Many Facets" items={facetTitles} variant="poster" />
    </div>
  );
}
