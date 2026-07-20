'use client';

import { scene } from './store';

/**
 * lib/audio.ts — the audio engine behind the sound ribbon.
 *
 * By default it SYNTHESISES a soft, evolving ambient chord (a few detuned
 * oscillators + slow tremolo) routed through a Web Audio `AnalyserNode`, so the
 * ribbon reacts to *real* frequency data with no external asset required.
 *
 * ┌─ SWAP IN A REAL TRACK ─────────────────────────────────────────────────┐
 * │ To drive the ribbon from an actual Ilaiyaraaja recording, drop the file │
 * │ at /public/audio/theme.mp3 and replace `buildSource()` below with:      │
 * │                                                                          │
 * │   const el = new Audio('/audio/theme.mp3');                              │
 * │   el.crossOrigin = 'anonymous'; el.loop = true;                          │
 * │   const src = ctx.createMediaElementSource(el);                          │
 * │   src.connect(this.analyser); this.media = el; el.play();               │
 * │                                                                          │
 * │ Everything downstream (analyser → level → ribbon) stays the same.        │
 * └──────────────────────────────────────────────────────────────────────── ┘
 */
class AudioEngine {
  private ctx: AudioContext | null = null;
  private analyser: AnalyserNode | null = null;
  private master: GainNode | null = null;
  private oscillators: OscillatorNode[] = [];
  private lfo: OscillatorNode | null = null;
  // Backed by a concrete ArrayBuffer so the type matches getByteFrequencyData.
  private data: Uint8Array<ArrayBuffer> | null = null;

  private ensure() {
    if (this.ctx) return;
    const Ctx =
      window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    const ctx = new Ctx();
    const analyser = ctx.createAnalyser();
    analyser.fftSize = 128;
    analyser.smoothingTimeConstant = 0.82;
    const master = ctx.createGain();
    master.gain.value = 0;
    master.connect(analyser);
    analyser.connect(ctx.destination);
    this.ctx = ctx;
    this.analyser = analyser;
    this.master = master;
    this.data = new Uint8Array(new ArrayBuffer(analyser.frequencyBinCount));
  }

  /** Build the synthesised ambient pad (a gentle Am9-ish voicing). */
  private buildSource() {
    if (!this.ctx || !this.master) return;
    const ctx = this.ctx;
    // A soft, consonant chord — low volume, purely atmospheric.
    const freqs = [220, 261.63, 329.63, 392, 493.88];
    this.oscillators = freqs.map((f, i) => {
      const osc = ctx.createOscillator();
      osc.type = i % 2 === 0 ? 'sine' : 'triangle';
      osc.frequency.value = f;
      osc.detune.value = (i - 2) * 4; // slight spread for warmth
      const g = ctx.createGain();
      g.gain.value = 0.18 / freqs.length;
      osc.connect(g);
      g.connect(this.master!);
      osc.start();
      return osc;
    });
    // Slow tremolo on the master so amplitude breathes over time.
    const lfo = ctx.createOscillator();
    lfo.frequency.value = 0.15;
    const lfoGain = ctx.createGain();
    lfoGain.gain.value = 0.06;
    lfo.connect(lfoGain);
    lfoGain.connect(this.master.gain);
    lfo.start();
    this.lfo = lfo;
  }

  async play() {
    this.ensure();
    if (!this.ctx || !this.master) return;
    if (this.ctx.state === 'suspended') await this.ctx.resume();
    if (this.oscillators.length === 0) this.buildSource();
    // Fade in to a gentle, non-intrusive level.
    const now = this.ctx.currentTime;
    this.master.gain.cancelScheduledValues(now);
    this.master.gain.setValueAtTime(this.master.gain.value, now);
    this.master.gain.linearRampToValueAtTime(0.6, now + 0.6);
    scene.playing = true;
  }

  pause() {
    scene.playing = false;
    if (!this.ctx || !this.master) return;
    const now = this.ctx.currentTime;
    this.master.gain.cancelScheduledValues(now);
    this.master.gain.setValueAtTime(this.master.gain.value, now);
    this.master.gain.linearRampToValueAtTime(0, now + 0.4);
  }

  /** Average, normalised frequency energy (0 → 1). Read by the ribbon. */
  level(): number {
    if (!this.analyser || !this.data || !scene.playing) return 0;
    this.analyser.getByteFrequencyData(this.data);
    let sum = 0;
    for (let i = 0; i < this.data.length; i++) sum += this.data[i];
    return sum / (this.data.length * 255);
  }

  dispose() {
    this.oscillators.forEach((o) => {
      try {
        o.stop();
      } catch {
        /* already stopped */
      }
    });
    this.lfo?.stop();
    this.oscillators = [];
    this.lfo = null;
    this.ctx?.close();
    this.ctx = null;
  }
}

/** Singleton — shared by the play/pause control and the 3D ribbon. */
export const audioEngine = new AudioEngine();
