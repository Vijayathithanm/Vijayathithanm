import type { Config } from 'tailwindcss';

/**
 * Minimal, gallery-like palette:
 *   paper   → pure white background (#FFFFFF)
 *   ink     → dark charcoal text (#1A1A1A)
 *   gold    → the single accent, used sparingly (#C8A047)
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
        ink: '#1A1A1A',
        muted: '#5A5A5A',
        faint: '#8A8A8A',
        line: '#EAEAEA',
        gold: '#C8A047',
        'gold-soft': '#E3CFA0',
      },
      fontFamily: {
        display: ['var(--font-display)', 'Georgia', 'serif'],
        sans: ['var(--font-sans)', 'system-ui', 'sans-serif'],
      },
      letterSpacing: {
        widest2: '0.35em',
      },
      maxWidth: {
        content: '72rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.8s ease forwards',
        float: 'float 7s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
      },
    },
  },
  plugins: [],
};

export default config;
