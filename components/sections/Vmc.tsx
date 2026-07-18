'use client';

import { useRef } from 'react';
import { motion, useScroll, useTransform } from 'framer-motion';
import { vmcPhases } from '@/content/resume';
import Reveal from '@/components/ui/Reveal';
import SectionHeading from '@/components/ui/SectionHeading';

/** Premium horizontal-feel showcase for the in-house VMC programme. */
export default function Vmc() {
  const trackRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: trackRef,
    offset: ['start end', 'end start'],
  });
  const lineScale = useTransform(scrollYProgress, [0.05, 0.85], [0, 1]);

  return (
    <section id="vmc" className="relative overflow-hidden py-24 md:py-36">
      <div className="eng-grid absolute inset-0 opacity-30" />
      <div className="glow-orb right-[-15%] top-[10%] h-[500px] w-[500px] bg-accent2/15" />

      <div className="relative mx-auto max-w-7xl px-5 md:px-8">
        <SectionHeading
          tag="05 · Flagship Programme"
          title="Building a Vertical Machining Center, in-house"
          intro="Leading the complete development of a VMC — from first concept sketch to a fatigue-validated machine structure. Every phase is simulation-driven."
        />

        {/* KPI strip */}
        <Reveal className="mb-16 grid grid-cols-2 gap-px overflow-hidden rounded-2xl border border-line bg-line/60 md:grid-cols-4">
          {[
            ['Abaqus', 'Structural & dynamic FEA'],
            ['fe-safe', 'Durability & fatigue life'],
            ['SolidWorks', 'Design & assembly'],
            ['Concept → Realization', 'End-to-end ownership'],
          ].map(([k, v]) => (
            <div key={k} className="bg-bg p-6 text-center">
              <div className="font-display text-lg font-semibold text-accent">{k}</div>
              <div className="mt-1 font-mono text-[11px] text-faint">{v}</div>
            </div>
          ))}
        </Reveal>

        {/* phase timeline */}
        <div ref={trackRef} className="relative">
          <div className="absolute left-0 top-5 hidden h-px w-full bg-line lg:block" />
          <motion.div
            style={{ scaleX: lineScale }}
            className="absolute left-0 top-5 hidden h-px w-full origin-left bg-accent lg:block"
          />

          <div className="grid gap-8 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-7 lg:gap-4">
            {vmcPhases.map((phase, i) => (
              <Reveal key={phase.phase} delay={i * 0.08}>
                <div className="group relative">
                  <div className="relative z-10 mb-5 flex h-10 w-10 items-center justify-center rounded-full border border-accent/40 bg-bg font-mono text-xs text-accent shadow-[0_0_16px_rgb(var(--accent)/0.2)] transition-all duration-300 group-hover:bg-accent group-hover:text-bg">
                    {phase.phase}
                  </div>
                  <h3 className="font-display text-base font-medium">{phase.title}</h3>
                  <p className="mt-2 text-[13px] leading-relaxed text-muted">{phase.desc}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>

        {/* analysis capabilities */}
        <Reveal delay={0.2} className="mt-16">
          <div className="blueprint-card rounded-2xl p-8 md:p-10">
            <div className="grid gap-8 md:grid-cols-2">
              <div>
                <div className="section-tag mb-4">Validation Scope</div>
                <ul className="space-y-3">
                  {[
                    'Structural design validation of frame and load path',
                    'Static stiffness analysis under cutting loads',
                    'Dynamic structural behaviour for vibration performance',
                    'Accidental impact load assessment (crash-case safety)',
                    'Durability & fatigue-life evaluation with fe-safe',
                  ].map((item) => (
                    <li key={item} className="flex gap-3 text-sm text-muted">
                      <span className="mt-[7px] h-1 w-1 shrink-0 rounded-full bg-accent" />
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
              <div className="flex flex-col justify-center border-t border-line/60 pt-8 md:border-l md:border-t-0 md:pl-10 md:pt-0">
                <p className="font-display text-2xl font-medium leading-snug">
                  “Machine stiffness, reliability and long-term performance — proven in
                  simulation before a single chip is cut.”
                </p>
                <div className="mt-4 font-mono text-xs text-faint">
                  — DESIGN PHILOSOPHY, VMC PROGRAMME
                </div>
              </div>
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
