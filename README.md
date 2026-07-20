# Ilaiyaraaja — Interactive 3D Experience

A single-page, gallery-minimal tribute to the maestro **Ilaiyaraaja**, built
with **React Three Fiber** + **@react-three/drei** for a persistent white 3D
stage and **Tailwind CSS** for the 2D overlay. Pure-white background, charcoal
ink, one restrained gold accent.

---

## Run it

```bash
npm install
npm run dev      # http://localhost:3000
npm run build    # static export → ./out  (no server needed)
```

The site is a **static export** (`output: 'export'`) — the `out/` folder can be
hosted on any static host.

---

## The 3D concept

- **Sound ribbon (hero centrepiece)** — one indexed plane geometry whose
  vertices undulate like a waveform via layered sine noise. Pressing **Play**
  routes a soft synthesised ambient chord through a Web Audio `AnalyserNode`,
  and the ribbon amplitude is driven by real frequency data; **Pause** settles
  it into calm procedural motion. Matte charcoal surface, thin gold edge
  highlights, a soft contact shadow, and a gentle tilt toward the cursor.
  _(To drive it from a real recording, drop `public/audio/theme.mp3` and follow
  the clearly-marked `SWAP` block in [`lib/audio.ts`](lib/audio.ts).)_
- **Vinyl gallery** — the Facets and Latest Posts appear as upright vinyl
  records on the same white stage, slowly spinning. One disc geometry +
  material is **reused** across every record; only the label textures differ.
  Hover slows the spin, scales up, lifts and glows gold; click flips a record
  to reveal its description on the back.
- **Scroll-driven camera** — as you scroll, the camera pulls back and pans so
  the ribbon recedes and the gallery rotates into frame. Biography, Latest
  News and the footer float above as 2D panels, so the white 3D stage stays
  continuous behind all content.

### Performance & accessibility

- Three.js scene is `dynamic(..., { ssr: false })` and code-split — initial
  first-load JS for the page is ~101 kB; the WebGL bundle loads after.
- Capped pixel ratio, adaptive DPR, fewer ribbon segments on mobile, one
  shared record geometry/material, and heavy work **pauses when the tab is
  hidden**.
- `prefers-reduced-motion` is respected everywhere: the ribbon freezes into a
  static curve, records stop spinning, reveal animations and Lenis smooth
  scroll are disabled.
- Keyboard-navigable nav dropdowns (`aria-expanded`, Escape to close), alt text
  on every image, focus-visible rings, and a `<noscript>` fallback so content
  is never left hidden.

---

## Architecture

```
app/
  layout.tsx          Fonts (Playfair Display + Inter), metadata, JSON-LD
  page.tsx            Renders <App/>
  globals.css         White/gold tokens, scene layering, reveal + reduced-motion
  robots.ts sitemap.ts SEO (static-export compatible)
content/
  site.ts             ★ Single source of truth for all copy & links
components/
  App.tsx             Composition; below-the-fold sections are code-split
  Providers.tsx       Lenis smooth scroll + scroll/pointer/visibility → store
  Navbar.tsx  Footer.tsx
  Scene.tsx           Lazy, client-only wrapper around the Canvas
  three/
    SceneCanvas.tsx   Canvas, lights, contact shadow, perf guards
    SoundRibbon.tsx   Audio-reactive waveform ribbon
    VinylGallery.tsx  Shared-geometry record gallery
    VinylRecord.tsx   One reusable, interactive record
    Rig.tsx  Lights.tsx
  sections/           Hero, Biography, LatestPosts, LatestNews, Facets
  ui/TiltCard.tsx     Cursor-tilt / lift card
lib/
  store.ts            Frame-loop shared state (no re-renders)
  audio.ts            Web Audio engine + AnalyserNode
  hooks.ts  utils.ts
```

## Swapping in real assets

All copy lives in [`content/site.ts`](content/site.ts). Every placeholder is
marked — search the codebase for **`SWAP`** to find each spot:

- Hero banners, post/news/facet images → drop real files in `public/images/…`
  and update the paths in `content/site.ts`.
- Biography intro film → `public/video/intro.mp4` (a `.mov` source can be added
  alongside).
- Real audio track for the ribbon → `public/audio/theme.mp3` (see `lib/audio.ts`).

## Tech

Next.js 14 · React 18 · TypeScript · React Three Fiber + drei · Three.js ·
Tailwind CSS · Framer Motion · Lenis · Lucide icons.
