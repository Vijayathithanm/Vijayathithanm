'use client';

import { Canvas } from '@react-three/fiber';
import { ContactShadows, AdaptiveDpr } from '@react-three/drei';
import * as THREE from 'three';
import Lights from './Lights';
import Rig from './Rig';
import SoundRibbon from './SoundRibbon';
import VinylGallery from './VinylGallery';
import { useIsMobile, useReducedMotion } from '@/lib/hooks';

/**
 * The persistent white 3D stage that sits behind all page content.
 * Performance guards: capped pixel ratio, fewer ribbon segments on mobile,
 * adaptive DPR, and per-object pausing when the tab is hidden.
 */
export default function SceneCanvas() {
  const mobile = useIsMobile();
  const reduced = useReducedMotion();

  return (
    <Canvas
      shadows
      dpr={[1, mobile ? 1.5 : 2]}
      gl={{ antialias: true, powerPreference: 'high-performance', toneMapping: THREE.NoToneMapping }}
      camera={{ position: [0, 0.5, 5.2], fov: 42 }}
      onCreated={({ gl, scene }) => {
        gl.setClearColor('#FFFFFF', 1);
        scene.background = new THREE.Color('#FFFFFF');
      }}
    >
      <Lights />
      <Rig />

      <SoundRibbon segments={mobile ? 56 : 100} />
      <VinylGallery />

      {/* Soft shared contact shadow on the white floor */}
      <ContactShadows
        position={[0, -0.95, -0.5]}
        scale={16}
        far={4.5}
        blur={2.6}
        opacity={0.32}
        color="#1A1A1A"
        resolution={mobile ? 256 : 512}
        frames={reduced ? 1 : Infinity}
      />

      <AdaptiveDpr pixelated />
    </Canvas>
  );
}
