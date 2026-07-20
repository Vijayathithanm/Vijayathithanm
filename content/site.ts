/**
 * content/site.ts — Single source of truth for every word & link on the site.
 * Edit this file to update copy; no component hardcodes content.
 *
 * NOTE: Replace all `/placeholder-*` image paths and the video path with real
 * assets dropped into `public/`. Search the codebase for "SWAP:" to find every
 * spot where a real asset should be plugged in.
 */

export const seo = {
  siteUrl: 'https://www.ilaiyaraajalive.com',
  title: 'Ilaiyaraaja — The Maestro | Official Interactive Experience',
  description:
    'An interactive 3D tribute to Ilaiyaraaja, the legendary Indian composer, songwriter and conductor. Explore his music, facets and latest news.',
  keywords: [
    'Ilaiyaraaja',
    'Maestro',
    'Indian film music',
    'composer',
    'Tamil cinema',
    'Isaignani',
  ],
};

/** Top navigation. `children` renders as an accessible dropdown menu. */
export type NavItem = { label: string; href: string; children?: { label: string; href: string }[] };

export const nav: NavItem[] = [
  { label: 'Home', href: '#home' },
  {
    label: 'Compositions',
    href: '#compositions',
    children: [
      { label: 'Movies', href: '#compositions' },
      { label: 'Albums', href: '#compositions' },
    ],
  },
  { label: 'Concerts', href: '#concerts' },
  { label: 'Maestroverse', href: '#latest-news' },
  { label: 'Live In', href: '#concerts' },
  { label: 'Awards', href: '#facets' },
  { label: 'E-Shopping', href: '#footer' },
  {
    label: 'Others',
    href: '#facets',
    children: [
      { label: 'Apply Certificate', href: '#footer' },
      { label: 'Exclusive Photographs', href: '#facets' },
      { label: 'Quiz', href: '#footer' },
    ],
  },
];

export const hero = {
  title: 'ILAIYARAAJA',
  subtitle:
    'Isaignani — the maestro whose melodies scored a generation. Composer, songwriter and conductor of more than a thousand films, still shaping the sound of Indian music.',
  cta: { label: 'Explore the music', href: '#biography' },
  // SWAP: replace with real banner artwork in /public/images/hero-1.jpg etc.
  banners: [
    {
      src: '/placeholder-hero-1.svg',
      alt: 'Ilaiyaraaja conducting a symphony orchestra',
      caption: 'Maestro at the podium',
    },
    {
      src: '/placeholder-hero-2.svg',
      alt: 'Ilaiyaraaja at the piano in the studio',
      caption: 'In the studio',
    },
  ],
};

export const biography = {
  heading: 'BIOGRAPHY',
  // SWAP: drop a real intro film at /public/video/intro.mp4 (and a .mov source
  // if you have one) and a poster at /public/images/bio-poster.jpg.
  video: {
    src: '/video/intro.mp4',
    poster: '/placeholder-bio-poster.svg',
  },
  intro:
    'Born in 1943 in Pannaipuram, Tamil Nadu, Ilaiyaraaja transformed Indian film music by fusing Western classical counterpoint, Carnatic tradition and Tamil folk into a wholly original voice. Across five decades and thousands of songs he has remained the standard against which film composers are measured.',
  cta: { label: 'Read detailed biography', href: '#latest-news' },
};

/** Latest Posts — also mirrored as vinyl records in the 3D gallery. */
export const latestPosts = {
  heading: 'LATEST POSTS',
  cards: [
    {
      title: 'Releasing Soon',
      blurb: 'A new score, mixed and mastered, is on its way to the screen.',
      // SWAP: /public/images/post-releasing.jpg
      image: '/placeholder-post-1.svg',
      href: '#latest-news',
    },
    {
      title: 'Maestroverse / Live In Concerts',
      blurb: 'The Maestro takes the stage — a world tour of live orchestral concerts.',
      image: '/placeholder-post-2.svg',
      href: '#latest-news',
    },
    {
      title: 'Live From Studio',
      blurb: 'Behind the console — a rare look inside the maestro’s recording sessions.',
      image: '/placeholder-post-3.svg',
      href: '#latest-news',
    },
  ],
};

export const latestNews = {
  heading: 'LATEST NEWS',
  feature: {
    kicker: 'Netflix Collaboration',
    title: 'Ilaiyaraaja scores the new season of Stranger Things',
    body: 'Netflix has collaborated with Ilaiyaraaja for the upcoming season of Stranger Things, with the maestro delivering iconic theme music for the series. Ahead of the Stranger Things season release, Netflix surprised Indian fans by announcing the collaboration. Stranger Things is set to release in Tamil and Telugu as well.',
    // SWAP: /public/images/news-netflix.jpg
    image: '/placeholder-news.svg',
    cta: { label: 'Read more news', href: '#facets' },
  },
};

/** Facets — also mirrored as vinyl records in the 3D gallery. */
export const facets = {
  heading: 'FACETS',
  intro:
    'Music legend Ilaiyaraaja stands out with phenomenal achievements and structural changes. His different facets are shown below.',
  cards: [
    {
      title: 'Lyricist',
      blurb:
        'Beyond composing, the maestro pens verse — lyrics steeped in philosophy, devotion and Tamil literary tradition.',
      image: '/placeholder-facet-1.svg',
      href: '#footer',
    },
    {
      title: 'Photographer',
      blurb:
        'An eye as keen as his ear — Ilaiyaraaja frames the world in stills with the same instinct he brings to sound.',
      image: '/placeholder-facet-2.svg',
      href: '#footer',
    },
    {
      title: 'Member of Parliament',
      blurb:
        'Nominated to the Rajya Sabha, the maestro carries his voice for the arts into India’s highest house.',
      image: '/placeholder-facet-3.svg',
      href: '#footer',
    },
  ],
};

export const footer = {
  address: {
    name: 'Ilaiyaraaja Studios',
    lines: ['137, Kodambakkam High Road', 'Chennai 600017', 'Tamil Nadu'],
    email: 'info@ilaiyaraajalive.com',
  },
  quickLinks: [
    { label: 'Biography', href: '#biography' },
    { label: 'Maestroverse', href: '#latest-news' },
    { label: 'Awards', href: '#facets' },
  ],
  legal: [
    { label: 'Disclaimer', href: '#' },
    { label: 'Terms and Conditions', href: '#' },
    { label: 'Privacy Policy', href: '#' },
  ],
  social: [
    // SWAP: point at the official channel.
    { label: 'YouTube', href: 'https://www.youtube.com/@ilaiyaraaja' },
  ],
  copyright: '© 2023 ilaiyaraajalive.com. All rights reserved.',
};

/* ───────────────────────────────────────────────────────────────
   CINEMATIC (Netflix-style) MODEL
   A shared "title" shape powers the billboard hero and every row.
   ─────────────────────────────────────────────────────────────── */

export type Title = {
  id: string;
  title: string;
  meta: string; // small line: year · genre · language
  description: string;
  poster: string; // portrait art (2:3) for row cards — SWAP for real art
  backdrop?: string; // wide art for the billboard — SWAP for real art
  badge?: string; // e.g. "New", "Top 10"
  rank?: number; // populates a Top-10 style numeral
};

/** The big billboard at the top of the page. */
export const featured = {
  kicker: 'Netflix Collaboration',
  title: 'ILAIYARAAJA',
  tagline: 'The maestro scores Stranger Things',
  description: latestNews.feature.body,
  meta: '2025 · Original Score · Tamil · Telugu · U/A',
  backdrop: '/placeholder-hero-1.svg', // SWAP: real cinematic backdrop
};

/**
 * Iconic compositions — a curated filmography the maestro scored.
 * (Real films; posters are placeholders — SWAP with real artwork.)
 */
export const films: Title[] = [
  { id: 'mullum-malarum', title: 'Mullum Malarum', meta: '1978 · Drama · Tamil', description: 'The score that announced a new voice in Indian film music.', poster: '/poster-mullum-malarum.svg' },
  { id: 'sagara-sangamam', title: 'Sagara Sangamam', meta: '1983 · Musical · Telugu', description: 'A dancer’s tragedy set to some of the maestro’s most beloved melodies.', poster: '/poster-sagara-sangamam.svg' },
  { id: 'sindhu-bhairavi', title: 'Sindhu Bhairavi', meta: '1985 · Musical · Tamil', description: 'Carnatic tradition meets cinema — a National Award-winning score.', poster: '/poster-sindhu-bhairavi.svg' },
  { id: 'mouna-ragam', title: 'Mouna Ragam', meta: '1986 · Romance · Tamil', description: 'Tender, aching themes for a modern love story.', poster: '/poster-mouna-ragam.svg' },
  { id: 'punnagai-mannan', title: 'Punnagai Mannan', meta: '1986 · Drama · Tamil', description: 'Sweeping romance and the unforgettable “Theme Music”.', poster: '/poster-punnagai-mannan.svg' },
  { id: 'nayakan', title: 'Nayakan', meta: '1987 · Crime · Tamil', description: 'An epic gangster saga carried by a haunting, iconic score.', poster: '/poster-nayakan.svg', badge: 'Top 10', rank: 1 },
  { id: 'geethanjali', title: 'Geethanjali', meta: '1989 · Romance · Telugu', description: 'Youthful, luminous melodies for a bittersweet romance.', poster: '/poster-geethanjali.svg' },
  { id: 'thalapathi', title: 'Thalapathi', meta: '1991 · Drama · Tamil', description: 'Friendship and fate, scored with grandeur and restraint.', poster: '/poster-thalapathi.svg', badge: 'Top 10', rank: 2 },
  { id: 'mahanadhi', title: 'Mahanadhi', meta: '1994 · Drama · Tamil', description: 'A father’s ruin, underscored with quiet devastation.', poster: '/poster-mahanadhi.svg' },
  { id: 'hey-ram', title: 'Hey Ram', meta: '2000 · Historical · Tamil', description: 'A sweeping historical canvas and a period-perfect score.', poster: '/poster-hey-ram.svg' },
];

/** Concerts & Live In — wide cards. */
export const concerts: Title[] = [
  { id: 'maestroverse-london', title: 'Maestroverse · London', meta: 'Live In · Symphony', description: 'The maestro conducts a full orchestra through decades of hits.', poster: '/placeholder-hero-2.svg' },
  { id: 'live-chennai', title: 'Live In Chennai', meta: 'Live In · Home Ground', description: 'A hometown crowd, a night of unforgettable melodies.', poster: '/placeholder-hero-1.svg' },
  { id: 'symphony-singapore', title: 'Symphony · Singapore', meta: 'Live In · World Tour', description: 'Ilaiyaraaja’s music reimagined for the concert hall.', poster: '/placeholder-news.svg' },
];

