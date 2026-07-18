'use client';

/**
 * Stylized COMSOL-style result plots, one per simulation card. These are
 * illustrative scientific schematics (colormaps, contour isolines,
 * streamlines, particle traces), not real result data — built as inline SVG
 * so every card has a custom, animated visual with no stock imagery.
 *
 * `kind` maps to the simulation's icon key from content/resume.ts.
 */

const dim = 'rgb(var(--faint))';

/** Small vertical colour-legend bar, drawn on the right edge of the plot. */
function Legend({ id, hi, lo }: { id: string; hi: string; lo: string }) {
  return (
    <g fontFamily="monospace" fontSize="6" fill={dim}>
      <rect x="224" y="22" width="7" height="86" rx="1.5" fill={`url(#${id})`} stroke="rgb(var(--line))" />
      <text x="227.5" y="18" textAnchor="middle">{hi}</text>
      <text x="227.5" y="118" textAnchor="middle">{lo}</text>
    </g>
  );
}

function Frame({ label }: { label: string }) {
  return (
    <>
      <rect x="10" y="12" width="206" height="116" rx="4" fill="none" stroke="rgb(var(--line))" />
      <text x="16" y="123" fontFamily="monospace" fontSize="6.5" fill={dim}>
        {label}
      </text>
    </>
  );
}

/* ── 1 · Electromagnetic Simulation ─────────────────────────────── */
function Electromagnetic() {
  return (
    <svg viewBox="0 0 240 140" className="h-full w-full">
      <defs>
        <radialGradient id="em-field" cx="50%" cy="88%" r="75%">
          <stop offset="0%" stopColor="#ff3b30" />
          <stop offset="22%" stopColor="#ff9500" />
          <stop offset="44%" stopColor="#ffd60a" />
          <stop offset="64%" stopColor="#34c759" />
          <stop offset="82%" stopColor="#0a84ff" />
          <stop offset="100%" stopColor="#0b1e4f" />
        </radialGradient>
        <linearGradient id="em-legend" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#ff3b30" />
          <stop offset="30%" stopColor="#ffd60a" />
          <stop offset="60%" stopColor="#34c759" />
          <stop offset="100%" stopColor="#0b1e4f" />
        </linearGradient>
        <clipPath id="em-clip">
          <rect x="10" y="12" width="206" height="116" rx="4" />
        </clipPath>
      </defs>

      <g clipPath="url(#em-clip)">
        <rect x="10" y="12" width="206" height="116" fill="url(#em-field)" opacity="0.5" />
        {/* |B| contour isolines */}
        {[62, 48, 34, 22].map((r, i) => (
          <ellipse
            key={i}
            cx="113"
            cy="124"
            rx={r * 1.5}
            ry={r}
            fill="none"
            stroke="rgb(var(--ink))"
            strokeOpacity="0.25"
            strokeWidth="0.7"
          />
        ))}
        {/* B-field streamlines arcing pole to pole */}
        {[0, 1, 2].map((i) => (
          <path
            key={i}
            d={`M ${72 - i * 14} 118 C ${80 - i * 8} ${70 - i * 14}, ${146 + i * 8} ${70 - i * 14}, ${154 + i * 14} 118`}
            fill="none"
            stroke="rgb(var(--ink))"
            strokeOpacity="0.55"
            strokeWidth="1"
            strokeDasharray="3 3"
          >
            <animate attributeName="stroke-dashoffset" values="12;0" dur="1.4s" repeatCount="indefinite" />
          </path>
        ))}
      </g>

      {/* magnet poles + target */}
      <rect x="60" y="118" width="106" height="6" fill="rgb(var(--card))" stroke="rgb(var(--line))" />
      <rect x="66" y="120" width="16" height="8" fill="#0a84ff" opacity="0.9" />
      <rect x="107" y="120" width="12" height="8" fill="#ff3b30" opacity="0.9" />
      <rect x="144" y="120" width="16" height="8" fill="#0a84ff" opacity="0.9" />

      <Frame label="|B|  MAGNETIC FLUX DENSITY (T)" />
      <Legend id="em-legend" hi="max" lo="0" />
    </svg>
  );
}

/* ── 2 · Plasma Modelling ───────────────────────────────────────── */
function Plasma() {
  return (
    <svg viewBox="0 0 240 140" className="h-full w-full">
      <defs>
        <radialGradient id="pl-field" cx="50%" cy="55%" r="60%">
          <stop offset="0%" stopColor="#f0f921" />
          <stop offset="20%" stopColor="#fca636" />
          <stop offset="45%" stopColor="#e16462" />
          <stop offset="70%" stopColor="#b12a90" />
          <stop offset="90%" stopColor="#6a00a8" />
          <stop offset="100%" stopColor="#0d0887" />
        </radialGradient>
        <linearGradient id="pl-legend" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#f0f921" />
          <stop offset="35%" stopColor="#e16462" />
          <stop offset="70%" stopColor="#b12a90" />
          <stop offset="100%" stopColor="#0d0887" />
        </linearGradient>
        <clipPath id="pl-clip">
          <rect x="10" y="12" width="206" height="116" rx="4" />
        </clipPath>
      </defs>

      <g clipPath="url(#pl-clip)">
        <rect x="10" y="12" width="206" height="116" fill="#0d0887" opacity="0.35" />
        {/* plasma density cloud */}
        <ellipse cx="113" cy="66" rx="78" ry="40" fill="url(#pl-field)" opacity="0.85">
          <animate attributeName="rx" values="78;84;78" dur="3s" repeatCount="indefinite" />
          <animate attributeName="opacity" values="0.75;0.95;0.75" dur="3s" repeatCount="indefinite" />
        </ellipse>
        {/* density contours */}
        {[54, 40, 26].map((r, i) => (
          <ellipse key={i} cx="113" cy="66" rx={r * 1.5} ry={r * 0.78} fill="none" stroke="#fff" strokeOpacity="0.28" strokeWidth="0.7" />
        ))}
        {/* electron sparks */}
        {[0, 1, 2, 3, 4].map((i) => (
          <circle key={i} cx={70 + i * 22} cy={66} r="1.3" fill="#fff">
            <animate attributeName="cy" values="66;54;66" dur={`${1 + i * 0.3}s`} repeatCount="indefinite" />
            <animate attributeName="opacity" values="1;0.2;1" dur={`${1 + i * 0.3}s`} repeatCount="indefinite" />
          </circle>
        ))}
      </g>

      {/* target below plasma */}
      <rect x="56" y="118" width="114" height="8" fill="rgb(var(--card))" stroke="rgb(var(--line))" />

      <Frame label="nₑ  ELECTRON DENSITY (m⁻³)" />
      <Legend id="pl-legend" hi="max" lo="0" />
    </svg>
  );
}

/* ── 3 · Charged-Particle Tracing ───────────────────────────────── */
function ParticleTracing() {
  const paths = [
    'M 24 30 C 60 40, 40 70, 78 78 S 120 40, 150 66 S 196 96, 210 62',
    'M 24 60 C 54 66, 48 96, 86 96 S 128 66, 158 88 S 200 110, 210 88',
    'M 24 96 C 58 100, 52 66, 92 62 S 132 96, 164 74 S 200 52, 210 40',
  ];
  return (
    <svg viewBox="0 0 240 140" className="h-full w-full">
      <defs>
        <linearGradient id="pt-vel" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor="#0a84ff" />
          <stop offset="45%" stopColor="#34c759" />
          <stop offset="75%" stopColor="#ffd60a" />
          <stop offset="100%" stopColor="#ff3b30" />
        </linearGradient>
        <linearGradient id="pt-legend" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#ff3b30" />
          <stop offset="35%" stopColor="#ffd60a" />
          <stop offset="70%" stopColor="#34c759" />
          <stop offset="100%" stopColor="#0a84ff" />
        </linearGradient>
      </defs>

      {/* faint E×B grid */}
      {[34, 58, 82, 106].map((y) => (
        <line key={y} x1="12" y1={y} x2="214" y2={y} stroke="rgb(var(--line))" strokeOpacity="0.4" strokeWidth="0.5" />
      ))}

      {paths.map((d, i) => (
        <g key={i}>
          <path d={d} fill="none" stroke="url(#pt-vel)" strokeWidth="1.4" strokeOpacity="0.85" />
          <circle r="2.4" fill="#fff" stroke="#ff3b30" strokeWidth="0.8">
            <animateMotion dur={`${3 + i * 0.6}s`} repeatCount="indefinite" path={d} />
          </circle>
        </g>
      ))}

      <Frame label="q(E + v×B)  PARTICLE TRAJECTORIES" />
      <Legend id="pt-legend" hi="v↑" lo="v↓" />
    </svg>
  );
}

/* ── 4 · Race-Track Erosion ─────────────────────────────────────── */
function Erosion() {
  return (
    <svg viewBox="0 0 240 140" className="h-full w-full">
      <defs>
        <linearGradient id="er-track" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor="#ffd60a" />
          <stop offset="50%" stopColor="#ff9500" />
          <stop offset="100%" stopColor="#ff3b30" />
        </linearGradient>
        <linearGradient id="er-legend" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#ff3b30" />
          <stop offset="55%" stopColor="#ff9500" />
          <stop offset="100%" stopColor="#ffd60a" />
        </linearGradient>
      </defs>

      {/* target disc (top view) */}
      <circle cx="80" cy="66" r="52" fill="rgb(var(--card))" stroke="rgb(var(--line))" />
      {/* erosion racetrack groove */}
      <ellipse cx="80" cy="66" rx="34" ry="34" fill="none" stroke="url(#er-track)" strokeWidth="9" strokeOpacity="0.9">
        <animate attributeName="stroke-width" values="7;10;7" dur="3s" repeatCount="indefinite" />
      </ellipse>
      <ellipse cx="80" cy="66" rx="34" ry="34" fill="none" stroke="#7f1d1d" strokeWidth="2" strokeOpacity="0.5" />
      <circle cx="80" cy="66" r="52" fill="none" stroke="rgb(var(--faint))" strokeDasharray="2 3" strokeOpacity="0.5" />

      {/* erosion depth cross-section */}
      <g transform="translate(150 34)">
        <line x1="0" y1="0" x2="0" y2="66" stroke="rgb(var(--line))" />
        <line x1="0" y1="66" x2="60" y2="66" stroke="rgb(var(--line))" />
        <path
          d="M 0 8 L 12 8 C 18 8, 18 40, 24 40 C 30 40, 30 8, 36 8 L 36 8 C 42 8, 42 40, 48 40 C 54 40, 54 8, 60 8"
          fill="none"
          stroke="url(#er-track)"
          strokeWidth="1.6"
          strokeDasharray="150"
          strokeDashoffset="150"
        >
          <animate attributeName="stroke-dashoffset" values="150;0" dur="3s" repeatCount="indefinite" />
        </path>
        <text x="2" y="-2" fontFamily="monospace" fontSize="5.5" fill={dim}>depth</text>
      </g>

      <Frame label="TARGET EROSION PROFILE (mm)" />
      <Legend id="er-legend" hi="deep" lo="0" />
    </svg>
  );
}

/* ── 5 · Transformer Flux Analysis ──────────────────────────────── */
function TransformerFlux() {
  return (
    <svg viewBox="0 0 240 140" className="h-full w-full">
      <defs>
        <linearGradient id="tf-core" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#34c759" />
          <stop offset="50%" stopColor="#ffd60a" />
          <stop offset="100%" stopColor="#ff3b30" />
        </linearGradient>
        <linearGradient id="tf-legend" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#ff3b30" />
          <stop offset="50%" stopColor="#ffd60a" />
          <stop offset="100%" stopColor="#0a84ff" />
        </linearGradient>
      </defs>

      {/* E-core */}
      <path
        d="M 40 28 H 150 V 104 H 40 Z M 62 46 H 128 V 86 H 62 Z"
        fill="url(#tf-core)"
        fillOpacity="0.28"
        fillRule="evenodd"
        stroke="rgb(var(--line))"
      />
      {/* flux loops through the core window */}
      {[0, 1, 2].map((i) => (
        <ellipse key={i} cx="95" cy="66" rx={12 + i * 7} ry={26 + i * 6} fill="none" stroke="#0a84ff" strokeOpacity={0.7 - i * 0.15} strokeWidth="1" strokeDasharray="4 3">
          <animate attributeName="stroke-dashoffset" values="14;0" dur="1.6s" repeatCount="indefinite" />
        </ellipse>
      ))}
      {/* windings (current density colormap) */}
      {[0, 1, 2, 3].map((i) => (
        <rect key={`p${i}`} x="44" y={48 + i * 10} width="14" height="7" rx="1.5" fill="#ff9500" opacity="0.85" />
      ))}
      {[0, 1, 2, 3].map((i) => (
        <rect key={`s${i}`} x="132" y={48 + i * 10} width="14" height="7" rx="1.5" fill="#ffd60a" opacity="0.85" />
      ))}

      <Frame label="Φ  MAGNETIC FLUX · J CURRENT DENSITY" />
      <Legend id="tf-legend" hi="J max" lo="0" />
    </svg>
  );
}

/* ── 6 · Machining & Tribology FEA ──────────────────────────────── */
function MachiningFea() {
  return (
    <svg viewBox="0 0 240 140" className="h-full w-full">
      <defs>
        <radialGradient id="fe-stress" cx="50%" cy="50%" r="55%">
          <stop offset="0%" stopColor="#ff3b30" />
          <stop offset="30%" stopColor="#ff9500" />
          <stop offset="55%" stopColor="#ffd60a" />
          <stop offset="78%" stopColor="#34c759" />
          <stop offset="100%" stopColor="#0a84ff" />
        </radialGradient>
        <linearGradient id="fe-legend" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#ff3b30" />
          <stop offset="35%" stopColor="#ffd60a" />
          <stop offset="70%" stopColor="#34c759" />
          <stop offset="100%" stopColor="#0a84ff" />
        </linearGradient>
        <clipPath id="fe-clip">
          <rect x="10" y="70" width="206" height="58" />
        </clipPath>
      </defs>

      {/* workpiece with stress field */}
      <g clipPath="url(#fe-clip)">
        <rect x="10" y="70" width="206" height="58" fill="#0a84ff" opacity="0.18" />
        <ellipse cx="120" cy="74" rx="46" ry="30" fill="url(#fe-stress)" opacity="0.8" />
        {/* FE mesh */}
        {Array.from({ length: 11 }).map((_, i) => (
          <line key={`v${i}`} x1={20 + i * 18} y1="70" x2={20 + i * 18} y2="128" stroke="rgb(var(--ink))" strokeOpacity="0.12" strokeWidth="0.5" />
        ))}
        {Array.from({ length: 4 }).map((_, i) => (
          <line key={`h${i}`} x1="10" y1={82 + i * 12} x2="216" y2={82 + i * 12} stroke="rgb(var(--ink))" strokeOpacity="0.12" strokeWidth="0.5" />
        ))}
        {Array.from({ length: 11 }).map((_, i) => (
          <line key={`d${i}`} x1={20 + i * 18} y1="70" x2={38 + i * 18} y2="128" stroke="rgb(var(--ink))" strokeOpacity="0.1" strokeWidth="0.5" />
        ))}
      </g>

      {/* cutting tool */}
      <g>
        <path d="M 132 30 L 152 30 L 152 66 L 120 66 Z" fill="rgb(var(--card))" stroke="rgb(var(--accent))" />
        <path d="M 120 66 L 132 30" stroke="rgb(var(--accent))" strokeWidth="1.4" />
        <animateTransform attributeName="transform" type="translate" values="0 0; -3 2; 0 0" dur="0.6s" repeatCount="indefinite" />
      </g>
      {/* chip curl */}
      <path d="M 120 66 C 104 58, 100 44, 112 40" fill="none" stroke="#ff9500" strokeWidth="2" strokeOpacity="0.8" />

      <Frame label="σ  VON MISES STRESS (MPa)" />
      <Legend id="fe-legend" hi="σ max" lo="0" />
    </svg>
  );
}

const visuals: Record<string, () => JSX.Element> = {
  magnet: Electromagnetic,
  zap: Plasma,
  orbit: ParticleTracing,
  'circle-dot': Erosion,
  activity: TransformerFlux,
  layers: MachiningFea,
};

export default function SimulationVisual({ kind }: { kind: string }) {
  const Visual = visuals[kind] ?? MachiningFea;
  return (
    <div className="eng-grid-fine relative h-full w-full bg-bg">
      <Visual />
    </div>
  );
}
