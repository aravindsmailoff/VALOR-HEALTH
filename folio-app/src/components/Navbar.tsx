"use client";

import Link from "next/link";
import { Sparkles } from "lucide-react";

export default function Navbar() {
  return (
    <nav className="meadow-nav">
      <div className="meadow-container meadow-nav-inner">
        <Link href="#top" className="brand-logo">
          <Sparkles size={18} className="brand-star" />
          <span>VALOR Health</span>
        </Link>

        <div className="nav-menu">
          <Link href="#what-is-twin" className="nav-link">Continuous Care</Link>
          <Link href="#twin" className="nav-link">Clinical Twin</Link>
          <Link href="#use-cases" className="nav-link">Use Cases</Link>
          <Link href="#plans" className="nav-link">Health Plans</Link>
          <Link href="#claims" className="nav-link">Cashless Claims</Link>
          <Link href="#faq" className="nav-link">FAQ</Link>
        </div>

        <Link href="#twin" className="btn-plum">
          Launch Twin Cockpit
        </Link>
      </div>
    </nav>
  );
}
