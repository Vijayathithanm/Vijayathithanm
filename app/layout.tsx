import type { Metadata } from 'next';
import { Bebas_Neue, Inter } from 'next/font/google';
import './globals.css';
import { seo } from '@/content/site';

/* Tall cinematic display face for big titles, clean sans for body. */
const display = Bebas_Neue({
  subsets: ['latin'],
  weight: '400',
  variable: '--font-display',
  display: 'swap',
});
const sans = Inter({ subsets: ['latin'], variable: '--font-sans', display: 'swap' });

export const metadata: Metadata = {
  metadataBase: new URL(seo.siteUrl),
  title: seo.title,
  description: seo.description,
  keywords: seo.keywords,
  authors: [{ name: 'Ilaiyaraaja' }],
  openGraph: {
    type: 'website',
    url: seo.siteUrl,
    title: seo.title,
    description: seo.description,
    siteName: 'Ilaiyaraaja',
  },
  twitter: {
    card: 'summary_large_image',
    title: seo.title,
    description: seo.description,
  },
  robots: { index: true, follow: true },
};

const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Person',
  name: 'Ilaiyaraaja',
  alternateName: 'Isaignani',
  jobTitle: 'Composer, Songwriter and Conductor',
  url: seo.siteUrl,
  sameAs: ['https://www.youtube.com/@ilaiyaraaja'],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={`${display.variable} ${sans.variable}`}>
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
        {/* If JS is disabled, don't leave reveal-on-scroll content hidden. */}
        <noscript>
          <style>{`.reveal{opacity:1!important;transform:none!important}`}</style>
        </noscript>
      </head>
      <body>{children}</body>
    </html>
  );
}
