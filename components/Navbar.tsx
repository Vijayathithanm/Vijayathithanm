'use client';

import { useEffect, useState } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { Download, Menu, Moon, Sun, X } from 'lucide-react';
import { profile } from '@/content/resume';

const links = [
  { href: '#about', label: 'About' },
  { href: '#experience', label: 'Experience' },
  { href: '#projects', label: 'Projects' },
  { href: '#simulations', label: 'Simulations' },
  { href: '#vmc', label: 'VMC' },
  { href: '#publications', label: 'Publications' },
  { href: '#skills', label: 'Skills' },
  { href: '#contact', label: 'Contact' },
];

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const [light, setLight] = useState(false);

  useEffect(() => {
    setLight(document.documentElement.classList.contains('light'));
    const onScroll = () => setScrolled(window.scrollY > 40);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  const toggleTheme = () => {
    const next = !light;
    setLight(next);
    document.documentElement.classList.toggle('light', next);
    try {
      localStorage.theme = next ? 'light' : 'dark';
    } catch {}
  };

  return (
    <>
      <motion.header
        initial={{ y: -80, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.7, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
        className={`fixed inset-x-0 top-0 z-50 transition-all duration-500 ${
          scrolled ? 'glass py-3' : 'bg-transparent py-5'
        }`}
      >
        <nav className="mx-auto flex max-w-7xl items-center justify-between px-5 md:px-8">
          <a href="#top" className="font-display text-lg font-semibold tracking-tight">
            <span className="font-mono text-accent">[</span> {profile.initials}{' '}
            <span className="font-mono text-accent">]</span>
          </a>

          <div className="hidden items-center gap-7 lg:flex">
            {links.map((l) => (
              <a
                key={l.href}
                href={l.href}
                className="group relative text-sm text-muted transition-colors hover:text-ink"
              >
                {l.label}
                <span className="absolute -bottom-1 left-0 h-px w-0 bg-accent transition-all duration-300 group-hover:w-full" />
              </a>
            ))}
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={toggleTheme}
              aria-label="Toggle theme"
              className="rounded-full border border-line p-2.5 text-muted transition-colors hover:border-accent/60 hover:text-accent"
            >
              {light ? <Moon size={15} /> : <Sun size={15} />}
            </button>
            <a
              href={profile.resumeFile}
              download
              className="hidden items-center gap-2 rounded-full bg-accent px-5 py-2.5 text-sm font-medium text-bg transition-shadow hover:shadow-[0_0_28px_rgb(var(--accent)/0.4)] sm:flex"
            >
              <Download size={14} /> Resume
            </a>
            <button
              onClick={() => setOpen(true)}
              aria-label="Open menu"
              className="rounded-full border border-line p-2.5 text-muted lg:hidden"
            >
              <Menu size={16} />
            </button>
          </div>
        </nav>
      </motion.header>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[60] flex flex-col bg-bg/95 backdrop-blur-xl lg:hidden"
          >
            <div className="flex justify-end p-5">
              <button
                onClick={() => setOpen(false)}
                aria-label="Close menu"
                className="rounded-full border border-line p-2.5 text-muted"
              >
                <X size={16} />
              </button>
            </div>
            <div className="flex flex-1 flex-col items-center justify-center gap-6">
              {links.map((l, i) => (
                <motion.a
                  key={l.href}
                  href={l.href}
                  onClick={() => setOpen(false)}
                  initial={{ opacity: 0, y: 16 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.05 * i }}
                  className="font-display text-2xl font-medium text-ink"
                >
                  {l.label}
                </motion.a>
              ))}
              <a
                href={profile.resumeFile}
                download
                className="mt-4 flex items-center gap-2 rounded-full bg-accent px-6 py-3 text-sm font-medium text-bg"
              >
                <Download size={14} /> Download Resume
              </a>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
