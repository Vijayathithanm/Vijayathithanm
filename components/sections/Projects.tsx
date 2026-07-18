'use client';

import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { ChevronDown } from 'lucide-react';
import { projects } from '@/content/resume';
import ProjectVisual from '@/components/ui/ProjectVisual';
import Reveal from '@/components/ui/Reveal';
import SectionHeading from '@/components/ui/SectionHeading';
import TiltCard from '@/components/ui/TiltCard';

const categories = ['All', 'Simulation', 'Machine Design', 'Coatings', 'Research', 'Robotics'];

export default function Projects() {
  const [filter, setFilter] = useState('All');
  const [expanded, setExpanded] = useState<string | null>(null);

  const visible = projects.filter((p) => filter === 'All' || p.category === filter);

  return (
    <section id="projects" className="mx-auto max-w-7xl px-5 py-24 md:px-8 md:py-36">
      <SectionHeading
        tag="03 · Projects"
        title="Engineering problems, solved end to end"
        intro="Every project follows the same arc: a hard physical problem, a simulation-driven approach, and a validated outcome."
      />

      {/* filter */}
      <Reveal className="mb-10 flex flex-wrap gap-2">
        {categories.map((c) => (
          <button
            key={c}
            onClick={() => setFilter(c)}
            className={`rounded-full border px-4 py-2 font-mono text-xs tracking-wider transition-all duration-300 ${
              filter === c
                ? 'border-accent bg-accent/10 text-accent'
                : 'border-line text-muted hover:border-accent/40 hover:text-ink'
            }`}
          >
            {c.toUpperCase()}
          </button>
        ))}
      </Reveal>

      <motion.div layout className="grid gap-6 md:grid-cols-2">
        <AnimatePresence mode="popLayout">
          {visible.map((p, i) => {
            const isOpen = expanded === p.id;
            return (
              <motion.div
                layout
                key={p.id}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.96 }}
                transition={{ duration: 0.5, delay: i * 0.06 }}
                className={p.featured ? 'md:col-span-1' : ''}
              >
                <TiltCard intensity={4} className="h-full">
                  <div className="blueprint-card group flex h-full flex-col overflow-hidden rounded-2xl">
                    {/* schematic visual */}
                    <div className="relative h-52 overflow-hidden border-b border-line/60 bg-surface/40">
                      <div className="absolute inset-0 transition-transform duration-700 group-hover:scale-[1.04]">
                        <ProjectVisual kind={p.visual} />
                      </div>
                      <div
                        className={`absolute right-4 top-4 rounded-full bg-gradient-to-r ${p.accent} px-3 py-1 font-mono text-[10px] font-medium tracking-wider text-white`}
                      >
                        {p.category.toUpperCase()}
                      </div>
                    </div>

                    <div className="flex flex-1 flex-col p-6 md:p-7">
                      <h3 className="font-display text-xl font-medium md:text-2xl">{p.title}</h3>
                      <p className="mt-1 font-mono text-xs text-accent">{p.subtitle}</p>
                      <p className="mt-4 text-sm leading-relaxed text-muted">{p.problem}</p>

                      <AnimatePresence initial={false}>
                        {isOpen && (
                          <motion.div
                            initial={{ height: 0, opacity: 0 }}
                            animate={{ height: 'auto', opacity: 1 }}
                            exit={{ height: 0, opacity: 0 }}
                            transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                            className="overflow-hidden"
                          >
                            <div className="mt-5 border-t border-line/60 pt-5">
                              <div className="section-tag mb-3 !text-[10px]">Approach</div>
                              <ul className="space-y-2">
                                {p.approach.map((a, j) => (
                                  <li key={j} className="flex gap-3 text-sm text-muted">
                                    <span className="font-mono text-xs text-accent">
                                      {String(j + 1).padStart(2, '0')}
                                    </span>
                                    {a}
                                  </li>
                                ))}
                              </ul>
                              <div className="section-tag mb-2 mt-5 !text-[10px]">Outcome</div>
                              <p className="text-sm leading-relaxed text-ink">{p.outcome}</p>
                            </div>
                          </motion.div>
                        )}
                      </AnimatePresence>

                      <div className="mt-5 flex flex-wrap gap-2">
                        {p.stack.map((s) => (
                          <span
                            key={s}
                            className="rounded-md border border-line bg-surface px-2.5 py-1 font-mono text-[11px] text-muted"
                          >
                            {s}
                          </span>
                        ))}
                      </div>

                      <button
                        onClick={() => setExpanded(isOpen ? null : p.id)}
                        className="mt-6 flex items-center gap-2 self-start font-mono text-xs tracking-wider text-accent transition-opacity hover:opacity-70"
                        aria-expanded={isOpen}
                      >
                        {isOpen ? 'COLLAPSE' : 'ENGINEERING DETAILS'}
                        <motion.span animate={{ rotate: isOpen ? 180 : 0 }}>
                          <ChevronDown size={14} />
                        </motion.span>
                      </button>
                    </div>
                  </div>
                </TiltCard>
              </motion.div>
            );
          })}
        </AnimatePresence>
      </motion.div>
    </section>
  );
}
