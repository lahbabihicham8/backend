import Link from "next/link";
import { Logo } from "./logo";

export function SiteFooter() {
  return (
    <footer className="border-t border-[var(--border)] bg-white/50 py-10">
      <div className="container grid gap-8 md:grid-cols-[1.4fr_1fr_1fr]">
        <div className="space-y-4">
          <Logo />
          <p className="max-w-md text-sm leading-7 text-[var(--muted)]">
            خفيفة علامة كويتية لمنتجات الراحة العملية في الحر والمشاوير اليومية.
            الدفع عند الاستلام داخل الكويت.
          </p>
        </div>
        <div className="space-y-3 text-sm">
          <h2 className="font-bold">روابط</h2>
          <a className="block text-[var(--muted)]" href="#">
            المنتجات
          </a>
          <a className="block text-[var(--muted)]" href="#">
            سياسة التوصيل
          </a>
          <a className="block text-[var(--muted)]" href="#">
            الاستبدال والاسترجاع
          </a>
        </div>
        <div className="space-y-3 text-sm">
          <h2 className="font-bold">الثقة</h2>
          <p className="text-[var(--muted)]">دفع عند الاستلام</p>
          <p className="text-[var(--muted)]">ضمان استرجاع ٧ أيام</p>
          <p className="text-[var(--muted)]">دعم داخل الكويت</p>
        </div>
      </div>
    </footer>
  );
}
