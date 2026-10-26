"use client";

import { ReactLenis } from "lenis/react";

interface SmoothScrollProps {
  children: React.ReactNode;
}

export default function SmoothScroll({ children }: SmoothScrollProps) {
  return (
    <ReactLenis
      root
      options={{
        lerp: 0.08,
        duration: 1.2,
        smoothWheel: true,
        wheelMultiplier: 1,
        touchMultiplier: 1.8,
        infinite: false,
      }}
    >
      {children}
    </ReactLenis>
  );
}
