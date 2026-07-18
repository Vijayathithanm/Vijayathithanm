'use client';

/**
 * Custom animated SVG schematics — one per project. Drawn as engineering
 * blueprints so every card feels custom-built, no stock imagery.
 */

const stroke = 'rgb(var(--accent))';
const stroke2 = 'rgb(var(--accent2))';
const dim = 'rgb(var(--faint))';

function Magnetron() {
  return (
    <svg viewBox="0 0 200 120" fill="none" className="h-full w-full">
      {/* vacuum chamber */}
      <rect x="20" y="14" width="160" height="92" rx="6" stroke={dim} strokeDasharray="4 4" />
      {/* target */}
      <rect x="55" y="20" width="90" height="8" stroke={stroke} fill="rgb(var(--accent) / 0.08)" />
      {/* magnets */}
      <rect x="60" y="10" width="18" height="10" stroke={stroke2} />
      <rect x="122" y="10" width="18" height="10" stroke={stroke2} />
      <text x="64" y="18" fill={stroke2} fontSize="6" fontFamily="monospace">N</text>
      <text x="127" y="18" fill={stroke2} fontSize="6" fontFamily="monospace">S</text>
      {/* field lines */}
      <path d="M69 20 C 69 44, 131 44, 131 20" stroke={stroke2} opacity="0.6" />
      <path d="M75 20 C 75 36, 125 36, 125 20" stroke={stroke2} opacity="0.4" />
      <path d="M63 20 C 63 52, 137 52, 137 20" stroke={stroke2} opacity="0.3" />
      {/* plasma glow */}
      <ellipse cx="100" cy="40" rx="34" ry="9" fill="rgb(var(--plasma) / 0.18)">
        <animate attributeName="ry" values="9;12;9" dur="3s" repeatCount="indefinite" />
      </ellipse>
      {/* particle traces */}
      {[0, 1, 2].map((i) => (
        <circle key={i} r="1.6" fill={stroke}>
          <animateMotion
            dur={`${2.4 + i * 0.7}s`}
            repeatCount="indefinite"
            path={`M ${72 + i * 24} 30 C ${80 + i * 20} 44, ${110 - i * 10} 46, ${118 - i * 16} 30`}
          />
        </circle>
      ))}
      {/* substrate */}
      <rect x="65" y="88" width="70" height="6" stroke={dim} />
      <text x="80" y="102" fill={dim} fontSize="6" fontFamily="monospace">SUBSTRATE</text>
    </svg>
  );
}

function Vmc() {
  return (
    <svg viewBox="0 0 200 120" fill="none" className="h-full w-full">
      {/* column */}
      <path d="M120 18 h44 v84 h-24 v-58 h-20 z" stroke={stroke} fill="rgb(var(--accent) / 0.05)" />
      {/* base */}
      <rect x="26" y="94" width="148" height="12" stroke={stroke} fill="rgb(var(--accent) / 0.05)" />
      {/* table + saddle */}
      <rect x="34" y="78" width="82" height="8" stroke={stroke2} />
      <rect x="46" y="86" width="58" height="8" stroke={dim} />
      {/* spindle head */}
      <g>
        <rect x="96" y="30" width="26" height="26" stroke={stroke2} fill="rgb(var(--accent2) / 0.08)" />
        <rect x="104" y="56" width="10" height="14" stroke={stroke} />
        <animateTransform
          attributeName="transform"
          type="translate"
          values="0 0; 0 8; 0 0"
          dur="4s"
          repeatCount="indefinite"
        />
      </g>
      {/* tool */}
      <path d="M109 70 l0 6 M106 76 l6 0" stroke={stroke} />
      {/* dimension lines */}
      <path d="M26 112 h148" stroke={dim} strokeDasharray="2 3" />
      <path d="M18 18 v88" stroke={dim} strokeDasharray="2 3" />
      <text x="80" y="118" fill={dim} fontSize="6" fontFamily="monospace">X-TRAVEL</text>
      <text x="6" y="64" fill={dim} fontSize="6" fontFamily="monospace" transform="rotate(-90 10 64)">Z-AXIS</text>
      {/* stress fringe hint */}
      <path d="M124 44 q10 16 -2 46" stroke="rgb(var(--plasma))" opacity="0.5" strokeDasharray="3 3" />
    </svg>
  );
}

function Coating() {
  return (
    <svg viewBox="0 0 200 120" fill="none" className="h-full w-full">
      {/* substrate */}
      <rect x="30" y="82" width="140" height="20" stroke={dim} fill="rgb(var(--line) / 0.2)" />
      <text x="82" y="95" fill={dim} fontSize="7" fontFamily="monospace">EN19 STEEL</text>
      {/* Cr interlayer */}
      <rect x="30" y="72" width="140" height="10" stroke={stroke2} fill="rgb(var(--accent2) / 0.12)" />
      <text x="174" y="80" fill={stroke2} fontSize="6" fontFamily="monospace">Cr</text>
      {/* TiB2 */}
      <rect x="30" y="62" width="140" height="10" stroke={stroke2} fill="rgb(var(--accent2) / 0.2)" />
      <text x="174" y="70" fill={stroke2} fontSize="6" fontFamily="monospace">TiB₂</text>
      {/* DLC */}
      <rect x="30" y="48" width="140" height="14" stroke={stroke} fill="rgb(var(--accent) / 0.18)" />
      <text x="174" y="58" fill={stroke} fontSize="6" fontFamily="monospace">DLC</text>
      {/* sputtered atoms */}
      {[0, 1, 2, 3, 4].map((i) => (
        <circle key={i} cx={45 + i * 28} cy="20" r="2" fill={stroke}>
          <animate
            attributeName="cy"
            values="14;46"
            dur={`${1.4 + i * 0.3}s`}
            repeatCount="indefinite"
          />
          <animate attributeName="opacity" values="1;0" dur={`${1.4 + i * 0.3}s`} repeatCount="indefinite" />
        </circle>
      ))}
      <text x="30" y="12" fill={dim} fontSize="6" fontFamily="monospace">SPUTTER FLUX ↓</text>
    </svg>
  );
}

function Drill() {
  return (
    <svg viewBox="0 0 200 120" fill="none" className="h-full w-full">
      {/* CFRP laminate */}
      {[0, 1, 2, 3, 4].map((i) => (
        <rect key={i} x="30" y={64 + i * 7} width="140" height="7" stroke={dim} opacity={0.8 - i * 0.1} />
      ))}
      <text x="34" y="112" fill={dim} fontSize="6" fontFamily="monospace">CFRP LAMINATE</text>
      {/* Ti layer */}
      <rect x="30" y="99" width="140" height="8" stroke={stroke2} fill="rgb(var(--accent2) / 0.1)" />
      <text x="150" y="112" fill={stroke2} fontSize="6" fontFamily="monospace">Ti-6Al-4V</text>
      {/* drill */}
      <g>
        <rect x="92" y="8" width="16" height="34" stroke={stroke} fill="rgb(var(--accent) / 0.08)" />
        <path d="M92 42 L100 60 L108 42 Z" stroke={stroke} fill="rgb(var(--accent) / 0.12)" />
        <path d="M94 14 l12 8 M94 24 l12 8 M94 34 l12 6" stroke={stroke} opacity="0.6" />
        <animateTransform
          attributeName="transform"
          type="translate"
          values="0 0; 0 7; 0 0"
          dur="3s"
          repeatCount="indefinite"
        />
      </g>
      {/* AE waves */}
      {[0, 1, 2].map((i) => (
        <circle key={i} cx="100" cy="66" r={6 + i * 8} stroke={stroke} fill="none" opacity={0.5 - i * 0.15}>
          <animate attributeName="r" values={`${6 + i * 8};${20 + i * 8}`} dur="2s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.5;0" dur="2s" repeatCount="indefinite" />
        </circle>
      ))}
      {/* cryo */}
      <text x="16" y="30" fill={stroke2} fontSize="7" fontFamily="monospace">LN₂</text>
      <path d="M28 32 q16 8 40 12" stroke={stroke2} strokeDasharray="3 3" opacity="0.7" />
    </svg>
  );
}

function Ae() {
  return (
    <svg viewBox="0 0 200 120" fill="none" className="h-full w-full">
      {/* axes */}
      <path d="M24 12 v88 h152" stroke={dim} />
      <text x="10" y="60" fill={dim} fontSize="6" fontFamily="monospace" transform="rotate(-90 14 60)">AE-RMS</text>
      <text x="90" y="112" fill={dim} fontSize="6" fontFamily="monospace">TIME</text>
      {/* AE burst signal */}
      <path
        d="M24 66 L40 66 L44 50 L48 78 L52 58 L56 70 L64 66 L80 66 L84 40 L88 88 L92 46 L96 76 L100 60 L104 66 L124 66 L128 30 L132 92 L136 36 L140 84 L144 54 L148 70 L156 66 L176 66"
        stroke={stroke}
        strokeWidth="1.2"
        strokeDasharray="600"
        strokeDashoffset="600"
      >
        <animate attributeName="stroke-dashoffset" values="600;0" dur="4s" repeatCount="indefinite" />
      </path>
      {/* threshold */}
      <path d="M24 42 h152" stroke="rgb(var(--plasma))" strokeDasharray="4 4" opacity="0.6" />
      <text x="130" y="38" fill="rgb(var(--plasma))" fontSize="6" fontFamily="monospace">WEAR LIMIT</text>
      {/* prediction band */}
      <rect x="124" y="14" width="34" height="86" fill="rgb(var(--accent) / 0.06)" stroke={stroke} strokeDasharray="2 3" opacity="0.7" />
      <text x="126" y="22" fill={stroke} fontSize="6" fontFamily="monospace">SVM ►</text>
    </svg>
  );
}

function Robot() {
  return (
    <svg viewBox="0 0 200 120" fill="none" className="h-full w-full">
      {/* obstacles */}
      <rect x="60" y="30" width="30" height="24" stroke={dim} />
      <circle cx="130" cy="72" r="16" stroke={dim} />
      <rect x="96" y="88" width="26" height="18" stroke={dim} />
      {/* start / goal */}
      <circle cx="30" cy="96" r="5" stroke={stroke} fill="rgb(var(--accent) / 0.15)" />
      <text x="22" y="112" fill={stroke} fontSize="6" fontFamily="monospace">START</text>
      <circle cx="172" cy="20" r="5" stroke={stroke2} fill="rgb(var(--accent2) / 0.15)" />
      <text x="160" y="12" fill={stroke2} fontSize="6" fontFamily="monospace">GOAL</text>
      {/* tangent bug path */}
      <path
        d="M30 96 L56 62 Q52 44 62 28 L92 26 Q104 40 112 56 L146 60 Q158 44 172 20"
        stroke={stroke}
        strokeDasharray="260"
        strokeDashoffset="260"
        fill="none"
      >
        <animate attributeName="stroke-dashoffset" values="260;0" dur="3.5s" repeatCount="indefinite" />
      </path>
      {/* robot dot */}
      <circle r="3" fill={stroke}>
        <animateMotion
          dur="3.5s"
          repeatCount="indefinite"
          path="M30 96 L56 62 Q52 44 62 28 L92 26 Q104 40 112 56 L146 60 Q158 44 172 20"
        />
      </circle>
    </svg>
  );
}

const visuals = {
  magnetron: Magnetron,
  vmc: Vmc,
  coating: Coating,
  drill: Drill,
  ae: Ae,
  robot: Robot,
};

export default function ProjectVisual({ kind }: { kind: keyof typeof visuals }) {
  const Visual = visuals[kind];
  return (
    <div className="eng-grid-fine relative h-full w-full p-4">
      <Visual />
    </div>
  );
}
