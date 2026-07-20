'use client';

import { useEffect, useRef, useState } from 'react';
import { Menu, X, ChevronDown } from 'lucide-react';
import { nav } from '@/content/site';
import { scrollToHash, cn } from '@/lib/utils';

/**
 * Sticky, transparent-over-white navigation with accessible dropdown menus
 * (hover + keyboard: Enter/Space to toggle, Escape to close) and a mobile
 * drawer. The logo and all links use in-page smooth-scroll anchors.
 */
export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [openMenu, setOpenMenu] = useState<string | null>(null);
  const closeTimer = useRef<ReturnType<typeof setTimeout>>();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 24);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

  // Close menus on Escape.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setOpenMenu(null);
        setMobileOpen(false);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  const go = (e: React.MouseEvent, href: string) => {
    if (href.startsWith('#')) {
      e.preventDefault();
      scrollToHash(href);
      setMobileOpen(false);
      setOpenMenu(null);
    }
  };

  const openNow = (label: string) => {
    clearTimeout(closeTimer.current);
    setOpenMenu(label);
  };
  const closeSoon = () => {
    closeTimer.current = setTimeout(() => setOpenMenu(null), 140);
  };

  return (
    <header
      className={cn(
        'interactive fixed inset-x-0 top-0 z-50 transition-colors duration-300',
        scrolled ? 'bg-white/80 backdrop-blur-md border-b border-line' : 'bg-transparent',
      )}
    >
      <nav
        aria-label="Primary"
        className="mx-auto flex max-w-content items-center justify-between px-5 py-4 md:px-8"
      >
        {/* Logo */}
        <a
          href="#home"
          onClick={(e) => go(e, '#home')}
          className="font-display text-lg font-extrabold tracking-widest2 text-ink"
        >
          ILAIYA<span className="text-gold">RAAJA</span>
        </a>

        {/* Desktop links */}
        <ul className="hidden items-center gap-6 lg:flex">
          {nav.map((item) =>
            item.children ? (
              <li
                key={item.label}
                className="relative"
                onMouseEnter={() => openNow(item.label)}
                onMouseLeave={closeSoon}
              >
                <button
                  type="button"
                  aria-haspopup="true"
                  aria-expanded={openMenu === item.label}
                  onClick={() => setOpenMenu((m) => (m === item.label ? null : item.label))}
                  className="flex items-center gap-1 text-sm text-muted transition-colors hover:text-gold"
                >
                  {item.label}
                  <ChevronDown size={14} className="mt-0.5" aria-hidden />
                </button>
                {openMenu === item.label && (
                  <ul
                    className="absolute left-0 top-full mt-2 min-w-48 rounded-lg border border-line bg-white p-2 shadow-[0_20px_50px_-20px_rgba(0,0,0,0.25)]"
                    role="menu"
                  >
                    {item.children.map((child) => (
                      <li key={child.label} role="none">
                        <a
                          role="menuitem"
                          href={child.href}
                          onClick={(e) => go(e, child.href)}
                          className="block rounded-md px-3 py-2 text-sm text-muted transition-colors hover:bg-line/60 hover:text-gold"
                        >
                          {child.label}
                        </a>
                      </li>
                    ))}
                  </ul>
                )}
              </li>
            ) : (
              <li key={item.label}>
                <a
                  href={item.href}
                  onClick={(e) => go(e, item.href)}
                  className="text-sm text-muted transition-colors hover:text-gold"
                >
                  {item.label}
                </a>
              </li>
            ),
          )}
        </ul>

        {/* Mobile toggle */}
        <button
          type="button"
          className="lg:hidden text-ink"
          aria-label={mobileOpen ? 'Close menu' : 'Open menu'}
          aria-expanded={mobileOpen}
          onClick={() => setMobileOpen((o) => !o)}
        >
          {mobileOpen ? <X /> : <Menu />}
        </button>
      </nav>

      {/* Mobile drawer */}
      {mobileOpen && (
        <div className="interactive border-t border-line bg-white lg:hidden">
          <ul className="mx-auto max-w-content px-5 py-3">
            {nav.map((item) => (
              <li key={item.label} className="border-b border-line/70 last:border-0">
                <a
                  href={item.href}
                  onClick={(e) => go(e, item.href)}
                  className="block py-3 text-sm font-medium text-ink"
                >
                  {item.label}
                </a>
                {item.children && (
                  <ul className="pb-3 pl-4">
                    {item.children.map((child) => (
                      <li key={child.label}>
                        <a
                          href={child.href}
                          onClick={(e) => go(e, child.href)}
                          className="block py-1.5 text-sm text-muted"
                        >
                          {child.label}
                        </a>
                      </li>
                    ))}
                  </ul>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
    </header>
  );
}
