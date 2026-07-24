'use client';

import { Youtube, Music2 } from 'lucide-react';
import { footer } from '@/content/site';
import { scrollToHash } from '@/lib/utils';

/** Dark streaming-style footer. */
export default function Footer() {
  const onLink = (e: React.MouseEvent, href: string) => {
    if (href.startsWith('#')) {
      e.preventDefault();
      scrollToHash(href);
    }
  };

  return (
    <footer id="footer" className="relative border-t border-line bg-panel" aria-label="Footer">
      <div className="mx-auto max-w-content px-5 py-14 md:px-8">
        <div className="mb-10 flex flex-wrap items-center gap-4">
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

        <div className="grid gap-10 text-sm md:grid-cols-4">
          <div>
            <h3 className="flex items-center gap-2 font-display text-xl font-semibold tracking-wide text-ink">
              <Music2 size={16} className="text-gold" aria-hidden /> {footer.address.name}
            </h3>
            <address className="mt-3 space-y-1 not-italic leading-relaxed text-faint">
              {footer.address.lines.map((line) => (
                <p key={line}>{line}</p>
              ))}
              <p className="pt-2">
                <a href={`mailto:${footer.address.email}`} className="text-muted hover:text-gold">
                  {footer.address.email}
                </a>
              </p>
            </address>
          </div>

          <nav aria-label="Quick links">
            <h4 className="text-xs font-semibold uppercase tracking-widest2 text-faint">Quick Links</h4>
            <ul className="mt-3 space-y-2">
              {footer.quickLinks.map((l) => (
                <li key={l.label}>
                  <a href={l.href} onClick={(e) => onLink(e, l.href)} className="text-muted transition-colors hover:text-gold">
                    {l.label}
                  </a>
                </li>
              ))}
            </ul>
          </nav>

          <nav aria-label="Legal">
            <h4 className="text-xs font-semibold uppercase tracking-widest2 text-faint">Legal</h4>
            <ul className="mt-3 space-y-2">
              {footer.legal.map((l) => (
                <li key={l.label}>
                  <a href={l.href} className="text-muted transition-colors hover:text-gold">
                    {l.label}
                  </a>
                </li>
              ))}
            </ul>
          </nav>

          <div>
            <h4 className="text-xs font-semibold uppercase tracking-widest2 text-faint">Explore</h4>
            <ul className="mt-3 space-y-2">
              <li><a href="#compositions" onClick={(e) => onLink(e, '#compositions')} className="text-muted hover:text-gold">Compositions</a></li>
              <li><a href="#concerts" onClick={(e) => onLink(e, '#concerts')} className="text-muted hover:text-gold">Concerts</a></li>
              <li><a href="#facets" onClick={(e) => onLink(e, '#facets')} className="text-muted hover:text-gold">Facets</a></li>
            </ul>
          </div>
        </div>

        <p className="mt-12 border-t border-line pt-6 text-xs text-faint">{footer.copyright}</p>
      </div>
    </footer>
  );
}
