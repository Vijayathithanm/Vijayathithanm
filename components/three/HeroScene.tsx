'use client';

import { useMemo, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import * as THREE from 'three';

/** Procedural involute-style gear built from a 2D shape. */
function makeGearGeometry(teeth = 18, outerR = 1.9, innerR = 1.55, holeR = 0.55, depth = 0.35) {
  const shape = new THREE.Shape();
  const step = (Math.PI * 2) / teeth;
  for (let i = 0; i < teeth; i++) {
    const a0 = i * step;
    const a1 = a0 + step * 0.28;
    const a2 = a0 + step * 0.5;
    const a3 = a0 + step * 0.78;
    const a4 = a0 + step;
    if (i === 0) shape.moveTo(Math.cos(a0) * innerR, Math.sin(a0) * innerR);
    shape.lineTo(Math.cos(a1) * outerR, Math.sin(a1) * outerR);
    shape.lineTo(Math.cos(a2) * outerR, Math.sin(a2) * outerR);
    shape.lineTo(Math.cos(a3) * innerR, Math.sin(a3) * innerR);
    shape.lineTo(Math.cos(a4) * innerR, Math.sin(a4) * innerR);
  }
  const hole = new THREE.Path();
  hole.absarc(0, 0, holeR, 0, Math.PI * 2, true);
  shape.holes.push(hole);

  return new THREE.ExtrudeGeometry(shape, {
    depth,
    bevelEnabled: false,
    curveSegments: 8,
  });
}

function Gear({
  position,
  scale,
  speed,
  color,
  teeth,
}: {
  position: [number, number, number];
  scale: number;
  speed: number;
  color: string;
  teeth: number;
}) {
  const ref = useRef<THREE.Group>(null);
  const geometry = useMemo(() => makeGearGeometry(teeth), [teeth]);

  useFrame((state) => {
    if (!ref.current) return;
    ref.current.rotation.z += speed * 0.004;
    const { x, y } = state.pointer;
    ref.current.rotation.x = THREE.MathUtils.lerp(ref.current.rotation.x, y * 0.25, 0.04);
    ref.current.rotation.y = THREE.MathUtils.lerp(ref.current.rotation.y, x * 0.35, 0.04);
  });

  return (
    <group ref={ref} position={position} scale={scale}>
      <mesh geometry={geometry}>
        <meshBasicMaterial color={color} wireframe transparent opacity={0.35} />
      </mesh>
    </group>
  );
}

function Particles({ count = 350 }: { count?: number }) {
  const ref = useRef<THREE.Points>(null);
  const positions = useMemo(() => {
    const arr = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      arr[i * 3] = (Math.random() - 0.5) * 14;
      arr[i * 3 + 1] = (Math.random() - 0.5) * 9;
      arr[i * 3 + 2] = (Math.random() - 0.5) * 6;
    }
    return arr;
  }, [count]);

  useFrame((state) => {
    if (!ref.current) return;
    ref.current.rotation.y = state.clock.elapsedTime * 0.015;
    ref.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.08) * 0.05;
  });

  return (
    <points ref={ref}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[positions, 3]} />
      </bufferGeometry>
      <pointsMaterial size={0.02} color="#22d3ee" transparent opacity={0.55} sizeAttenuation />
    </points>
  );
}

function TorusField() {
  const ref = useRef<THREE.Mesh>(null);
  useFrame((state) => {
    if (!ref.current) return;
    ref.current.rotation.x = state.clock.elapsedTime * 0.1;
    ref.current.rotation.y = state.clock.elapsedTime * 0.14;
  });
  return (
    <mesh ref={ref} position={[3.4, -0.4, -1.5]}>
      <torusGeometry args={[1.5, 0.45, 10, 40]} />
      <meshBasicMaterial color="#60a5fa" wireframe transparent opacity={0.1} />
    </mesh>
  );
}

/** Full-screen background scene: rotating CAD-wireframe gears + particle field. */
export default function HeroScene() {
  return (
    <Canvas
      dpr={[1, 1.75]}
      camera={{ position: [0, 0, 6], fov: 50 }}
      gl={{ antialias: true, alpha: true, powerPreference: 'high-performance' }}
      style={{ position: 'absolute', inset: 0 }}
      aria-hidden
    >
      <Gear position={[2.9, 0.6, -0.5]} scale={1.05} speed={1} color="#22d3ee" teeth={18} />
      <Gear position={[4.6, -1.6, -1]} scale={0.6} speed={-1.6} color="#60a5fa" teeth={12} />
      <Gear position={[-4.2, -1.9, -1.5]} scale={0.8} speed={1.2} color="#334155" teeth={14} />
      <TorusField />
      <Particles />
    </Canvas>
  );
}
