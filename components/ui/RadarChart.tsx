'use client';

import { useRef } from 'react';
import { motion, useInView } from 'framer-motion';
import { radarAxes } from '@/content/resume';

const SIZE = 380;
const CENTER = SIZE / 2;
const RADIUS = 132;
const RINGS = 4;

function polar(angle: number, r: number): [number, number] {
  return [CENTER + r * Math.cos(angle - Math.PI / 2), CENTER + r * Math.sin(angle - Math.PI / 2)];
}

/** Animated SVG radar chart of core competency areas. */
export default function RadarChart() {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, margin: '-80px' });
  const n = radarAxes.length;

  const points = radarAxes
    .map((axis, i) => {
      const [x, y] = polar((i / n) * Math.PI * 2, (axis.value / 100) * RADIUS);
      return `${x},${y}`;
    })
    .join(' ');

  return (
    <div ref={ref} className="relative mx-auto w-full max-w-[420px]">
      <svg viewBox={`0 0 ${SIZE} ${SIZE}`} className="h-auto w-full">
        {/* rings */}
        {Array.from({ length: RINGS }).map((_, ring) => {
          const r = ((ring + 1) / RINGS) * RADIUS;
          const ringPoints = Array.from({ length: n })
            .map((_, i) => polar((i / n) * Math.PI * 2, r).join(','))
            .join(' ');
          return (
            <polygon
              key={ring}
              points={ringPoints}
              fill="none"
              stroke="rgb(var(--line))"
              strokeWidth="1"
              opacity={0.7}
            />
          );
        })}
        {/* spokes */}
        {radarAxes.map((_, i) => {
          const [x, y] = polar((i / n) * Math.PI * 2, RADIUS);
          return (
            <line
              key={i}
              x1={CENTER}
              y1={CENTER}
              x2={x}
              y2={y}
              stroke="rgb(var(--line))"
              strokeWidth="1"
              opacity={0.7}
            />
          );
        })}
        {/* data polygon */}
        <motion.polygon
          points={points}
          fill="rgb(var(--accent) / 0.14)"
          stroke="rgb(var(--accent))"
          strokeWidth="1.6"
          initial={{ opacity: 0, scale: 0.4 }}
          animate={inView ? { opacity: 1, scale: 1 } : {}}
          transition={{ duration: 1, ease: [0.22, 1, 0.36, 1] }}
          style={{ transformOrigin: `${CENTER}px ${CENTER}px` }}
        />
        {/* vertices */}
        {radarAxes.map((axis, i) => {
          const [x, y] = polar((i / n) * Math.PI * 2, (axis.value / 100) * RADIUS);
          return (
            <motion.circle
              key={axis.axis}
              cx={x}
              cy={y}
              r="3.5"
              fill="rgb(var(--bg))"
              stroke="rgb(var(--accent))"
              strokeWidth="1.6"
              initial={{ opacity: 0 }}
              animate={inView ? { opacity: 1 } : {}}
              transition={{ delay: 0.6 + i * 0.08 }}
            />
          );
        })}
        {/* labels */}
        {radarAxes.map((axis, i) => {
          const [x, y] = polar((i / n) * Math.PI * 2, RADIUS + 28);
          return (
            <motion.text
              key={axis.axis}
              x={x}
              y={y}
              textAnchor="middle"
              dominantBaseline="middle"
              className="font-mono"
              fontSize="9.5"
              fill="rgb(var(--muted))"
              initial={{ opacity: 0 }}
              animate={inView ? { opacity: 1 } : {}}
              transition={{ delay: 0.8 + i * 0.06 }}
            >
              {axis.axis}
            </motion.text>
          );
        })}
      </svg>
    </div>
  );
}
