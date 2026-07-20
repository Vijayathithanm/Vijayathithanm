import type { Metadata } from 'next';
import { Space_Grotesk, Inter, JetBrains_Mono } from 'next/font/google';
import './globals.css';
import { profile, seo } from '@/content/resume';
import AppProviders from '@/components/providers/AppProviders';

const display = Space_Grotesk({
  subsets: ['latin'],
  variable: '--font-display',
  display: 'swap',
});
const sans = Inter({ subsets: ['latin'], variable: '--font-sans', display: 'swap' });
const mono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono',
  display: 'swap',
});

export const metadata: Metadata = {
  metadataBase: new URL(seo.siteUrl),
  title: seo.title,
  description: seo.description,
  keywords: seo.keywords,
  authors: [{ name: profile.name }],
  creator: profile.name,
  openGraph: {
    type: 'website',
    url: seo.siteUrl,
    title: seo.title,
    description: seo.description,
    siteName: profile.name,
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
  name: profile.name,
  jobTitle: profile.title,
  email: `mailto:${profile.email}`,
  telephone: profile.phone,
  url: seo.siteUrl,
  sameAs: [profile.linkedin],
  worksFor: { '@type': 'Organization', name: profile.company },
  alumniOf: [
    { '@type': 'CollegeOrUniversity', name: 'Indian Institute of Technology Madras' },
    { '@type': 'CollegeOrUniversity', name: 'Thiagarajar College of Engineering' },
    { '@type': 'CollegeOrUniversity', name: 'Anna University' },
  ],
  knowsAbout: seo.keywords,
  address: { '@type': 'PostalAddress', addressLocality: 'Bengaluru', addressCountry: 'IN' },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      className={`${display.variable} ${sans.variable} ${mono.variable}`}
      suppressHydrationWarning
    >
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
        <script
          dangerouslySetInnerHTML={{
            __html: `try{if(localStorage.theme==='light'){document.documentElement.classList.add('light')}}catch(e){}`,
          }}
        />
      </head>
      <body className="font-sans">
        <AppProviders>{children}</AppProviders>
      </body>
    </html>
  );
}
