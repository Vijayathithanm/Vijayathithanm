'use client';

import dynamic from 'next/dynamic';
import { motion, useScroll, useTransform } from 'framer-motion';
import { ArrowDown, Linkedin, Mail, MapPin } from 'lucide-react';
import { equations, profile } from '@/content/resume';
import MagneticButton from '@/components/ui/MagneticButton';
import Typewriter from '@/components/ui/Typewriter';

const HeroScene = dynamic(() => import('@/components/three/HeroScene'), { ssr: false });

export default function Hero() {
  const { scrollY } = useScroll();
  const yText = useTransform(scrollY, [0, 600], [0, 140]);
  const opacity = useTransform(scrollY, [0, 500], [1, 0]);

  return (
    <section id="top" className="relative flex min-h-screen items-center overflow-hidden">
      {/* layered background */}
      <div className="eng-grid absolute inset-0 opacity-60" />
      <div className="glow-orb left-[-10%] top-[-10%] h-[500px] w-[500px] bg-accent/20" />
      <div className="glow-orb bottom-[-20%] right-[-5%] h-[600px] w-[600px] bg-accent2/15" />
      <div className="absolute inset-0">
        <HeroScene />
      </div>

      {/* floating engineering equations */}
      <div aria-hidden className="pointer-events-none absolute inset-0 hidden lg:block">
        {equations.slice(0, 7).map((eq, i) => (
          <motion.span
            key={eq}
            initial={{ opacity: 0 }}
            animate={{ opacity: [0.08, 0.28, 0.08], y: [0, -18, 0] }}
            transition={{ duration: 7 + i * 1.3, repeat: Infinity, delay: i * 0.9 }}
            className="absolute font-mono text-sm text-accent"
            style={{
              left: `${8 + ((i * 37) % 85)}%`,
              top: `${12 + ((i * 29) % 72)}%`,
            }}
          >
            {eq}
          </motion.span>
        ))}
      </div>

      <motion.div
        style={{ y: yText, opacity }}
        className="relative z-10 mx-auto w-full max-w-7xl px-5 pt-28 md:px-8"
      >
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.35 }}
          className="mb-6 inline-flex items-center gap-2 rounded-full border border-line bg-surface/60 px-4 py-2 font-mono text-xs tracking-widest text-muted backdrop-blur"
        >
          <span className="relative flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-accent opacity-60" />
            <span className="relative inline-flex h-2 w-2 rounded-full bg-accent" />
          </span>
          PH.D. · IIT MADRAS — OPEN TO OPPORTUNITIES
        </motion.div>

        <h1 className="font-display text-4xl font-semibold leading-[1.05] tracking-tight sm:text-6xl md:text-7xl xl:text-8xl">
          <motion.span
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.5, ease: [0.22, 1, 0.36, 1] }}
            className="block"
          >
            Vijayathithan
          </motion.span>
          <motion.span
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.65, ease: [0.22, 1, 0.36, 1] }}
            className="text-gradient block"
          >
            Mathiyazhagan
          </motion.span>
        </h1>

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.85 }}
          className="mt-6 flex min-h-[2.2rem] items-center font-mono text-lg text-muted md:text-2xl"
        >
          <span className="mr-3 text-accent">›</span>
          <Typewriter words={profile.roles} />
        </motion.div>

        <motion.p
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 1 }}
          className="mt-6 max-w-2xl text-base leading-relaxed text-muted md:text-lg"
        >
          {profile.tagline}. Engineering machines, coatings and simulations at{' '}
          <span className="text-ink">{profile.company}</span> — from plasma physics to fatigue
          life.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 1.15 }}
          className="mt-10 flex flex-wrap items-center gap-4"
        >
          <MagneticButton href="#projects">Explore Work</MagneticButton>
          <MagneticButton href={profile.resumeFile} variant="ghost" download>
            Download Resume
          </MagneticButton>
          <div className="ml-1 flex items-center gap-3">
            <a
              href={profile.linkedin}
              target="_blank"
              rel="noopener noreferrer"
              aria-label="LinkedIn"
              className="rounded-full border border-line p-3 text-muted transition-all hover:border-accent/60 hover:text-accent"
            >
              <Linkedin size={16} />
            </a>
            <a
              href={`mailto:${profile.email}`}
              aria-label="Email"
              className="rounded-full border border-line p-3 text-muted transition-all hover:border-accent/60 hover:text-accent"
            >
              <Mail size={16} />
            </a>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.4 }}
          className="mt-8 flex items-center gap-2 font-mono text-xs text-faint"
        >
          <MapPin size={12} /> {profile.location} · {profile.availability}
        </motion.div>
      </motion.div>

      {/* scroll indicator */}
      <motion.a
        href="#about"
        aria-label="Scroll down"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.8 }}
        className="absolute bottom-8 left-1/2 z-10 -translate-x-1/2"
      >
        <motion.div
          animate={{ y: [0, 8, 0] }}
          transition={{ duration: 1.8, repeat: Infinity }}
          className="flex flex-col items-center gap-2 text-faint"
        >
          <span className="font-mono text-[10px] tracking-[0.3em]">SCROLL</span>
          <ArrowDown size={14} />
        </motion.div>
      </motion.a>
    </section>
  );
}
