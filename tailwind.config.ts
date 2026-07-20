import type { Config } from 'tailwindcss';

/**
 * Bright, gallery-white palette with a bold streaming-red accent:
 *   paper  → white canvas (#FFFFFF)
 *   ink    → near-black text (#141414)
 *   red    → streaming-red accent (#E50914)
 *   gold   → warm secondary accent (#C8A047)
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
        paper: '#FFFFFF',
        ink: '#141414',
        panel: '#F5F5F5',
        line: '#E6E6E6',
        muted: '#5A5A5A',
        faint: '#8A8A8A',
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
