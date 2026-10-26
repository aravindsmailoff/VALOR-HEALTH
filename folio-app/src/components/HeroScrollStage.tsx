"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import Link from "next/link";

const TOTAL_FRAMES = 160;
const SPLIT = 0.51;

interface BeatConfig {
  s: number;
  e: number;
  title: string;
  isH1?: boolean;
  desc: string;
  tabs?: string[];
  cta?: boolean;
}

const BEATS: BeatConfig[] = [
  {
    s: 0,
    e: 0.10,
    title: "Every health record, one desk.",
    isH1: true,
    desc: "Hospital coverage, digital twin vitals, and prescription safety, filed together and ready when you need them.",
  },
  {
    s: 0.11,
    e: 0.23,
    title: "Stop searching for paperwork.",
    desc: "Your clinical records and insurance cards sit in one secure place, so admissions and claims never start with a search through drawers.",
  },
  {
    s: 0.24,
    e: 0.37,
    title: "Continuous care. Nothing missing.",
    desc: "Each policy keeps its own real-time coverage schedule, pre-authorizations, and clinical contacts.",
    tabs: ["Inpatient Hospitalization", "Clinical Twin", "Cashless Network", "Rx Safety"],
  },
  {
    s: 0.38,
    e: 0.50,
    title: "Behind every folder, a life.",
    desc: "Keep scrolling to see where continuous predictive health protection shows up.",
  },
  {
    s: 0.51,
    e: 0.72,
    title: "It starts with a check-up.",
    desc: "Health cover turns doctor visits into routine care, keeping little milestones healthy and happy.",
  },
  {
    s: 0.73,
    e: 0.83,
    title: "Care that grows with you.",
    desc: "From routine diagnostics to specialist consultations, trusted guidance for every stage of life.",
  },
  {
    s: 0.84,
    e: 0.91,
    title: "Prescriptions without friction.",
    desc: "Cashless approvals and hassle-free pharmacy coverage when you need medication most.",
  },
  {
    s: 0.92,
    e: 1.01,
    title: "Peace of mind.",
    desc: "Live each day with confidence, knowing you and your loved ones are protected wherever life takes you.",
    cta: true,
  },
];

export default function HeroScrollStage() {
  const heroRef = useRef<HTMLElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [loadedCount, setLoadedCount] = useState(0);
  const [loadingComplete, setLoadingComplete] = useState(false);
  const [progress, setProgress] = useState(0);
  const [filmMode, setFilmMode] = useState(false);
  const [activeBeatIndex, setActiveBeatIndex] = useState(0);

  const imagesRef = useRef<HTMLImageElement[]>([]);
  const curRef = useRef<number>(0);
  const targetRef = useRef<number>(0);
  const visRef = useRef<boolean>(true);
  const animIdRef = useRef<number | null>(null);

  // Draw current frame to canvas
  const draw = useCallback((idx: number) => {
    const cv = canvasRef.current;
    if (!cv) return;
    const ctx = cv.getContext("2d");
    if (!ctx) return;

    const frameIdx = Math.max(0, Math.min(TOTAL_FRAMES - 1, idx));
    const im = imagesRef.current[frameIdx];
    if (!im || !im.complete || im.naturalWidth === 0) return;

    const cw = cv.width;
    const ch = cv.height;
    const s = Math.max(cw / im.width, ch / im.height);
    const w = im.width * s;
    const h = im.height * s;

    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = "high";
    ctx.drawImage(im, (cw - w) / 2, (ch - h) / 2, w, h);
  }, []);

  // Resize canvas with device pixel ratio
  const sizeCanvas = useCallback(() => {
    const cv = canvasRef.current;
    if (!cv) return;
    const d = Math.min(window.devicePixelRatio || 1, 2);
    cv.width = window.innerWidth * d;
    cv.height = window.innerHeight * d;
    draw(Math.round(curRef.current));
  }, [draw]);

  // Update loop for smooth frame lerping
  useEffect(() => {
    const loop = () => {
      if (visRef.current) {
        curRef.current += (targetRef.current - curRef.current) * 0.14;
        if (Math.abs(targetRef.current - curRef.current) < 0.01) {
          curRef.current = targetRef.current;
        }
        draw(Math.round(curRef.current));
      }
      animIdRef.current = requestAnimationFrame(loop);
    };

    animIdRef.current = requestAnimationFrame(loop);
    return () => {
      if (animIdRef.current) cancelAnimationFrame(animIdRef.current);
    };
  }, [draw]);

  // Scroll Handler
  const onScroll = useCallback(() => {
    const hero = heroRef.current;
    if (!hero) return;

    const r = hero.getBoundingClientRect();
    visRef.current = r.bottom > 0 && r.top < window.innerHeight;

    const scrollRange = hero.offsetHeight - window.innerHeight;
    const p = Math.max(0, Math.min(1, -r.top / (scrollRange || 1)));

    setProgress(p);
    targetRef.current = p * (TOTAL_FRAMES - 1);
    setFilmMode(p >= SPLIT);

    // Identify active beat
    const beatIdx = BEATS.findIndex((b) => p >= b.s && p < b.e);
    if (beatIdx !== -1) {
      setActiveBeatIndex(beatIdx);
    } else if (p >= 0.92) {
      setActiveBeatIndex(BEATS.length - 1);
    }
  }, []);

  // Preload all 160 frames from public/frames/frame_XXX.webp
  useEffect(() => {
    const imgs: HTMLImageElement[] = [];
    let count = 0;

    for (let i = 0; i < TOTAL_FRAMES; i++) {
      const im = new Image();
      const padIndex = String(i).padStart(3, "0");
      im.src = `/frames/frame_${padIndex}.webp`;

      im.onload = im.onerror = () => {
        count++;
        setLoadedCount(count);
        if (count === 1) {
          sizeCanvas();
        }
        if (count >= TOTAL_FRAMES) {
          setLoadingComplete(true);
          sizeCanvas();
          onScroll();
        }
      };

      imgs.push(im);
    }

    imagesRef.current = imgs;
  }, [sizeCanvas, onScroll]);

  // Event Listeners
  useEffect(() => {
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", sizeCanvas);
    sizeCanvas();
    onScroll();

    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", sizeCanvas);
    };
  }, [onScroll, sizeCanvas]);

  return (
    <header id="hero" ref={heroRef} style={{ height: "1100vh", position: "relative" }}>
      <div className="stage">
        {/* Loading banner */}
        {!loadingComplete && (
          <div className="load" id="load">
            Opening the folders…
          </div>
        )}

        {/* Scroll-Driven Photo Canvas */}
        <canvas
          id="cv"
          ref={canvasRef}
          role="img"
          aria-label="Scroll-driven film: insurance folders on a desk, then scenes of health and peace of mind"
        />

        {/* Dynamic Editorial Scrim */}
        <div className={`scrim ${filmMode ? "film-mode" : ""}`} id="scrim" />

        {/* Story Beats */}
        {BEATS.map((beat, i) => {
          const isActive = activeBeatIndex === i;
          return (
            <div key={i} className={`beat ${isActive ? "on" : ""}`}>
              {beat.isH1 ? <h1>{beat.title}</h1> : <h2>{beat.title}</h2>}
              <p>{beat.desc}</p>

              {beat.tabs && (
                <div className="tabs">
                  {beat.tabs.map((tab) => (
                    <span key={tab}>{tab}</span>
                  ))}
                </div>
              )}

              {beat.cta && (
                <div style={{ display: "flex", gap: "14px", flexWrap: "wrap", marginTop: "24px" }}>
                  <Link href="#twin" className="btn">
                    Open Digital Twin Simulator
                  </Link>
                </div>
              )}
            </div>
          );
        })}

        {/* Hint to move in */}
        <div
          className="hint"
          id="hint"
          style={{ opacity: progress > 0.02 ? 0 : 1 }}
        >
          Scroll to move in
        </div>

        {/* Progress Bar */}
        <div className="bar">
          <i id="prog" style={{ width: `${(progress * 100).toFixed(1)}%` }} />
        </div>
      </div>
    </header>
  );
}
