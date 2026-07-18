'use client';

import { motion } from 'framer-motion';

type Props = {
  tag: string;
  title: string;
  intro?: string;
  align?: 'left' | 'center';
};

const wordVariants = {
  hidden: { y: '110%' },
  visible: (i: number) => ({
    y: 0,
    transition: { duration: 0.7, delay: 0.06 * i, ease: [0.22, 1, 0.36, 1] },
  }),
};

/** Numbered section header with per-word split-text reveal. */
export default function SectionHeading({ tag, title, intro, align = 'left' }: Props) {
  const words = title.split(' ');
  return (
    <div className={`mb-14 md:mb-20 ${align === 'center' ? 'text-center' : ''}`}>
      <motion.p
        initial={{ opacity: 0, y: 12 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: '-60px' }}
        transition={{ duration: 0.5 }}
        className="section-tag mb-4"
      >
        <span className="mr-3 inline-block h-px w-8 translate-y-[-3px] bg-accent align-middle" />
        {tag}
      </motion.p>
      {/* Viewport detection lives on the h2 — the word spans are clipped by
          overflow-hidden and would never intersect on their own. */}
      <motion.h2
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: '-60px' }}
        className="font-display text-3xl font-semibold tracking-tight sm:text-4xl md:text-5xl"
      >
        {words.map((word, i) => (
          <span key={i} className="inline-block overflow-hidden pb-1 align-bottom">
            <motion.span custom={i} variants={wordVariants} className="inline-block">
              {word}
              {i < words.length - 1 ? ' ' : ''}
            </motion.span>
          </span>
        ))}
      </motion.h2>
      {intro && (
        <motion.p
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: '-60px' }}
          transition={{ duration: 0.6, delay: 0.25 }}
          className={`mt-5 max-w-2xl text-base leading-relaxed text-muted md:text-lg ${
            align === 'center' ? 'mx-auto' : ''
          }`}
        >
          {intro}
        </motion.p>
      )}
    </div>
  );
}
