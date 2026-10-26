"use client";

import Link from "next/link";
import { Sparkles } from "lucide-react";

export default function HeroMeadow() {
  return (
    <section className="meadow-container" id="top">
      <div className="hero-card">
        {/* Star Badge */}
        <div className="hero-star-badge">
          <Sparkles size={28} />
        </div>

        {/* Headline */}
        <h1 className="hero-title">
          Health in<br />Full Bloom
        </h1>

        {/* Subtitle */}
        <p className="hero-sub">
          A continuous health plan that quietly protects while you live.
          Spend with zero cashless friction, safeguard with an intelligent digital twin.
        </p>

        {/* CTA Button */}
        <div>
          <Link href="#simulator" className="btn-plum" style={{ padding: "14px 32px", fontSize: "15px" }}>
            See it bloom
          </Link>
        </div>

        {/* Floral Meadow Illustration with Aegis Biometric Coins */}
        <div className="meadow-floral-stage">
          <svg
            viewBox="0 0 1100 280"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            style={{ width: "100%", height: "100%", overflow: "visible" }}
          >
            <defs>
              <linearGradient id="roseCoinGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#fce7ee" />
                <stop offset="50%" stopColor="#f29bbd" />
                <stop offset="100%" stopColor="#b84f7b" />
              </linearGradient>
              <linearGradient id="rimGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stopColor="#e885aa" />
                <stop offset="100%" stopColor="#7a254c" />
              </linearGradient>
              <radialGradient id="meadowFog" cx="50%" cy="100%" r="60%">
                <stop offset="0%" stopColor="#fadfe6" stopOpacity="0.8" />
                <stop offset="100%" stopColor="#fadfe6" stopOpacity="0" />
              </radialGradient>
            </defs>

            {/* Ambient ground mist */}
            <ellipse cx="550" cy="270" rx="500" ry="100" fill="url(#meadowFog)" />

            {/* Left Biometric Token Coin */}
            <g transform="translate(320, 90)">
              {/* Coin side/rim */}
              <ellipse cx="65" cy="90" rx="58" ry="85" fill="url(#rimGrad)" />
              {/* Coin face */}
              <ellipse cx="60" cy="85" rx="55" ry="80" fill="url(#roseCoinGrad)" />
              <ellipse cx="60" cy="85" rx="45" ry="68" fill="none" stroke="rgba(255,255,255,0.6)" strokeWidth="2" />
              {/* Heart/Twin Emblem */}
              <path
                d="M 60 74 C 54 62 44 64 42 74 C 40 84 60 98 60 98 C 60 98 80 84 78 74 C 76 64 66 62 60 74 Z"
                fill="rgba(255,255,255,0.85)"
              />
            </g>

            {/* Right Biometric Token Coin */}
            <g transform="translate(730, 60)">
              <ellipse cx="65" cy="90" rx="52" ry="80" fill="url(#rimGrad)" />
              <ellipse cx="60" cy="85" rx="49" ry="75" fill="url(#roseCoinGrad)" />
              <ellipse cx="60" cy="85" rx="40" ry="63" fill="none" stroke="rgba(255,255,255,0.6)" strokeWidth="2" />
              <circle cx="60" cy="85" r="14" fill="rgba(255,255,255,0.75)" />
            </g>

            {/* Rose Meadow Dense Floral Shrubbery (Layer 1 - deep plum-rose) */}
            <path
              d="M 0 280 Q 80 180 160 210 Q 240 160 340 190 Q 420 150 520 180 Q 620 150 720 190 Q 820 160 920 190 Q 1000 170 1100 280 Z"
              fill="#8e3b5e"
              opacity="0.9"
            />

            {/* Rose Meadow Dense Floral Shrubbery (Layer 2 - mid berry pink) */}
            <path
              d="M 0 280 Q 70 200 150 220 Q 260 180 360 210 Q 470 175 580 205 Q 690 170 800 205 Q 910 180 1020 220 Q 1080 210 1100 280 Z"
              fill="#b94e7c"
            />

            {/* Dotted texture resembling flower blossom clusters */}
            <g fill="#f2a6c4" opacity="0.8">
              {[
                [40, 240, 6], [70, 220, 8], [110, 250, 7], [140, 215, 9], [180, 230, 8], [220, 205, 10],
                [260, 235, 7], [300, 210, 9], [350, 225, 8], [390, 195, 11], [430, 220, 9], [470, 190, 10],
                [510, 215, 8], [550, 195, 11], [590, 220, 8], [630, 190, 10], [670, 215, 9], [710, 200, 10],
                [760, 230, 8], [800, 205, 10], [850, 220, 8], [890, 195, 11], [940, 225, 8], [980, 210, 9],
                [1030, 235, 7], [1070, 250, 8]
              ].map(([cx, cy, r], idx) => (
                <circle key={idx} cx={cx} cy={cy} r={r} />
              ))}
            </g>

            {/* High-detail blossom accents (Layer 3 - light blush blossom caps) */}
            <g fill="#fdeaf1">
              {[
                [85, 230, 4], [130, 210, 5], [195, 220, 4], [245, 195, 5], [290, 225, 4],
                [335, 205, 5], [410, 190, 5], [455, 205, 4], [520, 185, 5], [575, 200, 4],
                [645, 185, 5], [725, 195, 4], [785, 200, 5], [835, 215, 4], [905, 190, 5],
                [965, 215, 4], [1025, 225, 5]
              ].map(([cx, cy, r], idx) => (
                <circle key={idx} cx={cx} cy={cy} r={r} />
              ))}
            </g>
          </svg>
        </div>
      </div>
    </section>
  );
}
