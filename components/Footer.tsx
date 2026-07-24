'use client';

import { Youtube } from 'lucide-react';
import { footer } from '@/content/site';
import { scrollToHash } from '@/lib/utils';

/** Clean footer on white with a thin top border. */
export default function Footer() {
  const onLink = (e: React.MouseEvent, href: string) => {
    if (href.startsWith('#')) {
      e.preventDefault();
      scrollToHash(href);
    }
  };

  return (
    <footer
      id="footer"
      className="interactive relative border-t border-line bg-white/90 backdrop-blur-sm"
      aria-label="Footer"
    >
      <div className="mx-auto max-w-content px-5 py-16 md:px-8">
        <div className="grid gap-10 md:grid-cols-4">
          {/* Address */}
          <div>
            <h3 className="font-display text-lg font-bold text-ink">{footer.address.name}</h3>
            <address className="mt-4 space-y-1 text-sm not-italic leading-relaxed text-muted">
              {footer.address.lines.map((line) => (
                <p key={line}>{line}</p>
              ))}
              <p className="pt-2">
                <a
                  href={`mailto:${footer.address.email}`}
                  className="text-ink underline-offset-4 hover:text-gold hover:underline"
                >
                  {footer.address.email}
                </a>
              </p>
            </address>
          </div>

          {/* Quick links */}
          <nav aria-label="Quick links">
            <h4 className="text-xs font-semibold uppercase tracking-widest2 text-faint">Quick Links</h4>
            <ul className="mt-4 space-y-2 text-sm">
              {footer.quickLinks.map((l) => (
                <li key={l.label}>
                  <a
                    href={l.href}
                    onClick={(e) => onLink(e, l.href)}
                    className="text-muted transition-colors hover:text-gold"
                  >
                    {l.label}
                  </a>
                </li>
              ))}
            </ul>
          </nav>

          {/* Legal */}
          <nav aria-label="Legal">
            <h4 className="text-xs font-semibold uppercase tracking-widest2 text-faint">Legal</h4>
            <ul className="mt-4 space-y-2 text-sm">
              {footer.legal.map((l) => (
                <li key={l.label}>
                  <a href={l.href} className="text-muted transition-colors hover:text-gold">
                    {l.label}
                  </a>
                </li>
              ))}
            </ul>
          </nav>

          {/* Connect */}
          <div>
            <h4 className="text-xs font-semibold uppercase tracking-widest2 text-faint">Connect socially</h4>
            <div className="mt-4 flex gap-3">
              {footer.social.map((s) => (
                <a
                  key={s.label}
                  href={s.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={s.label}
                  className="flex h-10 w-10 items-center justify-center rounded-full border border-line text-ink transition-colors hover:border-gold hover:text-gold"
                >
                  <Youtube size={18} />
                </a>
              ))}
            </div>
          </div>
        </div>

        <div className="mt-14 border-t border-line pt-6 text-center text-xs text-faint">
          {footer.copyright}
        </div>
      </div>
    </footer>
  );
}
