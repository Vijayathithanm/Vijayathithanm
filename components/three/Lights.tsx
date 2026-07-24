'use client';

/** Soft, gallery-style studio lighting — everything reads on white. */
export default function Lights() {
  return (
    <>
      <ambientLight intensity={0.9} />
      {/* Key light, upper-front */}
      <directionalLight
        position={[4, 6, 6]}
        intensity={1.15}
        castShadow
        shadow-mapSize={[1024, 1024]}
        shadow-bias={-0.0004}
      >
        <orthographicCamera attach="shadow-camera" args={[-8, 8, 8, -8, 0.1, 30]} />
      </directionalLight>
      {/* Cool fill from the opposite side to keep shadows open */}
      <directionalLight position={[-6, 3, 2]} intensity={0.35} />
      {/* Faint warm rim to hint at the gold accent */}
      <pointLight position={[0, 2, -4]} intensity={0.4} color="#C8A047" distance={18} />
    </>
  );
}
