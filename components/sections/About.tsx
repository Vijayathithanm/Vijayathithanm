'use client';

import { motion } from 'framer-motion';
import { Atom, Cog, Cpu, FlaskConical } from 'lucide-react';
import { applicationAreas, profile, stats } from '@/content/resume';
import CountUp from '@/components/ui/CountUp';
import Portrait from '@/components/ui/Portrait';
import Reveal from '@/components/ui/Reveal';
import SectionHeading from '@/components/ui/SectionHeading';

const pillars = [
  {
    icon: Atom,
    title: 'Multiphysics Simulation',
    desc: 'Electromagnetics, plasma, particle tracing and structural FEA in COMSOL & Abaqus.',
  },
  {
    icon: Cog,
    title: 'Machine Development',
    desc: 'In-house VMC from concept to realization — stiffness, dynamics, fatigue.',
  },
  {
    icon: FlaskConical,
    title: 'Surface Engineering',
    desc: 'HiPIMS PVD coatings, DLC thin films, tribology and characterisation.',
  },
  {
    icon: Cpu,
    title: 'AI for Manufacturing',
    desc: 'Acoustic-emission prognostics, ML wear prediction, digital-twin foundations.',
  },
];

export default function About() {
  return (
    <section id="about" className="relative mx-auto max-w-7xl px-5 py-24 md:px-8 md:py-36">
      {/* portrait + intro */}
      <div className="mb-16 grid items-center gap-12 md:mb-20 lg:grid-cols-[0.8fr_1.2fr] lg:gap-16">
        <Portrait />
        <div>
          <SectionHeading
            tag="01 · About"
            title="Engineering across physics, machines & intelligence"
            intro={profile.summary}
          />
        </div>
      </div>

      {/* animated statistics */}
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        {stats.map((s, i) => (
          <Reveal key={s.label} delay={i * 0.1}>
            <div className="blueprint-card group rounded-2xl p-6 md:p-8">
              <div className="font-display text-4xl font-semibold text-ink md:text-5xl">
                <CountUp value={s.value} suffix={s.suffix} />
              </div>
              <div className="mt-2 text-sm font-medium text-muted">{s.label}</div>
              <div className="mt-1 font-mono text-[11px] text-faint">{s.note}</div>
            </div>
          </Reveal>
        ))}
      </div>

      {/* pillars */}
      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {pillars.map((p, i) => (
          <Reveal key={p.title} delay={i * 0.1}>
            <motion.div
              whileHover={{ y: -6 }}
              transition={{ type: 'spring', stiffness: 260, damping: 20 }}
              className="blueprint-card h-full rounded-2xl p-6"
            >
              <div className="mb-4 inline-flex rounded-xl border border-line bg-surface p-3 text-accent">
                <p.icon size={20} strokeWidth={1.6} />
              </div>
              <h3 className="font-display text-lg font-medium">{p.title}</h3>
              <p className="mt-2 text-sm leading-relaxed text-muted">{p.desc}</p>
            </motion.div>
          </Reveal>
        ))}
      </div>

      {/* application areas ticker */}
      <Reveal delay={0.2} className="mt-14">
        <div className="relative overflow-hidden border-y border-line py-5 [mask-image:linear-gradient(90deg,transparent,black_10%,black_90%,transparent)]">
          <motion.div
            animate={{ x: ['0%', '-50%'] }}
            transition={{ duration: 28, repeat: Infinity, ease: 'linear' }}
            className="flex w-max gap-10 whitespace-nowrap"
          >
            {[...applicationAreas, ...applicationAreas].map((area, i) => (
              <span key={i} className="flex items-center gap-10 font-mono text-sm text-muted">
                {area}
                <span className="text-accent">◆</span>
              </span>
            ))}
          </motion.div>
        </div>
      </Reveal>
    </section>
  );
}
