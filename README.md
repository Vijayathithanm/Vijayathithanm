# 👋 Hi, I'm Vijayathithan — this is my engineering portfolio

A premium, dark-themed, fully animated portfolio for a Mechanical R&D Engineer /
Simulation Scientist — built with Next.js, TypeScript, Tailwind CSS, Framer
Motion, GSAP, Three.js (React Three Fiber) and Lenis smooth scroll.

**Live sections:** Hero (3D CAD-wireframe gears + particles + floating
equations) · About & animated stats · Professional timeline · Projects with
filtering & animated SVG schematics · COMSOL simulation showcase · VMC flagship
programme · Publications · Skills (radar chart + progress bars) ·
Certifications · Contact (glassmorphism form) · Resume download.

---

## Quick start

```bash
npm install
npm run dev        # http://localhost:3000
npm run build      # static export → ./out
```

The site is a **fully static export** (`output: 'export'`) — no server
required. The `out/` folder can be hosted anywhere.

## Editing content — no code required

**All content lives in [`content/resume.ts`](content/resume.ts).**
Profile, stats, experience, education, projects, simulations, VMC phases,
publications, skills, certifications and SEO strings are plain typed objects.
Edit that one file and rebuild — no component ever hardcodes content.

To update the downloadable resume, replace
`public/resume/Vijayathithan_Mathiyazhagan_CV.docx` (a PDF works too — update
`profile.resumeFile` in `content/resume.ts` to match the new filename).

### Adding your photo

The About/Hero currently use a monogram + 3D scene. To add a portrait, drop
`public/images/profile.jpg` into the repo and reference it from any section
(e.g. add an `<Image>` in `components/sections/About.tsx`).

## Architecture

```
app/                    Next.js App Router
  layout.tsx            Fonts, metadata, Open Graph, JSON-LD Person schema
  page.tsx              Section composition
  globals.css           Design tokens (dark/light), grid & blueprint utilities
  robots.ts sitemap.ts  SEO (static-export compatible)
content/
  resume.ts             ★ Single source of truth for every word on the site
components/
  providers/            Lenis smooth scroll + GSAP ScrollTrigger wiring
  three/HeroScene.tsx   R3F scene — procedural wireframe gears + particle field
  sections/             Hero, About, Timeline, Projects, Simulations, Vmc,
                        Publications, Skills, Certifications, Contact
  ui/                   Reusable animation primitives:
                        Reveal, SectionHeading (split-text), MagneticButton,
                        CountUp, Typewriter, TiltCard, RadarChart,
                        ProjectVisual (custom animated SVG schematics)
lib/utils.ts            Helpers
public/resume/          Downloadable CV
vercel.json             Deployment + caching + security headers
```

## Design system

- **Theme** — dark by default (deep engineering navy), light mode via the
  navbar toggle, persisted in `localStorage`, no flash-of-wrong-theme
  (inline script in `<head>`).
- **Tokens** — all colors are CSS variables (`--bg`, `--ink`, `--accent`, …)
  consumed by Tailwind, so retheming is a 10-line change in `globals.css`.
- **Type** — Space Grotesk (display) · Inter (body) · JetBrains Mono
  (technical labels), self-hosted via `next/font`.
- **Signature details** — blueprint corner-tick cards, engineering grid
  backgrounds, scan-line hovers, floating governing equations, magnetic
  buttons, cursor glow, custom animated SVG schematics per project (magnetron
  field lines, VMC kinematics, DLC layer stack, CFRP drilling, AE signal,
  robot path).

## Performance & accessibility

- Static export, code-split; the Three.js scene is `dynamic(..., {ssr:false})`
  and lazy-loaded — first-load JS for the page is ~153 kB gzipped.
- GPU-only animations (transforms/opacity), `requestAnimationFrame` batching
  for pointer effects, `prefers-reduced-motion` respected globally (Lenis and
  CSS animations disabled).
- Semantic landmarks, labelled controls, `aria-expanded` on disclosure
  buttons, keyboard-reachable interactive elements, WCAG-conscious contrast in
  both themes.
- SEO: full metadata, Open Graph, Twitter cards, `robots.txt`, `sitemap.xml`,
  and a JSON-LD `Person` schema generated from `content/resume.ts`.

## Deployment

### Vercel (recommended)

1. Push this repository to GitHub.
2. [vercel.com/new](https://vercel.com/new) → import the repo.
3. Framework preset: **Next.js** — no other settings needed
   (`vercel.json` already configures output, caching and security headers).
4. After the first deploy, set `seo.siteUrl` in `content/resume.ts` to your
   final domain and push again.

### Any static host (GitHub Pages, Netlify, S3, nginx…)

```bash
npm run build   # produces ./out
```

Upload `out/` as-is. For GitHub Pages under a sub-path, set
`basePath`/`assetPrefix` in `next.config.mjs` first.

### Contact form

The form opens the visitor's mail client pre-filled (zero backend, works on
static hosting). To capture submissions instead, point the form at a
[Formspree](https://formspree.io) endpoint in
`components/sections/Contact.tsx` — one URL change.

### Analytics

Add your snippet (e.g. Vercel Analytics, Plausible, GA4) in
`app/layout.tsx` — the layout is the single injection point.

## Tech

Next.js 14 · React 18 · TypeScript · Tailwind CSS · Framer Motion · GSAP +
ScrollTrigger · Three.js + React Three Fiber · Lenis · Lucide icons.
