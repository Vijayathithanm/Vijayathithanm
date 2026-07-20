'use client';

import dynamic from 'next/dynamic';
import Providers from './Providers';
import Navbar from './Navbar';
import Hero from './sections/Hero';
import { TitleModalProvider } from './ui/TitleModal';

/* Below-the-fold sections are code-split so the initial bundle stays light. */
const Catalog = dynamic(() => import('./sections/Catalog'));
const Footer = dynamic(() => import('./Footer'));

export default function App() {
  return (
    <Providers>
      <TitleModalProvider>
        <Navbar />
        <main>
          <Hero />
          <Catalog />
        </main>
        <Footer />
      </TitleModalProvider>
    </Providers>
  );
}
