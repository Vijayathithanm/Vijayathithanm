'use client';

import { motion } from 'framer-motion';
import {
  Activity,
  Award,
  BadgeCheck,
  BarChart3,
  Box,
  Code2,
  Ruler,
} from 'lucide-react';
import { certifications } from '@/content/resume';
import Reveal from '@/components/ui/Reveal';
import SectionHeading from '@/components/ui/SectionHeading';

const iconMap: Record<string, React.ElementType> = {
  award: Award,
  'badge-check': BadgeCheck,
  box: Box,
  'bar-chart': BarChart3,
  ruler: Ruler,
  activity: Activity,
  code: Code2,
};

export default function Certifications() {
  return (
    <section
      id="certifications"
      className="border-t border-line/50 bg-surface/40 py-24 md:py-36"
    >
      <div className="mx-auto max-w-7xl px-5 md:px-8">
        <SectionHeading
          tag="08 · Credentials"
          title="Certifications"
          intro="Continuous learning across metal cutting, simulation, quality systems and data."
        />

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {certifications.map((cert, i) => {
            const Icon = iconMap[cert.icon] ?? Award;
            return (
              <Reveal key={cert.title} delay={i * 0.06}>
                <motion.div
                  whileHover={{ y: -5, scale: 1.01 }}
                  transition={{ type: 'spring', stiffness: 300, damping: 20 }}
                  className="blueprint-card group flex h-full items-start gap-4 rounded-2xl p-6"
                >
                  <div className="rounded-xl border border-line bg-bg p-3 text-accent transition-colors group-hover:border-accent/50">
                    <Icon size={18} strokeWidth={1.6} />
                  </div>
                  <div>
                    <h3 className="text-sm font-medium leading-snug">{cert.title}</h3>
                    <p className="mt-1.5 font-mono text-[11px] text-faint">{cert.org}</p>
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
