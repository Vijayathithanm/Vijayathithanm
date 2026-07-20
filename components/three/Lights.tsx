'use client';

/** Moody, cinematic lighting for the dark hero stage. */
export default function Lights() {
  return (
    <>
      <ambientLight intensity={0.35} />
      {/* Key light, upper-front */}
      <directionalLight position={[4, 6, 6]} intensity={0.9} />
      {/* Cool fill from the side */}
      <directionalLight position={[-6, 2, 2]} intensity={0.25} color="#8aa0ff" />
      {/* Warm gold rim behind the ribbon */}
      <pointLight position={[0, 1.5, -3]} intensity={1.1} color="#C8A047" distance={16} />
      {/* Red kicker for the streaming glow */}
      <pointLight position={[3, -1, 2]} intensity={0.7} color="#E50914" distance={14} />
    </>
  );
}
