import Link from "next/link";
import { Logo } from "./logo";

const links = [
  { href: "/", label: "الرئيسية" },
  { href: "#offers", label: "المنتج" },
  { href: "#contact", label: "تواصل معانا" }
];

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-20 border-b border-[var(--border)] bg-[var(--warm-cream)]/90 backdrop-blur">
      <div className="container flex min-h-20 items-center justify-between gap-6">
        <Link href="/" aria-label="الصفحة الرئيسية">
          <Logo />
        </Link>
        <nav className="hidden items-center gap-6 text-sm font-semibold text-[var(--muted)] md:flex">
          {links.map((link) => (
            <a key={link.label} href={link.href} className="hover:text-[var(--ink)]">
              {link.label}
            </a>
          ))}
        </nav>
        <a
          href="#offers"
          className="rounded-full bg-[var(--cta-orange)] px-5 py-3 text-sm font-bold text-white shadow-sm"
        >
          اطلب الآن
        </a>
      </div>
    </header>
  );
}
