'use client';

import { Info } from 'lucide-react';
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
    <div className="relative z-20 -mt-16 space-y-2 pb-10 md:-mt-24">
      <Row id="compositions" heading="Iconic Compositions" items={films} variant="poster" />
      <Row heading="Trending — Top of the Charts" items={[...films].reverse()} variant="poster" />
      <Row id="latest-posts" heading="Latest Posts" items={postTitles} variant="wide" />

      {/* Featured news billboard */}
      <section id="latest-news" className="reveal mx-auto max-w-content px-4 py-8 md:px-8">
        <button
          type="button"
          onClick={() => open(newsTitle)}
          className="group relative block w-full overflow-hidden rounded-xl border border-line text-left"
          aria-label={`${newsTitle.title} — more info`}
        >
          <div className="relative aspect-[16/8] w-full md:aspect-[21/7]">
            <Img src={newsTitle.poster} alt={newsTitle.title} className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105" fallback="/placeholder-news.svg" />
            <div className="absolute inset-0 scrim-left" />
            <div className="absolute inset-y-0 left-0 flex max-w-xl flex-col justify-center p-6 md:p-10">
              <span className="mb-3 w-fit rounded bg-red px-2 py-0.5 text-[11px] font-bold uppercase tracking-wide text-white">
                {latestNews.feature.kicker}
              </span>
              <h3 className="font-display text-3xl tracking-wide text-ink md:text-5xl">{newsTitle.title}</h3>
              <p className="mt-3 line-clamp-3 text-sm text-muted md:text-base">{latestNews.feature.body}</p>
              <span className="mt-5 flex w-fit items-center gap-2 rounded bg-red px-5 py-2 text-sm font-semibold text-white transition-colors group-hover:bg-red-dark">
                <Info size={16} /> More Info
              </span>
            </div>
          </div>
        </button>
      </section>

      <Row id="concerts" heading="Concerts & Live In" items={concerts} variant="wide" />
      <Row id="facets" heading="The Many Facets" items={facetTitles} variant="poster" />
    </div>
  );
}
