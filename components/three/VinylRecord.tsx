'use client';

import { useMemo, useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import type { ThreeEvent } from '@react-three/fiber';
import * as THREE from 'three';
import { scene as store, damp } from '@/lib/store';

/**
 * A single upright vinyl record. The disc geometry + material are created once
 * in the gallery and passed in (shared across every record); only the two
 * label textures — front (title) and back (description) — are per-record.
 *
 * Interaction: rotates slowly on its own axis; on hover it slows, scales up,
 * lifts and glows gold; on click it flips to reveal the description on the back.
 */
export type RecordData = {
  title: string;
  subtitle: string; // small line under the title on the front label
  description: string; // shown on the back after a flip
  href: string;
};

/** Draw a vinyl-style label onto a canvas → texture. SWAP: draw a real
 *  thumbnail with `ctx.drawImage(img, …)` where noted. */
function makeLabel(title: string, sub: string, opts?: { back?: boolean }): THREE.CanvasTexture {
  const S = 512;
  const c = document.createElement('canvas');
  c.width = c.height = S;
  const ctx = c.getContext('2d')!;
  // Paper-white label
  ctx.fillStyle = '#FFFFFF';
  ctx.beginPath();
  ctx.arc(S / 2, S / 2, S / 2, 0, Math.PI * 2);
  ctx.fill();
  // Concentric gold rings
  ctx.strokeStyle = '#C8A047';
  ctx.lineWidth = 4;
  [S * 0.46, S * 0.34].forEach((r) => {
    ctx.beginPath();
    ctx.arc(S / 2, S / 2, r, 0, Math.PI * 2);
    ctx.stroke();
  });
  // SWAP: to show a real thumbnail, load an <img> and:
  //   ctx.save(); ctx.beginPath(); ctx.arc(S/2, S*0.34, 60,0,Math.PI*2);
  //   ctx.clip(); ctx.drawImage(img, S/2-60, S*0.34-60, 120,120); ctx.restore();

  ctx.textAlign = 'center';
  ctx.fillStyle = '#1A1A1A';
  if (opts?.back) {
    // Wrapped description on the back label
    ctx.font = '600 26px Georgia, serif';
    wrap(ctx, title, S / 2, S * 0.34, S * 0.62, 34);
    ctx.fillStyle = '#5A5A5A';
    ctx.font = '400 22px Georgia, serif';
    wrap(ctx, sub, S / 2, S * 0.5, S * 0.66, 30);
  } else {
    ctx.font = '700 40px Georgia, serif';
    ctx.fillText(title, S / 2, S / 2 + 8, S * 0.6);
    ctx.fillStyle = '#8A8A8A';
    ctx.font = '400 22px Georgia, serif';
    ctx.fillText(sub, S / 2, S / 2 + 46, S * 0.6);
  }
  const tex = new THREE.CanvasTexture(c);
  tex.anisotropy = 4;
  tex.needsUpdate = true;
  return tex;
}

function wrap(ctx: CanvasRenderingContext2D, text: string, x: number, y: number, maxW: number, lh: number) {
  const words = text.split(' ');
  let line = '';
  let yy = y;
  for (const w of words) {
    const test = line ? `${line} ${w}` : w;
    if (ctx.measureText(test).width > maxW && line) {
      ctx.fillText(line, x, yy);
      line = w;
      yy += lh;
    } else line = test;
  }
  if (line) ctx.fillText(line, x, yy);
}

export default function VinylRecord({
  data,
  position,
  discGeometry,
  discMaterial,
  labelGeometry,
  spinDir = 1,
}: {
  data: RecordData;
  position: [number, number, number];
  discGeometry: THREE.CylinderGeometry;
  discMaterial: THREE.Material;
  labelGeometry: THREE.CylinderGeometry;
  spinDir?: number;
}) {
  const group = useRef<THREE.Group>(null);
  const disc = useRef<THREE.Group>(null);
  const glow = useRef<THREE.MeshBasicMaterial>(null);
  const [hovered, setHovered] = useState(false);
  const [flipped, setFlipped] = useState(false);
  const spin = useRef(Math.random() * Math.PI * 2);

  const frontTex = useMemo(() => makeLabel(data.title, data.subtitle), [data.title, data.subtitle]);
  const backTex = useMemo(
    () => makeLabel(data.description, '', { back: true }),
    [data.description],
  );

  useFrame((_, dt) => {
    if (!store.active) return;
    const d = Math.min(dt, 0.05);
    const idle = store.reducedMotion ? 0 : 1;

    // Spin about the disc's face axis: slower on hover, frozen when flipped
    // (so the description stays readable) or under reduced motion.
    const speed = (flipped ? 0 : hovered ? 0.18 : 0.6) * idle * spinDir;
    spin.current += speed * d;
    if (disc.current) disc.current.rotation.z = spin.current;

    if (group.current) {
      const targetScale = hovered ? 1.12 : 1;
      const s = damp(group.current.scale.x, targetScale, 6, d);
      group.current.scale.setScalar(s);
      // Lift on hover
      group.current.position.y = damp(group.current.position.y, position[1] + (hovered ? 0.18 : 0), 6, d);
      // Flip to reveal the back
      const targetY = flipped ? Math.PI : 0;
      group.current.rotation.y = damp(group.current.rotation.y, targetY, 7, d);
    }
    if (glow.current) glow.current.opacity = damp(glow.current.opacity, hovered ? 0.5 : 0, 8, d);
  });

  const onOver = (e: ThreeEvent<PointerEvent>) => {
    e.stopPropagation();
    setHovered(true);
    document.body.style.cursor = 'pointer';
  };
  const onOut = () => {
    setHovered(false);
    document.body.style.cursor = '';
  };
  const onClick = (e: ThreeEvent<MouseEvent>) => {
    e.stopPropagation();
    setFlipped((f) => !f); // flip reveals the description; swap for navigation:
    // window.location.hash = data.href;
  };

  return (
    <group ref={group} position={position}>
      {/* Gold glow halo — fades in on hover */}
      <mesh position={[0, 0, -0.06]} scale={1.06}>
        <circleGeometry args={[0.95, 48]} />
        <meshBasicMaterial ref={glow} color="#C8A047" transparent opacity={0} depthWrite={false} />
      </mesh>

      <group
        ref={disc}
        onPointerOver={onOver}
        onPointerOut={onOut}
        onClick={onClick}
      >
        {/* Shared disc geometry + material (reused across all records) */}
        <mesh geometry={discGeometry} material={discMaterial} castShadow receiveShadow />
        {/* Front label */}
        <mesh geometry={labelGeometry} position={[0, 0, 0.028]}>
          <meshStandardMaterial map={frontTex} roughness={0.6} metalness={0} />
        </mesh>
        {/* Back label (revealed on flip) */}
        <mesh geometry={labelGeometry} position={[0, 0, -0.028]} rotation={[0, Math.PI, 0]}>
          <meshStandardMaterial map={backTex} roughness={0.6} metalness={0} />
        </mesh>
        {/* Spindle hole */}
        <mesh position={[0, 0, 0]}>
          <cylinderGeometry args={[0.03, 0.03, 0.12, 16]} />
          <meshStandardMaterial color="#FFFFFF" />
        </mesh>
      </group>
    </group>
  );
}
