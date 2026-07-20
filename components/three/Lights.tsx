'use client';

/** Soft, bright studio lighting for the white stage. */
export default function Lights() {
  return (
    <>
      <ambientLight intensity={0.95} />
      {/* Key light, upper-front */}
      <directionalLight position={[4, 6, 6]} intensity={1.1} />
      {/* Cool fill from the opposite side */}
      <directionalLight position={[-6, 3, 2]} intensity={0.3} />
      {/* Faint gold rim to warm the charcoal ribbon */}
      <pointLight position={[0, 2, -3]} intensity={0.5} color="#C8A047" distance={16} />
    </>
  );
}
