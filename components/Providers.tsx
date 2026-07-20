'use client';

import { useEffect } from 'react';
import Lenis from 'lenis';
import { scene } from '@/lib/store';
import { useReducedMotion, useScrollReveal } from '@/lib/hooks';

/**
 * Providers — mounts once at the root. It:
 *   • runs Lenis smooth scroll (disabled under reduced-motion),
 *   • keeps the shared `scene` store in sync with scroll / pointer / tab
 *     visibility so the 3D canvas can read them every frame without React
 *     re-renders,
 *   • wires the reveal-on-scroll observer.
 */
export default function Providers({ children }: { children: React.ReactNode }) {
  const reduced = useReducedMotion();
  useScrollReveal();

  useEffect(() => {
    scene.reducedMotion = reduced;

    const updateProgress = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      scene.progress = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
    };
    updateProgress();

    // Pointer parallax — normalised to [-1, 1].
    const onPointer = (e: PointerEvent) => {
      scene.pointerX = (e.clientX / window.innerWidth) * 2 - 1;
      scene.pointerY = (e.clientY / window.innerHeight) * 2 - 1;
    };
    // Pause heavy work when the tab is hidden.
    const onVisibility = () => {
      scene.active = document.visibilityState === 'visible';
    };

    window.addEventListener('scroll', updateProgress, { passive: true });
    window.addEventListener('resize', updateProgress);
    window.addEventListener('pointermove', onPointer, { passive: true });
    document.addEventListener('visibilitychange', onVisibility);

    let lenis: Lenis | undefined;
    let raf = 0;
    if (!reduced) {
      lenis = new Lenis({ lerp: 0.09, wheelMultiplier: 0.9 });
      lenis.on('scroll', updateProgress);
      const loop = (time: number) => {
        lenis?.raf(time);
        raf = requestAnimationFrame(loop);
      };
      raf = requestAnimationFrame(loop);
    }

    return () => {
      window.removeEventListener('scroll', updateProgress);
      window.removeEventListener('resize', updateProgress);
      window.removeEventListener('pointermove', onPointer);
      document.removeEventListener('visibilitychange', onVisibility);
      cancelAnimationFrame(raf);
      lenis?.destroy();
    };
  }, [reduced]);

  return <>{children}</>;
}
