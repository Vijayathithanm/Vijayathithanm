'use client';

import { useMemo, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { scene as store, damp } from '@/lib/store';
import { audioEngine } from '@/lib/audio';

/**
 * SoundRibbon — the hero centrepiece.
 *
 * A single indexed plane geometry (NOT many meshes) whose vertices undulate
 * like a waveform via layered sine noise. When the track is playing the
 * amplitude is driven by real audio-frequency energy from the AnalyserNode;
 * otherwise it settles into calm procedural motion. Matte charcoal surface
 * with two thin continuous gold edge highlights, and it tilts gently toward
 * the cursor.
 *
 * Under `prefers-reduced-motion` the ribbon freezes into a static elegant
 * curve and stops reacting.
 */
export default function SoundRibbon({ segments = 96 }: { segments?: number }) {
  const group = useRef<THREE.Group>(null);
  const level = useRef(0);

  const LENGTH = 11;
  const WIDTH = 1.35;
  const segX = segments;
  const segZ = 6;
  const rowCount = segX + 1;

  // One indexed plane geometry, laid flat (XZ) so it waves in Y.
  const geometry = useMemo(() => {
    const g = new THREE.PlaneGeometry(LENGTH, WIDTH, segX, segZ);
    g.rotateX(-Math.PI / 2);
    return g;
  }, [segX]);

  // Base (rest) positions we displace from every frame.
  const base = useMemo(() => Float32Array.from(geometry.attributes.position.array), [geometry]);

  // Two continuous gold edge lines built imperatively (avoids JSX <line> quirks).
  const { topLine, botLine } = useMemo(() => {
    const make = (opacity: number) => {
      const geo = new THREE.BufferGeometry();
      geo.setAttribute('position', new THREE.BufferAttribute(new Float32Array(rowCount * 3), 3));
      const mat = new THREE.LineBasicMaterial({ color: '#C8A047', transparent: true, opacity });
      return new THREE.Line(geo, mat);
    };
    return { topLine: make(0.9), botLine: make(0.55) };
  }, [rowCount]);

  useFrame((state) => {
    if (!store.active) return; // paused when tab hidden
    const t = store.reducedMotion ? 0 : state.clock.elapsedTime;

    // Smoothly follow the analyser (0 when paused → procedural fallback).
    level.current = damp(level.current, audioEngine.level(), 6, 1 / 60);
    const amp = 0.2 + level.current * 0.6; // procedural base + audio drive

    const pos = geometry.attributes.position.array as Float32Array;
    for (let i = 0; i < pos.length; i += 3) {
      const x = base[i];
      const z = base[i + 2];
      const wave =
        Math.sin(x * 0.62 + t * 1.05) * 0.6 +
        Math.sin(x * 1.35 - t * 0.7 + z * 1.4) * 0.28 +
        Math.sin(x * 2.4 + t * 1.7) * 0.12 * (0.4 + level.current);
      pos[i + 1] = base[i + 1] + wave * amp;
    }
    geometry.attributes.position.needsUpdate = true;
    geometry.computeVertexNormals();

    // Copy the two border rows into the gold edge lines.
    const topArr = topLine.geometry.attributes.position.array as Float32Array;
    const botArr = botLine.geometry.attributes.position.array as Float32Array;
    const lastRowStart = pos.length - rowCount * 3;
    for (let c = 0; c < rowCount * 3; c++) {
      topArr[c] = pos[c];
      botArr[c] = pos[lastRowStart + c];
    }
    topLine.geometry.attributes.position.needsUpdate = true;
    botLine.geometry.attributes.position.needsUpdate = true;

    // Gentle tilt toward the cursor for a parallax feel.
    if (group.current) {
      const tiltX = store.reducedMotion ? 0 : store.pointerY * 0.12;
      const tiltZ = store.reducedMotion ? 0 : -store.pointerX * 0.14;
      group.current.rotation.x = damp(group.current.rotation.x, tiltX, 3, 1 / 60);
      group.current.rotation.z = damp(group.current.rotation.z, tiltZ, 3, 1 / 60);
    }
  });

  return (
    <group ref={group} position={[0, 0.55, 0]}>
      <mesh geometry={geometry} castShadow receiveShadow>
        {/* Matte charcoal ribbon surface */}
        <meshStandardMaterial color="#1A1A1A" roughness={0.85} metalness={0.05} side={THREE.DoubleSide} />
      </mesh>
      <primitive object={topLine} />
      <primitive object={botLine} />
    </group>
  );
}
