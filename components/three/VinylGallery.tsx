'use client';

import { useMemo } from 'react';
import * as THREE from 'three';
import VinylRecord, { type RecordData } from './VinylRecord';
import { facets, latestPosts } from '@/content/site';

/**
 * VinylGallery — the Facets and Latest Posts cards as floating upright vinyl
 * records on one shared white stage. A single disc geometry + material and a
 * single label geometry are created here and reused across every record, so
 * the whole gallery is cheap to render.
 */
export default function VinylGallery() {
  // Shared, reused resources ------------------------------------------------
  const { discGeometry, labelGeometry, discMaterial } = useMemo(() => {
    // Cylinder axis rotated to Z so the flat faces point at the camera.
    const disc = new THREE.CylinderGeometry(0.9, 0.9, 0.05, 64);
    disc.rotateX(Math.PI / 2);
    const label = new THREE.CylinderGeometry(0.36, 0.36, 0.05, 48);
    label.rotateX(Math.PI / 2);
    const mat = new THREE.MeshStandardMaterial({ color: '#141414', roughness: 0.5, metalness: 0.15 });
    return { discGeometry: disc, labelGeometry: label, discMaterial: mat };
  }, []);

  // Records: the three Facets + the three Latest Posts.
  const records: RecordData[] = useMemo(
    () => [
      ...facets.cards.map((c) => ({
        title: c.title,
        subtitle: 'Facet',
        description: c.blurb,
        href: c.href,
      })),
      ...latestPosts.cards.map((c) => ({
        title: c.title,
        subtitle: 'Latest Post',
        description: c.blurb,
        href: c.href,
      })),
    ],
    [],
  );

  // Lay them out in a gentle arc so the gallery reads as one composition.
  const layout = useMemo(() => {
    const n = records.length;
    return records.map((_, i) => {
      const t = n > 1 ? i / (n - 1) - 0.5 : 0; // -0.5 → 0.5
      const x = t * 9.2;
      const z = -Math.abs(t) * 2.4 - 1.4; // ends recede for depth
      const y = -0.55 + Math.sin(t * Math.PI) * 0.12;
      return [x, y, z] as [number, number, number];
    });
  }, [records]);

  return (
    <group position={[0, -0.55, -1.6]}>
      {records.map((data, i) => (
        <VinylRecord
          key={data.title}
          data={data}
          position={layout[i]}
          discGeometry={discGeometry}
          labelGeometry={labelGeometry}
          discMaterial={discMaterial}
          spinDir={i % 2 === 0 ? 1 : -1}
        />
      ))}
    </group>
  );
}
