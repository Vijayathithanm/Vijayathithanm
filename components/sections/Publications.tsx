'use client';

import { useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { BookOpen, Mic, Presentation } from 'lucide-react';
import { publications } from '@/content/resume';
import Reveal from '@/components/ui/Reveal';
import SectionHeading from '@/components/ui/SectionHeading';

const tabs = [
  { key: 'journal', label: 'Journal Articles', icon: BookOpen },
  { key: 'conference', label: 'Conference Papers', icon: Presentation },
  { key: 'talk', label: 'Invited Talks', icon: Mic },
] as const;

export default function Publications() {
  const [tab, setTab] = useState<'journal' | 'conference' | 'talk'>('journal');
  const visible = publications.filter((p) => p.type === tab);

  return (
    <section
      id="publications"
      className="border-t border-line/50 bg-surface/40 py-24 md:py-36"
    >
      <div className="mx-auto max-w-5xl px-5 md:px-8">
        <SectionHeading
          tag="06 · Research Output"
          title="Publications & talks"
          intro="Peer-reviewed research in Wear, IJAMT and Proc. IMechE — presented at ASME IMECE, Wear of Materials, and MATADOR."
        />

        <Reveal className="mb-8 flex flex-wrap gap-2">
          {tabs.map((t) => (
            <button
              key={t.key}
              onClick={() => setTab(t.key)}
              className={`flex items-center gap-2 rounded-full border px-4 py-2 font-mono text-xs tracking-wider transition-all duration-300 ${
                tab === t.key
                  ? 'border-accent bg-accent/10 text-accent'
                  : 'border-line text-muted hover:border-accent/40 hover:text-ink'
              }`}
            >
              <t.icon size={13} />
              {t.label.toUpperCase()}
            </button>
          ))}
        </Reveal>

        <div className="space-y-4">
          <AnimatePresence mode="popLayout">
            {visible.map((p, i) => (
              <motion.article
                layout
                key={p.ref}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.4, delay: i * 0.06 }}
                className="blueprint-card group flex gap-5 rounded-2xl p-6 md:p-7"
              >
                <div className="hidden h-10 w-10 shrink-0 items-center justify-center rounded-lg border border-line bg-bg font-mono text-xs text-accent sm:flex">
                  {p.ref}
                </div>
                <div>
                  <h3 className="font-medium leading-snug text-ink transition-colors group-hover:text-accent">
                    {p.title}
                  </h3>
                  <p className="mt-2 text-sm text-muted">
                    {p.authors} · <span className="italic">{p.venue}</span>
                  </p>
                  <div className="mt-2 flex items-center gap-3 font-mono text-xs text-faint">
                    <span>{p.year}</span>
                    {p.note && (
                      <span className="rounded-full border border-line px-2.5 py-0.5 text-[10px] tracking-wider">
                        {p.note.toUpperCase()}
                      </span>
                    )}
                  </div>
                </div>
              </motion.article>
            ))}
          </AnimatePresence>
        </div>
      </div>
    </section>
  );
}
