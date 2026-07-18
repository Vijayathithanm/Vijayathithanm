'use client';

import { motion } from 'framer-motion';
import {
  Activity,
  CircleDot,
  Layers,
  Magnet,
  Orbit,
  Zap,
} from 'lucide-react';
import { simulations } from '@/content/resume';
import Reveal from '@/components/ui/Reveal';
import SectionHeading from '@/components/ui/SectionHeading';

const iconMap: Record<string, React.ElementType> = {
  magnet: Magnet,
  zap: Zap,
  orbit: Orbit,
  'circle-dot': CircleDot,
  activity: Activity,
  layers: Layers,
};

export default function Simulations() {
  return (
    <section
      id="simulations"
      className="relative overflow-hidden border-t border-line/50 bg-surface/40 py-24 md:py-36"
    >
      <div className="glow-orb left-1/2 top-0 h-[400px] w-[700px] -translate-x-1/2 bg-plasma/10" />

      <div className="relative mx-auto max-w-7xl px-5 md:px-8">
        <SectionHeading
          tag="04 · COMSOL Multiphysics"
          title="Simulation is the first prototype"
          intro="Multiphysics models built for the indigenous magnetron programme — from electromagnetic field topology to plasma behaviour and target erosion."
        />

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {simulations.map((sim, i) => {
            const Icon = iconMap[sim.icon] ?? Layers;
            return (
              <Reveal key={sim.title} delay={i * 0.08}>
                <motion.div
                  whileHover={{ y: -6 }}
                  transition={{ type: 'spring', stiffness: 260, damping: 20 }}
                  className="blueprint-card group relative h-full overflow-hidden rounded-2xl p-7"
                >
                  {/* scan-line effect on hover */}
                  <div className="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-500 group-hover:opacity-100">
                    <div className="animate-scan absolute inset-x-0 h-24 bg-gradient-to-b from-transparent via-accent/10 to-transparent" />
                  </div>

                  <div className="mb-5 inline-flex rounded-xl border border-line bg-bg p-3.5 text-accent transition-all duration-500 group-hover:rotate-[360deg] group-hover:border-accent/50">
                    <Icon size={22} strokeWidth={1.5} />
                  </div>
                  <h3 className="font-display text-lg font-medium">{sim.title}</h3>
                  <p className="mt-2.5 text-sm leading-relaxed text-muted">{sim.desc}</p>
                  <div className="mt-5 font-mono text-[10px] tracking-[0.25em] text-faint">
                    COMSOL MULTIPHYSICS®
                  </div>
                </motion.div>
              </Reveal>
            );
          })}
        </div>
      </div>
    </section>
  );
}
