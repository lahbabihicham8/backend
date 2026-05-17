"use client";

import { useState } from "react";
import { formatKwd, products } from "@/data/products";
import { createEventId, getPixelPayloadForOffer, trackPixelEvent } from "@/lib/tracking";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || "https://getkhafeefa-backend.amt9aa.easypanel.host";
const product = products[0];

const orderErrorMessages: Record<string, string> = {
  INVALID_PHONE: "رقم الهاتف لازم يكون رقم كويتي صحيح من ٨ أرقام ويبدأ بـ 5 أو 6 أو 9.",
  NON_KUWAIT_PHONE: "رقم الهاتف لازم يكون رقم كويتي.",
  ORDER_REGION_BLOCKED: "الطلب مرفوض لأن الاتصال لا يظهر من الكويت. جرّب بدون VPN أو من شبكة كويتية.",
  VPN_OR_PROXY_BLOCKED: "الطلب مرفوض لأنك تستخدم VPN أو Proxy. جرّب إيقاف الـ VPN وقت الطلب.",
  HIGH_RISK_ORDER: "تعذر قبول الطلب حالياً. تواصل معنا عبر واتساب لإتمام الطلب."
};

function normalizeKuwaitPhone(phone: string) {
  const westernDigits = phone.replace(/[٠-٩۰-۹]/g, (digit) =>
    String("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹".indexOf(digit) % 10)
  );
  const digits = westernDigits.replace(/\D/g, "");

  if (digits.startsWith("00965")) {
    return digits.slice(5);
  }

  if (digits.startsWith("965")) {
    return digits.slice(3);
  }

  return digits;
}

export function CheckoutForm() {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const offers = product.offers;

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const offerId = String(formData.get("offer") ?? offers[0].id);
    const offer = offers.find((item) => item.id === offerId) ?? offers[0];
    const phone = normalizeKuwaitPhone(String(formData.get("phone") ?? ""));

    if (!/^[569]\d{7}$/.test(phone)) {
      setErrorMessage(orderErrorMessages.INVALID_PHONE);
      return;
    }

    const eventId = createEventId("order");
    const orderPayload = {
      ...getPixelPayloadForOffer(offerId, eventId),
      order_id: eventId,
      checkout_type: "cod"
    };

    setIsSubmitting(true);
    setErrorMessage("");
    trackPixelEvent("InitiateCheckout", orderPayload);

    try {
      const response = await fetch(`${apiBaseUrl.replace(/\/$/, "")}/v1/orders`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          customer_name: String(formData.get("customer_name") ?? ""),
          phone,
          address: String(formData.get("address") ?? ""),
          items: [
            {
              product_id: product.id,
              offer_id: offer.id,
              quantity: 1
            }
          ],
          currency: product.currency,
          payment_method: "COD",
          event_id: eventId,
          landing_page_url: window.location.href
        })
      });

      if (!response.ok) {
        const errorBody = await response.json().catch(() => null);
        throw new Error(errorBody?.detail || "ORDER_SUBMIT_FAILED");
      }

      const createdOrder = await response.json();
      setIsSubmitting(false);
      setIsSuccess(true);
      trackPixelEvent("Purchase", {
        ...orderPayload,
        order_id: createdOrder.order_id
      });
    } catch (error) {
      console.error(error);
      setIsSubmitting(false);
      const errorCode = error instanceof Error ? error.message : "";
      setErrorMessage(orderErrorMessages[errorCode] ?? "تعذر إرسال الطلب. حاول مرة ثانية أو تواصل معنا عبر واتساب.");
    }
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
            name="customer_name"
            type="text"
            required
            className="w-full rounded-xl border border-[var(--border)] px-4 py-3 focus:border-[var(--khafeefa-olive)] focus:outline-none"
            placeholder="محمد عبدالله"
          />
        </div>
        <div>
          <label className="mb-2 block text-sm font-bold text-[var(--ink)]">رقم الهاتف</label>
          <input
            name="phone"
            type="tel"
            required
            inputMode="numeric"
            autoComplete="tel"
            maxLength={12}
            className="w-full text-left rounded-xl border border-[var(--border)] px-4 py-3 focus:border-[var(--khafeefa-olive)] focus:outline-none"
            dir="ltr"
            placeholder="90000000"
          />
        </div>
        <div>
          <label className="mb-2 block text-sm font-bold text-[var(--ink)]">العنوان بالتفصيل</label>
          <textarea
            name="address"
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
            name="offer"
            required
            className="w-full rounded-xl border border-[var(--border)] bg-white px-4 py-3 focus:border-[var(--khafeefa-olive)] focus:outline-none"
          >
            {offers.map(offer => (
              <option key={offer.id} value={offer.id}>
                {offer.label} - {formatKwd(offer.price)}
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
        {errorMessage ? (
          <p className="rounded-2xl bg-red-50 p-3 text-center text-sm font-bold text-red-700">
            {errorMessage}
          </p>
        ) : null}
      </form>
    </div>
  );
}
