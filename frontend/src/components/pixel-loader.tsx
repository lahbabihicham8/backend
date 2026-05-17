"use client";

import Script from "next/script";
import { useEffect, useRef } from "react";
import { trackPageView } from "@/lib/tracking";

const metaPixelId = process.env.NEXT_PUBLIC_META_PIXEL_ID;
const tiktokPixelId = process.env.NEXT_PUBLIC_TIKTOK_PIXEL_ID;
const snapPixelId = process.env.NEXT_PUBLIC_SNAP_PIXEL_ID;
const pixelsEnabled = process.env.NEXT_PUBLIC_ENABLE_PIXELS !== "false";

export function PixelLoader() {
  const activePixelCount = [metaPixelId, tiktokPixelId, snapPixelId].filter(Boolean).length;
  const hasTrackedPageView = useRef(false);

  useEffect(() => {
    if (!pixelsEnabled || activePixelCount === 0 || hasTrackedPageView.current) {
      return;
    }

    hasTrackedPageView.current = true;
    const timeoutId = window.setTimeout(trackPageView, 500);

    return () => window.clearTimeout(timeoutId);
  }, [activePixelCount]);

  if (!pixelsEnabled) {
    return null;
  }

  return (
    <>
      {metaPixelId ? (
        <Script id="meta-pixel" strategy="afterInteractive">
          {`
            !function(f,b,e,v,n,t,s)
            {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
            n.callMethod.apply(n,arguments):n.queue.push(arguments)};
            if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
            n.queue=[];t=b.createElement(e);t.async=!0;
            t.src=v;s=b.getElementsByTagName(e)[0];
            s.parentNode.insertBefore(t,s)}(window, document,'script',
            'https://connect.facebook.net/en_US/fbevents.js');
            fbq('init', '${metaPixelId}');
          `}
        </Script>
      ) : null}

      {tiktokPixelId ? (
        <Script id="tiktok-pixel" strategy="afterInteractive">
          {`
            !function (w, d, t) {
              w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];
              ttq.methods=["page","track","identify","instances","debug","on","off","once","ready","alias","group","enableCookie","disableCookie"];
              ttq.setAndDefer=function(t,e){t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}};
              for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);
              ttq.instance=function(t){for(var e=ttq._i[t]||[],n=0;n<ttq.methods.length;n++)ttq.setAndDefer(e,ttq.methods[n]);return e};
              ttq.load=function(e,n){var i="https://analytics.tiktok.com/i18n/pixel/events.js";
              ttq._i=ttq._i||{},ttq._i[e]=[],ttq._i[e]._u=i,ttq._t=ttq._t||{},ttq._t[e]=+new Date,ttq._o=ttq._o||{},ttq._o[e]=n||{};
              var o=document.createElement("script");o.type="text/javascript",o.async=!0,o.src=i+"?sdkid="+e+"&lib="+t;
              var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(o,a)};
              ttq.load('${tiktokPixelId}');
            }(window, document, 'ttq');
          `}
        </Script>
      ) : null}

      {snapPixelId ? (
        <Script id="snap-pixel" strategy="afterInteractive">
          {`
            (function(e,t,n){if(e.snaptr)return;var a=e.snaptr=function()
            {a.handleRequest?a.handleRequest.apply(a,arguments):a.queue.push(arguments)};
            a.queue=[];var s='script';r=t.createElement(s);r.async=!0;
            r.src=n;var u=t.getElementsByTagName(s)[0];
            u.parentNode.insertBefore(r,u);})(window,document,
            'https://sc-static.net/scevent.min.js');
            snaptr('init', '${snapPixelId}');
          `}
        </Script>
      ) : null}
    </>
  );
}
