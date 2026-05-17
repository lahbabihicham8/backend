"use client";

import { products, type Offer } from "@/data/products";

type PixelEventName = "PageView" | "ViewContent" | "AddToCart" | "InitiateCheckout" | "Purchase";

type PixelPayload = {
  content_ids?: string[];
  content_name?: string;
  content_type?: string;
  contents?: Array<{
    id: string;
    quantity: number;
    item_price: number;
  }>;
  currency?: string;
  value?: number;
  num_items?: number;
  event_id?: string;
  offer_id?: string;
  offer_label?: string;
  order_id?: string;
  checkout_type?: string;
};

declare global {
  interface Window {
    fbq?: (...args: unknown[]) => void;
    ttq?: {
      page?: () => void;
      track?: (event: string, payload?: Record<string, unknown>) => void;
    };
    snaptr?: (...args: unknown[]) => void;
  }
}

const product = products[0];

const pixelEventMap: Record<PixelEventName, { tiktok: string; snap: string }> = {
  PageView: { tiktok: "PageView", snap: "PAGE_VIEW" },
  ViewContent: { tiktok: "ViewContent", snap: "VIEW_CONTENT" },
  AddToCart: { tiktok: "AddToCart", snap: "ADD_CART" },
  InitiateCheckout: { tiktok: "InitiateCheckout", snap: "START_CHECKOUT" },
  Purchase: { tiktok: "CompletePayment", snap: "PURCHASE" }
};

export function createEventId(prefix: string) {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return `${prefix}_${crypto.randomUUID()}`;
  }

  return `${prefix}_${Date.now()}_${Math.random().toString(16).slice(2)}`;
}

export function buildOfferPayload(offer: Offer, eventId = createEventId("pixel")): PixelPayload {
  return {
    content_ids: [product.id],
    content_name: product.title,
    content_type: "product",
    contents: [
      {
        id: product.id,
        quantity: offer.quantity,
        item_price: Number((offer.price / offer.quantity).toFixed(3))
      }
    ],
    currency: product.currency,
    value: offer.price,
    num_items: offer.quantity,
    event_id: eventId,
    offer_id: offer.id,
    offer_label: offer.label
  };
}

export function getPixelPayloadForOffer(offerId: string, eventId?: string) {
  const offer = product.offers.find((item) => item.id === offerId) ?? product.offers[0];
  return buildOfferPayload(offer, eventId);
}

export function trackPixelEvent(eventName: PixelEventName, payload: PixelPayload = {}) {
  if (process.env.NEXT_PUBLIC_ENABLE_PIXELS === "false" || typeof window === "undefined") {
    return;
  }

  const mappedEvent = pixelEventMap[eventName];

  window.fbq?.("track", eventName, payload, payload.event_id ? { eventID: payload.event_id } : undefined);
  window.ttq?.track?.(mappedEvent.tiktok, payload as Record<string, unknown>);
  window.snaptr?.("track", mappedEvent.snap, payload);
}

export function trackPageView() {
  const eventId = createEventId("page");
  const payload = buildOfferPayload(product.offers[0], eventId);

  window.fbq?.("track", "PageView", {}, { eventID: eventId });
  window.ttq?.page?.();
  window.snaptr?.("track", "PAGE_VIEW", { event_id: eventId });
  trackPixelEvent("ViewContent", payload);
}
