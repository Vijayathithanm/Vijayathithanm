'use client';

import { useEffect, useRef } from 'react';

/** Soft radial glow that follows the pointer — GPU-accelerated, desktop only. */
export default function CursorGlow() {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    if (window.matchMedia('(pointer: coarse)').matches) return;

    let x = 0;
    let y = 0;
    let raf = 0;

    const onMove = (e: MouseEvent) => {
      x = e.clientX;
      y = e.clientY;
      if (!raf) {
        raf = requestAnimationFrame(() => {
          el.style.transform = `translate3d(${x - 300}px, ${y - 300}px, 0)`;
          raf = 0;
        });
      }
    };

    window.addEventListener('mousemove', onMove, { passive: true });
    return () => {
      window.removeEventListener('mousemove', onMove);
      cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <div
      ref={ref}
      aria-hidden
      className="pointer-events-none fixed left-0 top-0 z-[1] hidden h-[600px] w-[600px] rounded-full opacity-[0.07] md:block"
      style={{
        background:
          'radial-gradient(circle, rgb(var(--accent)) 0%, transparent 60%)',
        willChange: 'transform',
      }}
    />
  );
}
