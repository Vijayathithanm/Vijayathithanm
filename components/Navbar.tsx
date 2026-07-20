'use client';

import { useEffect, useRef, useState } from 'react';
import { Menu, X, ChevronDown, Search, Bell } from 'lucide-react';
import { nav } from '@/content/site';
import { scrollToHash, cn } from '@/lib/utils';

/**
 * Streaming-style top bar: transparent over the billboard, fading to solid
 * black as you scroll. Accessible dropdowns (hover + keyboard, Escape closes)
 * and a mobile drawer.
 */
export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [openMenu, setOpenMenu] = useState<string | null>(null);
  const closeTimer = useRef<ReturnType<typeof setTimeout>>();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);

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
        'fixed inset-x-0 top-0 z-50 transition-colors duration-500',
        scrolled ? 'bg-ink/95 backdrop-blur-sm shadow-lg shadow-black/40' : 'bg-gradient-to-b from-black/80 to-transparent',
      )}
    >
      <nav aria-label="Primary" className="mx-auto flex max-w-content items-center gap-6 px-4 py-3.5 md:px-8">
        {/* Logo */}
        <a
          href="#home"
          onClick={(e) => go(e, '#home')}
          className="font-display text-2xl tracking-wide text-red md:text-3xl"
        >
          ILAIYARAAJA
        </a>

        {/* Desktop links */}
        <ul className="ml-4 hidden items-center gap-5 lg:flex">
          {nav.map((item) =>
            item.children ? (
              <li key={item.label} className="relative" onMouseEnter={() => openNow(item.label)} onMouseLeave={closeSoon}>
                <button
                  type="button"
                  aria-haspopup="true"
                  aria-expanded={openMenu === item.label}
                  onClick={() => setOpenMenu((m) => (m === item.label ? null : item.label))}
                  className="flex items-center gap-1 text-sm text-muted transition-colors hover:text-white"
                >
                  {item.label}
                  <ChevronDown size={13} className="mt-0.5" aria-hidden />
                </button>
                {openMenu === item.label && (
                  <ul className="absolute left-0 top-full mt-2 min-w-48 rounded-md border border-line bg-black2/95 p-2 backdrop-blur" role="menu">
                    {item.children.map((child) => (
                      <li key={child.label} role="none">
                        <a
                          role="menuitem"
                          href={child.href}
                          onClick={(e) => go(e, child.href)}
                          className="block rounded px-3 py-2 text-sm text-muted transition-colors hover:bg-line hover:text-white"
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
                  className="text-sm text-muted transition-colors hover:text-white"
                >
                  {item.label}
                </a>
              </li>
            ),
          )}
        </ul>

        {/* Right cluster */}
        <div className="ml-auto flex items-center gap-4 text-white">
          <button aria-label="Search" className="hidden text-white/90 transition-colors hover:text-red sm:block">
            <Search size={18} />
          </button>
          <button aria-label="Notifications" className="hidden text-white/90 transition-colors hover:text-red sm:block">
            <Bell size={18} />
          </button>
          <span aria-hidden className="hidden h-7 w-7 rounded bg-gradient-to-br from-red to-gold sm:block" />
          <button
            type="button"
            className="lg:hidden"
            aria-label={mobileOpen ? 'Close menu' : 'Open menu'}
            aria-expanded={mobileOpen}
            onClick={() => setMobileOpen((o) => !o)}
          >
            {mobileOpen ? <X /> : <Menu />}
          </button>
        </div>
      </nav>

      {/* Mobile drawer */}
      {mobileOpen && (
        <div className="border-t border-line bg-black2 lg:hidden">
          <ul className="mx-auto max-w-content px-4 py-2">
            {nav.map((item) => (
              <li key={item.label} className="border-b border-line/70 last:border-0">
                <a href={item.href} onClick={(e) => go(e, item.href)} className="block py-3 text-sm font-medium text-white">
                  {item.label}
                </a>
                {item.children && (
                  <ul className="pb-3 pl-4">
                    {item.children.map((child) => (
                      <li key={child.label}>
                        <a href={child.href} onClick={(e) => go(e, child.href)} className="block py-1.5 text-sm text-muted">
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
