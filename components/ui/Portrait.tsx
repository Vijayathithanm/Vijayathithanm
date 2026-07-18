'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { asset } from '@/lib/utils';
import { profile } from '@/content/resume';

/**
 * Framed portrait. Renders the monogram by default and only reveals the photo
 * once it has actually loaded, so before public/images/profile.jpg is added
 * the card looks intentional (no broken-image icon), and the photo fades in
 * the moment it exists.
 */
export default function Portrait() {
  const [loaded, setLoaded] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.94 }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once: true, margin: '-80px' }}
      transition={{ duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
      className="relative mx-auto w-full max-w-sm"
    >
      {/* accent glow */}
      <div className="glow-orb inset-0 -z-10 h-full w-full bg-accent/20" />

      <div className="blueprint-card relative overflow-hidden rounded-3xl p-2">
        <div className="relative aspect-[4/5] overflow-hidden rounded-2xl bg-surface">
          <div className="eng-grid-fine absolute inset-0 opacity-40" />

          {/* monogram placeholder (visible until the photo loads) */}
          <div className="absolute inset-0 flex flex-col items-center justify-center gap-3">
            <div className="font-display text-6xl font-semibold text-accent">
              {profile.initials}
            </div>
            <div className="font-mono text-[10px] tracking-[0.25em] text-faint">
              PORTRAIT
            </div>
          </div>

          {/* photo fades in over the monogram only on successful load */}
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={asset('/images/profile.jpg')}
            alt={`Portrait of ${profile.name}`}
            onLoad={() => setLoaded(true)}
            className="absolute inset-0 h-full w-full object-cover transition-opacity duration-700"
            style={{ opacity: loaded ? 1 : 0 }}
          />

          {/* bottom gradient for the caption chip legibility */}
          <div className="pointer-events-none absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-bg/70 to-transparent" />
        </div>
      </div>

      {/* corner label */}
      <div className="absolute -bottom-3 left-6 rounded-full border border-line bg-bg px-4 py-1.5 font-mono text-[10px] tracking-[0.2em] text-accent">
        PH.D · IIT MADRAS
      </div>
    </motion.div>
  );
}
