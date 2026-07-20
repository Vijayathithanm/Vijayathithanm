import type { Config } from 'tailwindcss';

/**
 * Cinematic, streaming-style dark palette:
 *   ink    → near-black canvas (#141414)
 *   red    → hot streaming-red accent (#E50914)
 *   gold   → warm secondary accent that ties back to the maestro (#C8A047)
 */
const config: Config = {
  content: [
    './app/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './content/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        ink: '#141414',
        black2: '#0b0b0b',
        panel: '#1c1c1c',
        line: '#2b2b2b',
        white: '#ffffff',
        muted: '#b3b3b3',
        faint: '#7a7a7a',
        red: '#E50914',
        'red-dark': '#b0060f',
        gold: '#C8A047',
      },
      fontFamily: {
        display: ['var(--font-display)', 'Arial Narrow', 'sans-serif'],
        sans: ['var(--font-sans)', 'system-ui', 'sans-serif'],
      },
      letterSpacing: {
        widest2: '0.3em',
      },
      maxWidth: {
        content: '90rem',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
      animation: {
        'fade-in': 'fadeIn 0.7s ease forwards',
      },
    },
  },
  plugins: [],
};

export default config;
