'use client';

import dynamic from 'next/dynamic';

/**
 * Code-splits the entire Three.js scene out of the initial bundle and renders
 * it client-side only (no SSR). While it loads, the page shows the pure-white
 * background so there is never a flash of empty canvas.
 */
const SceneCanvas = dynamic(() => import('./three/SceneCanvas'), {
  ssr: false,
  loading: () => null,
});

export default function Scene() {
  return (
    <div className="scene-layer" aria-hidden="true">
      <SceneCanvas />
    </div>
  );
}
