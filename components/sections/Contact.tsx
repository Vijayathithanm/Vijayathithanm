'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Download, Linkedin, Mail, MapPin, Phone, Send } from 'lucide-react';
import { profile } from '@/content/resume';
import MagneticButton from '@/components/ui/MagneticButton';
import Reveal from '@/components/ui/Reveal';
import SectionHeading from '@/components/ui/SectionHeading';

export default function Contact() {
  const [form, setForm] = useState({ name: '', email: '', message: '' });
  const [sent, setSent] = useState(false);

  const submit = (e: React.FormEvent) => {
    e.preventDefault();
    const subject = encodeURIComponent(`Portfolio enquiry from ${form.name}`);
    const body = encodeURIComponent(`${form.message}\n\nFrom: ${form.name} (${form.email})`);
    window.location.href = `mailto:${profile.email}?subject=${subject}&body=${body}`;
    setSent(true);
    setTimeout(() => setSent(false), 4000);
  };

  const channels = [
    { icon: Mail, label: 'Email', value: profile.email, href: `mailto:${profile.email}` },
    { icon: Phone, label: 'Phone', value: profile.phone, href: `tel:${profile.phone.replace(/\s/g, '')}` },
    { icon: Linkedin, label: 'LinkedIn', value: 'linkedin.com/in/vijayathithan', href: profile.linkedin },
    { icon: MapPin, label: 'Location', value: `${profile.company}, ${profile.location}`, href: 'https://maps.google.com/?q=Bengaluru,India' },
  ];

  return (
    <section id="contact" className="relative overflow-hidden py-24 md:py-36">
      <div className="eng-grid absolute inset-0 opacity-30" />
      <div className="glow-orb bottom-[-30%] left-1/2 h-[500px] w-[800px] -translate-x-1/2 bg-accent/10" />

      <div className="relative mx-auto max-w-6xl px-5 md:px-8">
        <SectionHeading
          tag="09 · Contact"
          title="Let's engineer something together"
          intro={profile.availability}
          align="center"
        />

        <div className="grid gap-8 lg:grid-cols-2">
          {/* channels */}
          <Reveal>
            <div className="space-y-4">
              {channels.map((c) => (
                <motion.a
                  key={c.label}
                  href={c.href}
                  target={c.href.startsWith('http') ? '_blank' : undefined}
                  rel="noopener noreferrer"
                  whileHover={{ x: 6 }}
                  transition={{ type: 'spring', stiffness: 300, damping: 22 }}
                  className="glass group flex items-center gap-5 rounded-2xl p-5"
                >
                  <div className="rounded-xl border border-line bg-bg p-3.5 text-accent transition-colors group-hover:border-accent/60">
                    <c.icon size={18} strokeWidth={1.6} />
                  </div>
                  <div>
                    <div className="font-mono text-[10px] tracking-[0.25em] text-faint">
                      {c.label.toUpperCase()}
                    </div>
                    <div className="mt-0.5 text-sm font-medium text-ink transition-colors group-hover:text-accent">
                      {c.value}
                    </div>
                  </div>
                </motion.a>
              ))}
              <div className="pt-2">
                <MagneticButton href={profile.resumeFile} download className="w-full justify-center">
                  <Download size={15} /> Download Full Resume
                </MagneticButton>
              </div>
            </div>
          </Reveal>

          {/* glass form */}
          <Reveal delay={0.15}>
            <form onSubmit={submit} className="glass rounded-2xl p-7 md:p-8">
              <div className="space-y-5">
                <div>
                  <label htmlFor="name" className="mb-2 block font-mono text-[10px] tracking-[0.25em] text-faint">
                    NAME
                  </label>
                  <input
                    id="name"
                    required
                    value={form.name}
                    onChange={(e) => setForm({ ...form, name: e.target.value })}
                    className="w-full rounded-xl border border-line bg-bg/60 px-4 py-3 text-sm text-ink outline-none transition-colors placeholder:text-faint focus:border-accent/60"
                    placeholder="Your name"
                  />
                </div>
                <div>
                  <label htmlFor="email" className="mb-2 block font-mono text-[10px] tracking-[0.25em] text-faint">
                    EMAIL
                  </label>
                  <input
                    id="email"
                    type="email"
                    required
                    value={form.email}
                    onChange={(e) => setForm({ ...form, email: e.target.value })}
                    className="w-full rounded-xl border border-line bg-bg/60 px-4 py-3 text-sm text-ink outline-none transition-colors placeholder:text-faint focus:border-accent/60"
                    placeholder="you@company.com"
                  />
                </div>
                <div>
                  <label htmlFor="message" className="mb-2 block font-mono text-[10px] tracking-[0.25em] text-faint">
                    MESSAGE
                  </label>
                  <textarea
                    id="message"
                    required
                    rows={5}
                    value={form.message}
                    onChange={(e) => setForm({ ...form, message: e.target.value })}
                    className="w-full resize-none rounded-xl border border-line bg-bg/60 px-4 py-3 text-sm text-ink outline-none transition-colors placeholder:text-faint focus:border-accent/60"
                    placeholder="Tell me about the role or project…"
                  />
                </div>
                <motion.button
                  type="submit"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.97 }}
                  className="flex w-full items-center justify-center gap-2 rounded-xl bg-accent py-3.5 text-sm font-medium text-bg transition-shadow hover:shadow-[0_0_32px_rgb(var(--accent)/0.4)]"
                >
                  <motion.span
                    animate={sent ? { x: 60, opacity: 0 } : { x: 0, opacity: 1 }}
                    className="flex items-center gap-2"
                  >
                    <Send size={15} /> {sent ? 'Opening mail client…' : 'Send Message'}
                  </motion.span>
                </motion.button>
              </div>
            </form>
          </Reveal>
        </div>
      </div>
    </section>
  );
}
