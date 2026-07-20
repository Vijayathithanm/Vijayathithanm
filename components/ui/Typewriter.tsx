'use client';

import { useEffect, useState } from 'react';

type Props = { words: string[]; className?: string };

/** Cycling typewriter effect. */
export default function Typewriter({ words, className }: Props) {
  const [wordIndex, setWordIndex] = useState(0);
  const [text, setText] = useState('');
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const word = words[wordIndex % words.length];
    const speed = deleting ? 40 : 85;

    const timer = setTimeout(() => {
      if (!deleting) {
        const next = word.slice(0, text.length + 1);
        setText(next);
        if (next === word) setTimeout(() => setDeleting(true), 1800);
      } else {
        const next = word.slice(0, text.length - 1);
        setText(next);
        if (next === '') {
          setDeleting(false);
          setWordIndex((i) => (i + 1) % words.length);
        }
      }
    }, speed);

    return () => clearTimeout(timer);
  }, [text, deleting, wordIndex, words]);

  return (
    <span className={className}>
      {text}
      <span className="ml-0.5 inline-block w-[2px] animate-pulse-soft bg-accent align-middle" style={{ height: '1em' }} />
    </span>
  );
}
