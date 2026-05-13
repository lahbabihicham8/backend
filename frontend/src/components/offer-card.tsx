"use client";

import { formatKwd, type Offer } from "@/data/products";

type OfferCardProps = {
  offer: Offer;
};

export function OfferCard({ offer }: OfferCardProps) {
  return (
    <div className="relative rounded-3xl border border-[var(--border)] bg-white p-5 shadow-sm flex flex-col h-full">
      {offer.badge ? (
        <span className="absolute -top-3 right-5 rounded-full bg-[var(--trust-green)] px-3 py-1 text-xs font-bold text-white">
          {offer.badge}
        </span>
      ) : null}
      <p className="text-lg font-bold">{offer.label}</p>
      <p className="mt-2 text-3xl font-black text-[var(--date-brown)]">
        {formatKwd(offer.price)}
      </p>
      <p className="mt-2 text-sm text-[var(--muted)] flex-grow">
        {offer.quantity > 1
          ? `يطلع عليك الحبة بـ ${formatKwd(offer.price / offer.quantity)}`
          : "أفضل بداية للتجربة اليومية"}
      </p>
      <button 
        onClick={() => {
          const select = document.getElementById('offer-select') as HTMLSelectElement;
          if (select) select.value = offer.id;
          document.getElementById('checkout')?.scrollIntoView({ behavior: 'smooth' });
        }}
        className="mt-6 w-full rounded-full bg-[var(--khafeefa-olive)] py-3 text-center font-bold text-white transition-colors hover:bg-[var(--ink)]"
      >
        اطلب الحين وادفع عند الاستلام
      </button>
    </div>
  );
}
