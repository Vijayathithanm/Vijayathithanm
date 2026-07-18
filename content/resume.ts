/**
 * ─────────────────────────────────────────────────────────────────────────────
 *  SINGLE SOURCE OF TRUTH
 *  All site content lives here. Edit this file to update the website —
 *  no component changes required.
 * ─────────────────────────────────────────────────────────────────────────────
 */

export const profile = {
  name: 'Vijayathithan Mathiyazhagan',
  shortName: 'Vijayathithan',
  initials: 'VM',
  title: 'Research & Development Engineer',
  tagline: 'Advanced Manufacturing · Surface Engineering · Multiphysics Simulation',
  roles: [
    'R&D Engineer',
    'Simulation Scientist',
    'Product Developer',
    'Surface Engineering Specialist',
    'Machine Designer',
  ],
  summary:
    'Mechanical engineer with a Ph.D. from IIT Madras, specialising in HiPIMS-based PVD coating technology, indigenous magnetron development, and multiphysics simulation. Currently leading the end-to-end development of an in-house Vertical Machining Center — from concept to realization — backed by deep expertise in finite element analysis, acoustic-emission tool prognostics, and machine learning for manufacturing.',
  location: 'Bengaluru, India',
  company: 'Addlife Coatings Pvt. Ltd.',
  email: 'mv.athithan@gmail.com',
  phone: '+91 96009 33661',
  linkedin: 'https://linkedin.com/in/vijayathithan',
  resumeFile: `${process.env.NEXT_PUBLIC_BASE_PATH ?? ''}/resume/Vijayathithan_Mathiyazhagan_CV.docx`,
  availability: 'Open to opportunities — start time negotiable, location flexible.',
};

export const stats = [
  { label: 'Years of Research', value: 7, suffix: '+', note: 'First publication 2019' },
  { label: 'Journal Publications', value: 4, suffix: '', note: 'Refereed, incl. Wear & IJAMT' },
  { label: 'Conference Papers & Talks', value: 4, suffix: '', note: 'ASME IMECE · WOM · MATADOR' },
  { label: 'Engineering Tools Mastered', value: 15, suffix: '+', note: 'CAE · CAD · ML · DAQ' },
];

export const applicationAreas = [
  'Machining of advanced aerospace materials',
  'Multiphysics modelling of magnetron & plasma',
  'Damage and tool-wear analysis',
  'Tool prognostics & digital twin',
  'Machine learning for manufacturing',
  'PVD coatings',
  'Tribological studies',
];

export type TimelineEntry = {
  period: string;
  title: string;
  org: string;
  location: string;
  kind: 'industry' | 'research' | 'education';
  highlights: string[];
};

export const experience: TimelineEntry[] = [
  {
    period: 'Mar 2024 — Present',
    title: 'Research and Development Engineer',
    org: 'Addlife Coatings Pvt. Ltd.',
    location: 'Bengaluru, India',
    kind: 'industry',
    highlights: [
      'Executed multiphysics simulations in COMSOL for indigenous magnetron development — electromagnetic and plasma simulations, charged-particle tracing in vacuum chambers, and race-track identification on target materials.',
      'Conducted in-depth studies on transformer magnetic flux, current density distribution, and current-leakage mitigation.',
      'Leading the in-house development of a Vertical Machining Center (VMC) from concept to realization — structural design validation, static & dynamic analysis, accidental impact assessment, and durability/fatigue evaluation using Abaqus and fe-safe.',
      'Conducted FEA using Abaqus and AdvantEdge to evaluate tool and coating performance.',
      'Performed coating quality assessments through tribological testing, SEM analysis, and adhesion tests.',
    ],
  },
  {
    period: 'Mar 2022 — Feb 2024',
    title: 'Research Associate',
    org: 'Indian Institute of Technology Madras',
    location: 'Chennai, India · Supervisor: Prof. N. Arunachalam',
    kind: 'research',
    highlights: [
      'Developed diamond-like carbon (DLC) coating technology to enhance tribological performance and lifespan of HSU and liner cylinders for defence applications.',
      'Conducted thin-film deposition using magnetron sputtering with TiB₂ and Cr interlayers on aerospace-grade steel.',
      'Performed SEM/EDX and Raman spectroscopy analyses to assess coating quality and sp³ content.',
      'Developed 3D finite-element models in Abaqus for wear analysis of DLC coatings on EN19 steel.',
      'Implemented machine-learning models (SVM) in Python for wear prediction; optimized coating-process parameters via ANOVA using Design Expert and Minitab.',
      'Designed and fabricated a custom chamber for tribological studies in lubricated environments.',
    ],
  },
];

export const education: TimelineEntry[] = [
  {
    period: 'Ph.D. · April 2025',
    title: 'Ph.D., Mechanical Engineering',
    org: 'Indian Institute of Technology Madras',
    location: 'Chennai · CGPA 8.25 / 10.0',
    kind: 'education',
    highlights: [
      'Thesis: Advanced Machining of Carbon Fiber Reinforced Polymers (CFRP) — Damage Mechanisms, Tool Wear, and Predictive Modelling.',
      'Candidacy: Predictive maintenance via AE-based online tool monitoring in composite-material machining.',
      'Adviser: Dr. Anil Meena · Area: Advanced Manufacturing Technology.',
    ],
  },
  {
    period: 'M.E. · April 2016',
    title: 'M.E., Manufacturing Engineering',
    org: 'Thiagarajar College of Engineering',
    location: 'Madurai · CGPA 8.37 / 10.0',
    kind: 'education',
    highlights: [
      'Thesis: Mobile Robot Path Planning Using Tangent Bug Algorithm.',
      'Adviser: Prof. C. Paramasivam · Area: Advanced Manufacturing Technology.',
    ],
  },
  {
    period: 'B.E. · April 2012',
    title: 'B.E., Mechanical Engineering',
    org: 'Anna University, Ramanathapuram Campus',
    location: 'CGPA 7.87 / 10.0',
    kind: 'education',
    highlights: [],
  },
];

export type Project = {
  id: string;
  category: 'Simulation' | 'Machine Design' | 'Coatings' | 'Research' | 'Robotics';
  title: string;
  subtitle: string;
  problem: string;
  approach: string[];
  outcome: string;
  stack: string[];
  accent: string; // tailwind gradient hint
  visual: 'magnetron' | 'vmc' | 'coating' | 'drill' | 'ae' | 'robot';
  featured?: boolean;
};

export const projects: Project[] = [
  {
    id: 'magnetron',
    category: 'Simulation',
    title: 'Indigenous Magnetron Development',
    subtitle: 'COMSOL multiphysics — electromagnetics, plasma & particle tracing',
    problem:
      'Developing an indigenous magnetron for PVD sputtering demands precise knowledge of magnetic field topology, plasma confinement, and target utilisation — before any metal is cut.',
    approach: [
      'Electromagnetic field simulation of the magnetron assembly in COMSOL Multiphysics.',
      'Plasma simulation and charged-particle tracing inside the vacuum chamber.',
      'Race-track identification on target materials to predict erosion profiles.',
      'Transformer magnetic-flux and current-density distribution studies with current-leakage mitigation.',
    ],
    outcome:
      'Simulation-driven design intelligence guiding the indigenous magnetron programme at Addlife Coatings.',
    stack: ['COMSOL Multiphysics', 'Electromagnetics', 'Plasma Physics', 'Particle Tracing'],
    accent: 'from-cyan-500 to-blue-600',
    visual: 'magnetron',
    featured: true,
  },
  {
    id: 'vmc',
    category: 'Machine Design',
    title: 'In-House Vertical Machining Center',
    subtitle: 'Concept → realization · structural, dynamic & fatigue validation',
    problem:
      'Building a VMC in-house requires the machine structure to deliver stiffness, damping, and long-term durability that rival established machine-tool OEMs.',
    approach: [
      'End-to-end ownership from concept to realization.',
      'Structural design validation of the machine frame and load path in Abaqus.',
      'Static and dynamic structural analysis for stiffness and vibration behaviour.',
      'Accidental impact load assessment for crash-case safety.',
      'Durability and fatigue-life evaluation with fe-safe.',
    ],
    outcome:
      'A validated machine structure engineered for stiffness, reliability, and long-term performance.',
    stack: ['Abaqus', 'fe-safe', 'SolidWorks', 'Machine Design', 'Fatigue Analysis'],
    accent: 'from-blue-500 to-violet-600',
    visual: 'vmc',
    featured: true,
  },
  {
    id: 'dlc',
    category: 'Coatings',
    title: 'DLC Coatings for Defence Applications',
    subtitle: 'Thin-film engineering on aerospace-grade steel · IIT Madras',
    problem:
      'HSU and liner cylinders in defence systems demand dramatically better tribological performance and service life than uncoated steel can deliver.',
    approach: [
      'Diamond-like carbon (DLC) deposition via magnetron sputtering with TiB₂ and Cr interlayers.',
      'SEM/EDX and Raman spectroscopy to quantify coating quality and sp³ content.',
      '3D finite-element wear models of DLC on EN19 steel in Abaqus.',
      'SVM-based wear prediction in Python; ANOVA process optimisation in Design Expert & Minitab.',
      'Custom-designed chamber for tribological studies in lubricated environments.',
    ],
    outcome:
      'A complete DLC coating technology stack — deposition, characterisation, simulation, and prediction.',
    stack: ['Magnetron Sputtering', 'DLC', 'Abaqus', 'Python · SVM', 'Raman', 'SEM/EDX'],
    accent: 'from-emerald-500 to-cyan-600',
    visual: 'coating',
    featured: true,
  },
  {
    id: 'cfrp',
    category: 'Research',
    title: 'CFRP & CFRP/Ti Stack Machining',
    subtitle: 'Ph.D. research — damage mechanisms, tool wear & predictive modelling',
    problem:
      'Drilling CFRP and CFRP/Ti stacks induces delamination, thermal damage, and rapid tool wear — the core cost drivers in aerospace assembly.',
    approach: [
      'Cryogenic-assisted drilling to minimise thermal damage and improve hole quality.',
      'Machining-induced damage analysis correlated with tool-wear evolution.',
      'Response Surface Methodology for damage characterisation in CFRP/Ti stacks.',
      'Published in Wear, IJAMT, and Proc. IMechE Part B.',
    ],
    outcome:
      'Doctoral thesis and four refereed journal articles advancing composite machining science.',
    stack: ['Cryogenic Machining', 'CFRP/Ti', 'RSM', 'Tool Wear Analysis'],
    accent: 'from-orange-500 to-rose-600',
    visual: 'drill',
  },
  {
    id: 'ae-monitoring',
    category: 'Research',
    title: 'AE-Based Tool Condition Monitoring',
    subtitle: 'Real-time prognostics & digital-twin foundations',
    problem:
      'Tool failure during composite machining is silent and expensive — operators need real-time, sensor-driven wear prediction.',
    approach: [
      'Acoustic-emission sensing for online tool-condition monitoring during drilling.',
      'Signal processing with Fourier and wavelet transforms in MATLAB and Python.',
      'Predictive wear modelling under dry and cryogenic conditions (published in Wear).',
      'Machine-learning pipelines (SVM, AutoML/PyCaret) for wear prediction.',
    ],
    outcome:
      'A validated AE-driven prognostics methodology for predictive maintenance of machining processes.',
    stack: ['Acoustic Emission', 'MATLAB', 'Python', 'Wavelets', 'PyCaret'],
    accent: 'from-fuchsia-500 to-purple-600',
    visual: 'ae',
  },
  {
    id: 'robot',
    category: 'Robotics',
    title: 'Mobile Robot Path Planning',
    subtitle: 'M.E. thesis — Tangent Bug Algorithm',
    problem:
      'Autonomous navigation in unknown environments requires reactive path planning with minimal sensing.',
    approach: [
      'Implemented the Tangent Bug algorithm for sensor-based mobile-robot navigation.',
      'Studied convergence and path optimality against obstacle-rich maps.',
    ],
    outcome: "Master's thesis in Manufacturing Engineering at Thiagarajar College of Engineering.",
    stack: ['Path Planning', 'Tangent Bug', 'Robotics'],
    accent: 'from-slate-400 to-slate-600',
    visual: 'robot',
  },
];

export const simulations = [
  {
    title: 'Electromagnetic Simulation',
    desc: 'Magnetic field topology of the magnetron assembly — flux density mapping across the target surface.',
    icon: 'magnet',
  },
  {
    title: 'Plasma Modelling',
    desc: 'Glow-discharge plasma behaviour inside the vacuum chamber for sputter-process insight.',
    icon: 'zap',
  },
  {
    title: 'Charged-Particle Tracing',
    desc: 'Electron and ion trajectories traced through crossed E×B fields in the vacuum chamber.',
    icon: 'orbit',
  },
  {
    title: 'Race-Track Erosion',
    desc: 'Target-erosion profile prediction to maximise target utilisation and coating uniformity.',
    icon: 'circle-dot',
  },
  {
    title: 'Transformer Flux Analysis',
    desc: 'Magnetic flux and current-density distribution studies with current-leakage mitigation.',
    icon: 'activity',
  },
  {
    title: 'Machining & Tribology FEA',
    desc: 'Abaqus, AdvantEdge and 3D Deform models for cutting mechanics, damage and wear.',
    icon: 'layers',
  },
];

export const vmcPhases = [
  {
    phase: '01',
    title: 'Concept',
    desc: 'Machine architecture definition and design intent for an in-house Vertical Machining Center.',
  },
  {
    phase: '02',
    title: 'Structural Design',
    desc: 'Design of the machine structure in SolidWorks with focus on stiffness, manufacturability, and assembly.',
  },
  {
    phase: '03',
    title: 'Static Analysis',
    desc: 'Structural design validation under static load cases in Abaqus — deflection and stress across the load path.',
  },
  {
    phase: '04',
    title: 'Dynamic Analysis',
    desc: 'Dynamic structural behaviour for machining stability and vibration performance.',
  },
  {
    phase: '05',
    title: 'Impact Assessment',
    desc: 'Accidental impact load assessment for crash-case safety of the machine structure.',
  },
  {
    phase: '06',
    title: 'Durability & Fatigue',
    desc: 'Fatigue-life and durability evaluation with fe-safe for long-term reliability.',
  },
  {
    phase: '07',
    title: 'Realization',
    desc: 'Carrying the validated design through to physical build — concept to realization, in-house.',
  },
];

export type Publication = {
  ref: string;
  authors: string;
  title: string;
  venue: string;
  year: string;
  type: 'journal' | 'conference' | 'talk';
  note?: string;
};

export const publications: Publication[] = [
  {
    ref: 'J1',
    authors: 'V. Mathiyazhagan, A. Meena',
    title:
      'Predictive modelling of tool wear in CFRP drilling using acoustic emission sensors under dry and cryogenic conditions',
    venue: 'Wear, 205930',
    year: '2025',
    type: 'journal',
  },
  {
    ref: 'J2',
    authors: 'V. Mathiyazhagan, A. Meena',
    title: 'Machining-induced damages in the drilling of CFRP under dry and cryogenic environments',
    venue: 'International Journal of Advanced Manufacturing Technology, 134(1), 605–626',
    year: '2024',
    type: 'journal',
  },
  {
    ref: 'J3',
    authors: 'V. Mathiyazhagan, A. Meena',
    title:
      'A new approach for analysing machining-induced damage in correlation with tool wear during dry drilling of CFRP/Ti stacks',
    venue: 'Proc. IMechE, Part B: Journal of Engineering Manufacture',
    year: '2024',
    type: 'journal',
  },
  {
    ref: 'J4',
    authors: 'V. Mathiyazhagan, A. Meena',
    title: 'Machining-induced damage analysis in CFRP/Ti stacks during drilling using RSM approach',
    venue: 'International Journal of Advanced Manufacturing Technology',
    year: '2025',
    type: 'journal',
    note: 'Under review',
  },
  {
    ref: 'C1',
    authors: 'V. Mathiyazhagan, A. Meena',
    title:
      'Comparative study of material damage and tool wear mechanisms during drilling of CFRP/Ti stack',
    venue: 'ASME IMECE 2019, Salt Lake City, Utah, USA · IMECE2019-11191',
    year: '2019',
    type: 'conference',
  },
  {
    ref: 'T1',
    authors: 'V. Mathiyazhagan, A. Meena',
    title:
      'Predictive modelling of tool wear in CFRP drilling using acoustic emission sensors under dry and cryogenic conditions',
    venue: '25th International Conference on Wear of Materials, Sitges, Spain',
    year: '2025',
    type: 'talk',
  },
  {
    ref: 'T2',
    authors: 'V. Mathiyazhagan, A. Meena',
    title: 'Machining-induced surface quality in the drilling of CFRP/Ti stacks',
    venue: '40th International MATADOR Conference, Hangzhou, China',
    year: '2019',
    type: 'talk',
  },
  {
    ref: 'T3',
    authors: 'V. Mathiyazhagan, A. Meena',
    title:
      'Comparative study of material damage and tool wear mechanisms during drilling of CFRP/Ti stack',
    venue: 'ASME IMECE 2019, Salt Lake City, Utah, USA',
    year: '2019',
    type: 'talk',
  },
];

export const skillGroups = [
  {
    group: 'FEA & Simulation',
    icon: 'box',
    skills: [
      { name: 'Abaqus', level: 95 },
      { name: 'COMSOL Multiphysics', level: 92 },
      { name: 'fe-safe', level: 88 },
      { name: 'AdvantEdge', level: 85 },
      { name: '3D Deform', level: 80 },
    ],
  },
  {
    group: 'CAD & Design',
    icon: 'pen-tool',
    skills: [
      { name: 'SolidWorks', level: 92 },
      { name: 'AutoCAD', level: 85 },
      { name: 'CREO', level: 80 },
      { name: 'GD&T', level: 82 },
    ],
  },
  {
    group: 'Coating & Deposition',
    icon: 'layers',
    skills: [
      { name: 'HiPIMS', level: 93 },
      { name: 'Magnetron Sputtering', level: 92 },
      { name: 'DLC Thin Films', level: 90 },
      { name: 'Cemecon HiPIMS Machine', level: 88 },
    ],
  },
  {
    group: 'Programming & ML',
    icon: 'code',
    skills: [
      { name: 'Python', level: 88 },
      { name: 'MATLAB · Simulink', level: 86 },
      { name: 'SVM · PyCaret AutoML', level: 84 },
      { name: 'Signal Processing · Wavelets', level: 87 },
    ],
  },
  {
    group: 'DOE & Statistics',
    icon: 'bar-chart',
    skills: [
      { name: 'Minitab', level: 88 },
      { name: 'Design Expert', level: 88 },
      { name: 'ANOVA · RSM', level: 90 },
      { name: 'Power BI', level: 78 },
    ],
  },
  {
    group: 'Characterisation',
    icon: 'microscope',
    skills: [
      { name: 'SEM / EDX', level: 90 },
      { name: 'Raman Spectroscopy', level: 88 },
      { name: 'XRD · Interferometry', level: 84 },
      { name: 'Scratch Test · Tribometry', level: 90 },
    ],
  },
];

export const radarAxes = [
  { axis: 'Simulation & CAE', value: 95 },
  { axis: 'CAD & Design', value: 88 },
  { axis: 'Coatings & Surface Eng.', value: 92 },
  { axis: 'Programming & ML', value: 85 },
  { axis: 'Manufacturing', value: 88 },
  { axis: 'Research & DOE', value: 93 },
];

export const certifications = [
  { title: 'Diploma in Metal Cutting Technology', org: 'Sandvik Coromant', icon: 'award' },
  { title: 'Six Sigma: Green Belt', org: 'IIBA', icon: 'badge-check' },
  { title: 'Master COMSOL Multiphysics® Simulation', org: 'Udemy', icon: 'box' },
  { title: 'Power BI Essential Training', org: 'NASBA', icon: 'bar-chart' },
  { title: 'Geometric Dimensioning & Tolerancing', org: 'LinkedIn Learning', icon: 'ruler' },
  { title: 'Simulink Onramp', org: 'MathWorks', icon: 'activity' },
  { title: 'Introduction to Python', org: 'GUVI', icon: 'code' },
];

export const equations = [
  '∇×B = μ₀J',
  'F = q(E + v×B)',
  'σ = Eε',
  '∇·D = ρ',
  'Kt·σnom',
  '∂T/∂t = α∇²T',
  'Δσ = σmax − σmin',
  'Ra = 1/l ∫|z(x)|dx',
  'ω = √(k/m)',
  'τ = μN',
];

export const seo = {
  // Update this if the site's primary domain changes
  // (GitHub Pages: https://vijayathithanm.github.io/Vijayathithanm)
  siteUrl: 'https://vijayathithanportfolio.vercel.app',
  title: 'Vijayathithan Mathiyazhagan — R&D Engineer · Simulation Scientist',
  description:
    'Ph.D. (IIT Madras) mechanical engineer specialising in HiPIMS PVD coatings, indigenous magnetron development, COMSOL multiphysics simulation, VMC machine design, and AI-driven tool prognostics.',
  keywords: [
    'Mechanical Engineer',
    'R&D Engineer',
    'Simulation Scientist',
    'COMSOL Multiphysics',
    'Abaqus',
    'HiPIMS',
    'PVD Coatings',
    'Magnetron Sputtering',
    'VMC Machine Design',
    'Finite Element Analysis',
    'IIT Madras',
    'CFRP Machining',
    'Tool Condition Monitoring',
  ],
};
