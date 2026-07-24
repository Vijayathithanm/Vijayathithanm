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

/**
 * Real HD imagery from the internet (Unsplash — free to use). `img()` builds a
 * cropped, quality-tuned CDN URL. SWAP: replace with your own licensed
 * photographs of the maestro when you have them.
 */
const img = (id: string, w: number, h: number) =>
  `https://images.unsplash.com/photo-${id}?auto=format&fit=crop&w=${w}&h=${h}&q=80`;

/** Top navigation. `children` renders as an accessible dropdown menu. */
export type NavItem = { label: string; href: string; children?: { label: string; href: string }[] };

export const nav: NavItem[] = [
  { label: 'Home', href: '#home' },
  {
    label: 'Compositions',
    href: '#latest-posts',
    children: [
      { label: 'Movies', href: '#latest-posts' },
      { label: 'Albums', href: '#latest-posts' },
    ],
  },
  { label: 'Concerts', href: '#latest-posts' },
  { label: 'Maestroverse', href: '#latest-news' },
  { label: 'Live In', href: '#latest-posts' },
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
  // SWAP: replace with real banner artwork of the maestro.
  banners: [
    {
      src: img('1470225620780-dba8ba36b745', 1600, 1000),
      alt: 'A symphony orchestra performing on a concert stage',
      caption: 'Maestro at the podium',
    },
    {
      src: img('1507838153414-b4b713384a76', 1600, 1000),
      alt: 'A recording studio mixing console',
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
    poster: img('1465847899084-d164df4dedc6', 1280, 720),
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
      image: img('1487215078519-e21cc028cb29', 800, 600),
      href: '#latest-news',
    },
    {
      title: 'Maestroverse / Live In Concerts',
      blurb: 'The Maestro takes the stage — a world tour of live orchestral concerts.',
      image: img('1470225620780-dba8ba36b745', 800, 600),
      href: '#latest-news',
    },
    {
      title: 'Live From Studio',
      blurb: 'Behind the console — a rare look inside the maestro’s recording sessions.',
      image: img('1507838153414-b4b713384a76', 800, 600),
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
    image: img('1478720568477-152d9b164e26', 1200, 800),
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
      image: img('1455390582262-044cdead277a', 800, 600),
      href: '#footer',
    },
    {
      title: 'Photographer',
      blurb:
        'An eye as keen as his ear — Ilaiyaraaja frames the world in stills with the same instinct he brings to sound.',
      image: img('1452587925148-ce544e77e70d', 800, 600),
      href: '#footer',
    },
    {
      title: 'Member of Parliament',
      blurb:
        'Nominated to the Rajya Sabha, the maestro carries his voice for the arts into India’s highest house.',
      image: img('1529107386315-e1a2ed48a620', 800, 600),
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
