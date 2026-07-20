'use client';

import { useRef } from 'react';
import { motion, useMotionValue, useSpring, useTransform } from 'framer-motion';

type Props = { children: React.ReactNode; className?: string; intensity?: number };

/** 3D perspective tilt card that tracks the mouse. */
export default function TiltCard({ children, className, intensity = 8 }: Props) {
  const ref = useRef<HTMLDivElement>(null);
  const mx = useMotionValue(0.5);
  const my = useMotionValue(0.5);

  const rx = useSpring(useTransform(my, [0, 1], [intensity, -intensity]), {
    stiffness: 160,
    damping: 18,
  });
  const ry = useSpring(useTransform(mx, [0, 1], [-intensity, intensity]), {
    stiffness: 160,
    damping: 18,
  });

  const onMouseMove = (e: React.MouseEvent) => {
    const rect = ref.current?.getBoundingClientRect();
    if (!rect) return;
    mx.set((e.clientX - rect.left) / rect.width);
    my.set((e.clientY - rect.top) / rect.height);
  };

  const reset = () => {
    mx.set(0.5);
    my.set(0.5);
  };

  return (
    <motion.div
      ref={ref}
      onMouseMove={onMouseMove}
      onMouseLeave={reset}
      style={{ rotateX: rx, rotateY: ry, transformStyle: 'preserve-3d', perspective: 900 }}
      className={className}
    >
      {children}
    </motion.div>
  );
}
