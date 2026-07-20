/**
 * lib/store.ts — a tiny module-level store shared between the DOM and the 3D
 * scene. It is intentionally NOT React state: the values change every frame,
 * so the Canvas reads them directly inside `useFrame` (no re-renders), while a
 * single controller component writes to them from scroll / pointer listeners.
 */

export type SceneState = {
  /** Whole-page scroll progress, 0 (top) → 1 (bottom). */
  progress: number;
  /** Normalized pointer position, -1 → 1 on each axis (0,0 = centre). */
  pointerX: number;
  pointerY: number;
  /** True while the tab is visible — heavy work pauses when false. */
  active: boolean;
  /** Honour the OS "reduce motion" preference across DOM + 3D. */
  reducedMotion: boolean;
  /** Audio amplitude 0 → 1 driven by the analyser (0 = paused / silent). */
  audioLevel: number;
  /** Whether the maestro's track is currently "playing". */
  playing: boolean;
};

export const scene: SceneState = {
  progress: 0,
  pointerX: 0,
  pointerY: 0,
  active: true,
  reducedMotion: false,
  audioLevel: 0,
  playing: false,
};

/** Smoothly interpolate `current` toward `target` (frame-rate aware). */
export function damp(current: number, target: number, lambda: number, dt: number) {
  return current + (target - current) * (1 - Math.exp(-lambda * dt));
}
