'use client';

import { motion } from 'framer-motion';
import {
  Activity,
  BarChart3,
  Box,
  Code2,
  Layers,
  Microscope,
  PenTool,
} from 'lucide-react';
import { skillGroups } from '@/content/resume';
import RadarChart from '@/components/ui/RadarChart';
import Reveal from '@/components/ui/Reveal';
import SectionHeading from '@/components/ui/SectionHeading';

const iconMap: Record<string, React.ElementType> = {
  box: Box,
  'pen-tool': PenTool,
  layers: Layers,
  code: Code2,
  'bar-chart': BarChart3,
  microscope: Microscope,
  activity: Activity,
};

export default function Skills() {
  return (
    <section id="skills" className="mx-auto max-w-7xl px-5 py-24 md:px-8 md:py-36">
      <SectionHeading
        tag="07 · Capabilities"
        title="A full-stack engineering toolkit"
        intro="From multiphysics solvers to machine-learning pipelines — proficiency built through doctoral research and industrial R&D."
      />

      <div className="grid items-start gap-12 lg:grid-cols-[1fr_1.4fr]">
        {/* radar */}
        <Reveal className="lg:sticky lg:top-28">
          <div className="blueprint-card rounded-2xl p-6 md:p-8">
            <div className="section-tag mb-2">Competency Radar</div>
            <RadarChart />
          </div>
        </Reveal>

        {/* skill groups */}
        <div className="grid gap-4 sm:grid-cols-2">
          {skillGroups.map((group, gi) => {
            const Icon = iconMap[group.icon] ?? Box;
            return (
              <Reveal key={group.group} delay={gi * 0.06}>
                <div className="blueprint-card h-full rounded-2xl p-6">
                  <div className="mb-5 flex items-center gap-3">
                    <div className="rounded-lg border border-line bg-surface p-2.5 text-accent">
                      <Icon size={17} strokeWidth={1.6} />
                    </div>
                    <h3 className="font-display text-base font-medium">{group.group}</h3>
                  </div>
                  <div className="space-y-4">
                    {group.skills.map((skill, si) => (
                      <div key={skill.name}>
                        <div className="mb-1.5 flex items-center justify-between">
                          <span className="text-[13px] text-muted">{skill.name}</span>
                          <span className="font-mono text-[11px] text-faint">{skill.level}%</span>
                        </div>
                        <div className="h-[3px] overflow-hidden rounded-full bg-line/70">
                          <motion.div
                            initial={{ width: 0 }}
                            whileInView={{ width: `${skill.level}%` }}
                            viewport={{ once: true, margin: '-40px' }}
                            transition={{
                              duration: 1.1,
                              delay: 0.15 + si * 0.08,
                              ease: [0.22, 1, 0.36, 1],
                            }}
                            className="h-full rounded-full bg-gradient-to-r from-accent to-accent2"
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </Reveal>
            );
          })}
        </div>
      </div>
    </section>
  );
}
