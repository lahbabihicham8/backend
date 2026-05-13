"use client";

import { useState } from "react";
import { products } from "@/data/products";

export function CheckoutForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const offers = products[0].offers;

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    // Simulate API call
    setTimeout(() => {
      setIsSubmitting(false);
      setIsSuccess(true);
    }, 1500);
  };

  if (isSuccess) {
    return (
      <div className="rounded-3xl border border-[var(--border)] bg-[var(--trust-green)]/10 p-8 text-center shadow-sm">
        <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-[var(--trust-green)] text-white">
          <svg className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h2 className="text-2xl font-black text-[var(--trust-green)]">تم استلام طلبك بنجاح! 🎉</h2>
        <div className="mt-5 space-y-4 text-[var(--muted)]">
          <p className="text-lg font-bold text-[var(--ink)]">
            واحد من فريقنا المميز راح يتواصل معاك بأقرب وقت عشان يأكد طلبك.
          </p>
          <div className="rounded-2xl bg-white/60 p-4 text-sm leading-7">
            <p>❄️ جهّز نفسك لصيف أبرد ومشاوير أريح!</p>
            <p className="mt-2 font-semibold text-[var(--khafeefa-olive)]">
              تذكر: الدفع بيكون عند الاستلام، يعني ما تدفع ولا فلس لين يوصلك المندوب وتستلم طلبك بيدك.
            </p>
          </div>
        </div>
        <button 
          onClick={() => setIsSuccess(false)} 
          className="mt-6 rounded-full border border-[var(--trust-green)] px-8 py-3 text-sm font-bold text-[var(--trust-green)] transition-colors hover:bg-[var(--trust-green)] hover:text-white"
        >
          تقديم طلب آخر
        </button>
      </div>
    );
  }

  return (
    <div className="rounded-3xl border border-[var(--border)] bg-[var(--warm-cream)] p-6 md:p-8 shadow-sm">
      <h2 className="mb-6 text-center text-2xl font-black text-[var(--ink)]">أكمل طلبك الآن</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="mb-2 block text-sm font-bold text-[var(--ink)]">الاسم بالكامل</label>
          <input 
            type="text" 
            required 
            className="w-full rounded-xl border border-[var(--border)] px-4 py-3 focus:border-[var(--khafeefa-olive)] focus:outline-none" 
            placeholder="محمد عبدالله" 
          />
        </div>
        <div>
          <label className="mb-2 block text-sm font-bold text-[var(--ink)]">رقم الهاتف</label>
          <input 
            type="tel" 
            required 
            className="w-full text-left rounded-xl border border-[var(--border)] px-4 py-3 focus:border-[var(--khafeefa-olive)] focus:outline-none" 
            dir="ltr" 
            placeholder="9000 0000" 
          />
        </div>
        <div>
          <label className="mb-2 block text-sm font-bold text-[var(--ink)]">العنوان بالتفصيل</label>
          <textarea 
            required 
            className="w-full rounded-xl border border-[var(--border)] px-4 py-3 focus:border-[var(--khafeefa-olive)] focus:outline-none" 
            rows={3} 
            placeholder="المنطقة، القطعة، الشارع، المنزل"
          ></textarea>
        </div>
        <div>
          <label className="mb-2 block text-sm font-bold text-[var(--ink)]">اختر العرض</label>
          <select 
            id="offer-select"
            required
            className="w-full rounded-xl border border-[var(--border)] bg-white px-4 py-3 focus:border-[var(--khafeefa-olive)] focus:outline-none"
          >
            {offers.map(offer => (
              <option key={offer.id} value={offer.id}>
                {offer.label} - {offer.price} د.ك
              </option>
            ))}
          </select>
        </div>
        <button 
          type="submit" 
          disabled={isSubmitting}
          className="mt-6 w-full rounded-full bg-[var(--cta-orange)] py-4 text-center text-lg font-black text-white shadow-lg transition-transform hover:scale-[1.02] disabled:opacity-70 disabled:hover:scale-100"
        >
          {isSubmitting ? "جاري الإرسال..." : "تأكيد الطلب (الدفع عند الاستلام)"}
        </button>
      </form>
    </div>
  );
}
