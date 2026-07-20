'use client';

import { useThree, useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { useRef } from 'react';
import { scene as store, damp } from '@/lib/store';

/**
 * Scroll-driven camera. As the page scrolls the camera pulls back and pans:
 * hero → close on the sound ribbon; later sections → wide, so the vinyl
 * gallery rotates into frame. Pointer adds a gentle parallax offset.
 *
 * (This is the "GSAP-ScrollTrigger-equivalent" the brief allows — scroll
 * progress drives the camera directly, keeping the DOM overlay fully native
 * and accessible instead of trapping content inside drei's <ScrollControls>.)
 */
type Key = { p: number; pos: [number, number, number]; look: [number, number, number] };

const KEYS: Key[] = [
  { p: 0.0, pos: [0, 0.28, 4.4], look: [0, 0.5, 0] }, // close & level on the ribbon
  { p: 0.3, pos: [0.6, 0.9, 6.8], look: [0, 0.12, -0.6] },
  { p: 0.62, pos: [0, 1.55, 8.8], look: [0, -0.5, -1.2] }, // gallery in frame
  { p: 1.0, pos: [0.25, 1.75, 9.6], look: [0, -0.6, -1.2] },
];

function sample(progress: number, key: 'pos' | 'look', out: THREE.Vector3) {
  let a = KEYS[0];
  let b = KEYS[KEYS.length - 1];
  for (let i = 0; i < KEYS.length - 1; i++) {
    if (progress >= KEYS[i].p && progress <= KEYS[i + 1].p) {
      a = KEYS[i];
      b = KEYS[i + 1];
      break;
    }
  }
  const span = b.p - a.p || 1;
  const t = THREE.MathUtils.clamp((progress - a.p) / span, 0, 1);
  const e = t * t * (3 - 2 * t); // smoothstep
  out.set(
    THREE.MathUtils.lerp(a[key][0], b[key][0], e),
    THREE.MathUtils.lerp(a[key][1], b[key][1], e),
    THREE.MathUtils.lerp(a[key][2], b[key][2], e),
  );
  return out;
}

export default function Rig() {
  const { camera } = useThree();
  const target = useRef(new THREE.Vector3());
  const desiredPos = useRef(new THREE.Vector3());
  const desiredLook = useRef(new THREE.Vector3());

  useFrame((_, dt) => {
    const d = Math.min(dt, 0.05);
    sample(store.progress, 'pos', desiredPos.current);
    sample(store.progress, 'look', desiredLook.current);

    // Pointer parallax (skipped under reduced motion).
    if (!store.reducedMotion) {
      desiredPos.current.x += store.pointerX * 0.45;
      desiredPos.current.y += -store.pointerY * 0.28;
    }

    camera.position.x = damp(camera.position.x, desiredPos.current.x, 3, d);
    camera.position.y = damp(camera.position.y, desiredPos.current.y, 3, d);
    camera.position.z = damp(camera.position.z, desiredPos.current.z, 3, d);

    target.current.x = damp(target.current.x, desiredLook.current.x, 4, d);
    target.current.y = damp(target.current.y, desiredLook.current.y, 4, d);
    target.current.z = damp(target.current.z, desiredLook.current.z, 4, d);
    camera.lookAt(target.current);
  });

  return null;
}
