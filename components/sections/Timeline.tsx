'use client';

import { motion } from 'framer-motion';
import { Briefcase, FlaskConical, GraduationCap } from 'lucide-react';
import { education, experience } from '@/content/resume';
import Reveal from '@/components/ui/Reveal';
import SectionHeading from '@/components/ui/SectionHeading';

const icons = {
  industry: Briefcase,
  research: FlaskConical,
  education: GraduationCap,
};

const entries = [...experience, ...education];

export default function Timeline() {
  return (
    <section
      id="experience"
      className="relative border-t border-line/50 bg-surface/40 py-24 md:py-36"
    >
      <div className="mx-auto max-w-7xl px-5 md:px-8">
        <SectionHeading
          tag="02 · Journey"
          title="Professional & academic timeline"
          intro="Industry R&D, defence-grade research at IIT Madras, and a decade of engineering education — one continuous trajectory."
        />

        <div className="relative">
          {/* vertical spine */}
          <motion.div
            initial={{ scaleY: 0 }}
            whileInView={{ scaleY: 1 }}
            viewport={{ once: true, margin: '-100px' }}
            transition={{ duration: 1.4, ease: 'easeOut' }}
            className="absolute left-[19px] top-0 h-full w-px origin-top bg-gradient-to-b from-accent via-accent2 to-transparent md:left-1/2"
          />

          <div className="space-y-12 md:space-y-20">
            {entries.map((entry, i) => {
              const Icon = icons[entry.kind];
              const left = i % 2 === 0;
              return (
                <div
                  key={`${entry.org}-${entry.period}`}
                  className={`relative flex md:items-center ${
                    left ? 'md:flex-row' : 'md:flex-row-reverse'
                  }`}
                >
                  {/* node */}
                  <div className="absolute left-0 z-10 md:left-1/2 md:-translate-x-1/2">
                    <motion.div
                      initial={{ scale: 0 }}
                      whileInView={{ scale: 1 }}
                      viewport={{ once: true, margin: '-80px' }}
                      transition={{ type: 'spring', stiffness: 260, damping: 16, delay: 0.15 }}
                      className="flex h-10 w-10 items-center justify-center rounded-full border border-accent/50 bg-bg text-accent shadow-[0_0_20px_rgb(var(--accent)/0.25)]"
                    >
                      <Icon size={16} strokeWidth={1.7} />
                    </motion.div>
                  </div>

                  <div className={`ml-16 w-full md:ml-0 md:w-1/2 ${left ? 'md:pr-16' : 'md:pl-16'}`}>
                    <Reveal>
                      <div className="blueprint-card rounded-2xl p-6 md:p-8">
                        <div className="font-mono text-xs tracking-widest text-accent">
                          {entry.period}
                        </div>
                        <h3 className="mt-2 font-display text-xl font-medium">{entry.title}</h3>
                        <div className="mt-1 text-sm font-medium text-muted">{entry.org}</div>
                        <div className="font-mono text-xs text-faint">{entry.location}</div>
                        {entry.highlights.length > 0 && (
                          <ul className="mt-4 space-y-2.5">
                            {entry.highlights.map((h, j) => (
                              <li key={j} className="flex gap-3 text-sm leading-relaxed text-muted">
                                <span className="mt-[7px] h-1 w-1 shrink-0 rounded-full bg-accent" />
                                {h}
                              </li>
                            ))}
                          </ul>
                        )}
                      </div>
                    </Reveal>
                  </div>
                  <div className="hidden md:block md:w-1/2" />
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}
