import Navbar from '@/components/Navbar';
import Footer from '@/components/Footer';
import Hero from '@/components/sections/Hero';
import About from '@/components/sections/About';
import Timeline from '@/components/sections/Timeline';
import Projects from '@/components/sections/Projects';
import Simulations from '@/components/sections/Simulations';
import Vmc from '@/components/sections/Vmc';
import Publications from '@/components/sections/Publications';
import Skills from '@/components/sections/Skills';
import Certifications from '@/components/sections/Certifications';
import Contact from '@/components/sections/Contact';

export default function Home() {
  return (
    <main>
      <Navbar />
      <Hero />
      <About />
      <Timeline />
      <Projects />
      <Simulations />
      <Vmc />
      <Publications />
      <Skills />
      <Certifications />
      <Contact />
      <Footer />
    </main>
  );
}
