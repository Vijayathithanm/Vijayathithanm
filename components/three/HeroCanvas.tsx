'use client';

import { Canvas } from '@react-three/fiber';
import { AdaptiveDpr } from '@react-three/drei';
import * as THREE from 'three';
import Lights from './Lights';
import SoundRibbon from './SoundRibbon';
import { useIsMobile } from '@/lib/hooks';

/**
 * The audio-reactive sound ribbon, scoped to the hero billboard (transparent
 * canvas so the dark cinematic gradient shows through). Capped DPR, fewer
 * segments on mobile, pauses when the tab is hidden (handled inside the ribbon).
 */
export default function HeroCanvas() {
  const mobile = useIsMobile();
  return (
    <Canvas
      dpr={[1, mobile ? 1.5 : 2]}
      gl={{ antialias: true, alpha: true, powerPreference: 'high-performance', toneMapping: THREE.NoToneMapping }}
      camera={{ position: [0, 0.3, 4.6], fov: 42 }}
    >
      <Lights />
      <SoundRibbon segments={mobile ? 56 : 100} />
      <AdaptiveDpr pixelated />
    </Canvas>
  );
}
