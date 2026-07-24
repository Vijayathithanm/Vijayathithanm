'use client';

import dynamic from 'next/dynamic';
import Providers from './Providers';
import Scene from './Scene';
import Navbar from './Navbar';
import Hero from './sections/Hero';

/**
 * Below-the-fold sections are code-split so the initial bundle stays light —
 * only the Navbar, Hero and the (already lazily-imported) 3D scene load up
 * front. Markup is still server-rendered for SEO (ssr default = true).
 */
const Biography = dynamic(() => import('./sections/Biography'));
const LatestPosts = dynamic(() => import('./sections/LatestPosts'));
const LatestNews = dynamic(() => import('./sections/LatestNews'));
const Facets = dynamic(() => import('./sections/Facets'));
const Footer = dynamic(() => import('./Footer'));

export default function App() {
  return (
    <Providers>
      {/* Persistent white 3D stage behind everything */}
      <Scene />

      {/* 2D UI overlay — transparent so the canvas shows through as one surface */}
      <div className="content-layer">
        <Navbar />
        <main>
          <Hero />
          <Biography />
          <LatestPosts />
          <LatestNews />
          <Facets />
        </main>
        <Footer />
      </div>
    </Providers>
  );
}
