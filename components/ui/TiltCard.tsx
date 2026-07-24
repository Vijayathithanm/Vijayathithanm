'use client';

import { useRef, type ReactNode } from 'react';
import { useReducedMotion } from '@/lib/hooks';
import { cn } from '@/lib/utils';

/**
 * A lightweight 3D-tilt card: the surface leans toward the cursor and lifts
 * slightly on hover. Pure transform/opacity (GPU-friendly). Tilt is disabled
 * under reduced motion. `pointer-events` are enabled via `.interactive`.
 */
export default function TiltCard({
  children,
  className,
  max = 8,
}: {
  children: ReactNode;
  className?: string;
  max?: number;
}) {
  const ref = useRef<HTMLDivElement>(null);
  const reduced = useReducedMotion();

  const onMove = (e: React.PointerEvent) => {
    if (reduced || !ref.current) return;
    const r = ref.current.getBoundingClientRect();
    const px = (e.clientX - r.left) / r.width - 0.5;
    const py = (e.clientY - r.top) / r.height - 0.5;
    ref.current.style.transform = `perspective(900px) rotateY(${px * max}deg) rotateX(${-py * max}deg) translateY(-6px)`;
  };
  const reset = () => {
    if (ref.current) ref.current.style.transform = '';
  };

  return (
    <div
      ref={ref}
      onPointerMove={onMove}
      onPointerLeave={reset}
      className={cn(
        'interactive group relative rounded-xl border border-line bg-white/70 backdrop-blur-sm',
        'transition-[transform,box-shadow,border-color] duration-300 will-change-transform',
        'hover:border-gold/60 hover:shadow-[0_20px_60px_-24px_rgba(200,160,71,0.55)]',
        className,
      )}
    >
      {children}
    </div>
  );
}
