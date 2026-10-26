import Link from "next/link";

export default function Footer() {
  return (
    <footer>
      <div className="footer-inner">
        <div>© 2026 VALOR Health Insurance. Continuous coverage powered by AegisTwin.</div>
        <div>
          <Link href="#hero">Top</Link>
          <Link href="#twin">Digital Twin</Link>
          <Link href="#claims">Cashless Claims</Link>
        </div>
      </div>
    </footer>
  );
}
