'use client';

import { useEffect, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { profile } from '@/content/resume';

export default function Preloader({ onDone }: { onDone: () => void }) {
  const [progress, setProgress] = useState(0);
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    let value = 0;
    const interval = setInterval(() => {
      value += Math.random() * 22 + 8;
      if (value >= 100) {
        value = 100;
        clearInterval(interval);
        setTimeout(() => {
          setVisible(false);
          onDone();
        }, 350);
      }
      setProgress(Math.floor(value));
    }, 120);
    return () => clearInterval(interval);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          exit={{ opacity: 0, scale: 1.04 }}
          transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
          className="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-bg"
          aria-hidden
        >
          <div className="eng-grid-fine absolute inset-0 opacity-40" />
          <div className="relative flex flex-col items-center gap-6">
            <motion.div
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              className="font-display text-2xl font-semibold tracking-tight"
            >
              <span className="text-accent font-mono">[</span> {profile.initials}{' '}
              <span className="text-accent font-mono">]</span>
            </motion.div>
            <div className="h-px w-56 overflow-hidden bg-line">
              <motion.div
                className="h-full bg-accent"
                style={{ width: `${progress}%` }}
                transition={{ ease: 'linear' }}
              />
            </div>
            <div className="font-mono text-xs tracking-[0.35em] text-muted">
              INITIALIZING · {progress}%
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
