'use client';

import { useRef } from 'react';
import { motion, useMotionValue, useSpring } from 'framer-motion';
import { cn } from '@/lib/utils';

type Props = {
  children: React.ReactNode;
  href?: string;
  onClick?: () => void;
  variant?: 'primary' | 'ghost';
  className?: string;
  download?: boolean;
  external?: boolean;
};

/** Button that magnetically pulls toward the cursor. */
export default function MagneticButton({
  children,
  href,
  onClick,
  variant = 'primary',
  className,
  download,
  external,
}: Props) {
  const ref = useRef<HTMLDivElement>(null);
  const x = useMotionValue(0);
  const y = useMotionValue(0);
  const sx = useSpring(x, { stiffness: 180, damping: 16 });
  const sy = useSpring(y, { stiffness: 180, damping: 16 });

  const onMouseMove = (e: React.MouseEvent) => {
    const el = ref.current;
    if (!el) return;
    const rect = el.getBoundingClientRect();
    x.set((e.clientX - rect.left - rect.width / 2) * 0.3);
    y.set((e.clientY - rect.top - rect.height / 2) * 0.3);
  };

  const reset = () => {
    x.set(0);
    y.set(0);
  };

  const styles =
    variant === 'primary'
      ? 'bg-accent text-bg hover:shadow-[0_0_36px_rgb(var(--accent)/0.45)]'
      : 'border border-line text-ink hover:border-accent/60 hover:text-accent';

  const inner = (
    <span className="relative z-10 flex items-center gap-2 font-medium">{children}</span>
  );

  return (
    <motion.div
      ref={ref}
      onMouseMove={onMouseMove}
      onMouseLeave={reset}
      style={{ x: sx, y: sy }}
      className="inline-block"
    >
      {href ? (
        <a
          href={href}
          download={download}
          target={external ? '_blank' : undefined}
          rel={external ? 'noopener noreferrer' : undefined}
          className={cn(
            'inline-flex items-center rounded-full px-7 py-3.5 text-sm transition-all duration-300',
            styles,
            className,
          )}
        >
          {inner}
        </a>
      ) : (
        <button
          onClick={onClick}
          className={cn(
            'inline-flex items-center rounded-full px-7 py-3.5 text-sm transition-all duration-300',
            styles,
            className,
          )}
        >
          {inner}
        </button>
      )}
    </motion.div>
  );
}
