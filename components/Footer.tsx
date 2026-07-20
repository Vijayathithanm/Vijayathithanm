'use client';

import { ArrowUp, Linkedin, Mail } from 'lucide-react';
import { profile } from '@/content/resume';

export default function Footer() {
  return (
    <footer className="border-t border-line/60 py-10">
      <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-6 px-5 md:flex-row md:px-8">
        <div className="text-center md:text-left">
          <div className="font-display text-sm font-semibold">
            <span className="font-mono text-accent">[</span> {profile.name}{' '}
            <span className="font-mono text-accent">]</span>
          </div>
          <div className="mt-1 font-mono text-[11px] text-faint">
            {profile.title} · {profile.location} · © {new Date().getFullYear()}
          </div>
        </div>

        <div className="flex items-center gap-3">
          <a
            href={profile.linkedin}
            target="_blank"
            rel="noopener noreferrer"
            aria-label="LinkedIn"
            className="rounded-full border border-line p-2.5 text-muted transition-colors hover:border-accent/60 hover:text-accent"
          >
            <Linkedin size={14} />
          </a>
          <a
            href={`mailto:${profile.email}`}
            aria-label="Email"
            className="rounded-full border border-line p-2.5 text-muted transition-colors hover:border-accent/60 hover:text-accent"
          >
            <Mail size={14} />
          </a>
          <a
            href="#top"
            aria-label="Back to top"
            className="rounded-full border border-line p-2.5 text-muted transition-colors hover:border-accent/60 hover:text-accent"
          >
            <ArrowUp size={14} />
          </a>
        </div>
      </div>
    </footer>
  );
}
