# Site Architecture and CRO

## Pages

Required routes:

- `/`: home page.
- `/products/waist-fan-powerbank`: primary product landing page.
- `/collections`: collection page.
- `/about`: about us.
- `/contact`: contact us.
- `/thank-you/[orderId]`: thank-you page after successful order.
- `/privacy`, `/terms`, `/refund-policy`, `/shipping-policy`: trust/legal pages.

Optional admin route is not required for V1.

## Header

Arabic RTL layout. Desktop header starts at the right:

1. Circular mark with `ن` inside, using brand primary color.
2. Text logo:
   - Arabic: `خفيفة`
   - English under it: `khafeefa`
3. Menu links.
4. Cart button.

Mobile header:

- Logo right.
- Cart and menu left.
- Sticky but lightweight.

## Footer

Include:

- Brand logo and short promise.
- Shop links.
- Support links.
- Policies.
- WhatsApp/contact.
- COD/trust badges.
- Copyright.

## Home Page Structure

Goal: make Khafeefa feel like a real branded store before the product page sells hard.

Sections:

1. Hero:
   - Right: emotional Arabic headline.
   - Left: sample product/brand lifestyle image placeholder.
   - CTA: `تسوق الأكثر طلباً`
   - Secondary CTA: `كيف نختار منتجاتنا؟`
   - Badges: COD, Kuwait delivery, quality checked.

   Suggested copy:
   `خفيفة على يومك... قوية وقت تحتاجها`
   `منتجات عملية نختارها للحر والمشاوير والحياة السريعة في الكويت.`

2. Authority strip:
   - `فحص قبل التغليف`
   - `توصيل داخل الكويت`
   - `دفع عند الاستلام`
   - `دعم واتساب`

3. Featured product block:
   - Product image.
   - Star rating UI.
   - Price offers.
   - CTA to product page.
   - Short proof bullets.

4. Problem agitation:
   - Heat, walking, carrying phone/power bank/fan, waiting in car/outdoor.
   - Use alternating text/image layout.

5. Product solution:
   - Hands-free airflow.
   - Power bank emergency feature.
   - Waist/clip portability.
   - Compact design.

6. Why Khafeefa:
   - curated for Gulf use.
   - no random marketplace confusion.
   - clear support and COD.

7. UGC/social proof carousel:
   - Video placeholders for later UGC.
   - Review cards.

8. Offer block:
   - 1-piece offer and `Buy 2, get 1 free` bundle.
   - Push the 3-piece bundle as `الأكثر طلباً` and `أفضل قيمة للعائلة`.

9. FAQ:
   - Kuwait number/COD/delivery.
   - Battery use.
   - Warranty/exchange.
   - How to wear/use.

10. Final CTA.

## Product Landing Page

This is the main conversion page. Use a product-detail layout on desktop:

- Right side: copy, title, stars, selected offer, CTA, trust badges.
- Left side: gallery with 4 sample placeholders.
- Mobile: gallery first, then sticky CTA.

Required sections:

1. Product hero:
   - Title: `مروحة خفيفة للخصر مع باور بانك`
   - Subtitle: `هواء قريب منك + شحن للطوارئ في جهاز واحد، مصمم لمشاوير الكويت والحر اليومي.`
   - Stars and review count placeholder.
   - Offers:
     - 1 piece: `18.900 د.ك`
     - Buy 2, get 1 free: `29.900 د.ك` for 3 total pieces
   - Badge on bundle: `الأكثر طلباً`
   - Secondary badge on bundle: `خذ 3 وادفع عن 2`
   - CTA: `أضف العرض وافتح السلة`
   - CTA behavior: add selected offer to cart and open cart drawer.

2. Pain section:
   - `الحر ما ينتظر... والمشاوير ما تخلص`
   - Explain embarrassment, sweat, waiting, family outings.

3. Solution section:
   - Hands-free airflow.
   - Clip/waist use.
   - Power bank emergency convenience.
   - 4000mAh battery.
   - 5 wind speeds.

4. Proof/authority section:
   - `اختبارات خفيفة قبل التغليف`
   - Airflow check across 5 speeds, battery/USB charge check, button check, clip check, packaging check.
   - Supplier-listed certificates can be shown only after verification for the exact batch/model.

5. Use-case grid:
   - Work.
   - Car/parking.
   - Mall/souk.
   - Chalet/camping.
   - School pickup.
   - Family outings.

6. Comparison table:
   - Khafeefa product vs generic cheap fan:
     - branded support.
     - quality checked.
     - COD.
     - bundle offers.
     - easy replacement for manufacturing defect.

7. UGC/video section:
   - 3-4 video placeholders.
   - Later replace with AI/UGC videos.

8. Offer stack:
   - Repeat offers near bottom.
   - Scarcity copy: `الكمية اليومية محدودة حسب تجهيز الطلبات`
   - Do not fake exact countdown unless inventory logic exists.

9. FAQ.

10. Sticky mobile CTA:
   - Shows selected offer price.
   - Button adds to cart and opens cart.

## Collection Page

V1 has one hero product but should feel scalable.

Sections:

- Collection hero: `منتجات تخفف يومك`
- Product cards with image, rating, short copy, price/from, CTA.
- Trust strip.
- Coming-soon cards may be shown as `قريباً` only if they do not distract.

Product card needs:

- Heading.
- Subheading.
- Star rating.
- Offer preview.
- Scarcity/trust badge.
- CTA.

## Cart Drawer

Open on add-to-cart. Must feel like a continuation of the sale.

Contents:

- Items and quantities.
- Offer savings line.
- Progress message: `أضفت عرض ممتاز. تقدر تزيد منتج بسعر خاص قبل تأكيد الطلب.`
- Cross-sell carousel:
  - Placeholder products, with `قريباً` if not yet sellable.
  - Do not allow ordering unavailable cross-sells.
- CTA: `تأكيد الطلب`
- CTA opens checkout popup.

Cart should not navigate away before checkout.

## Checkout Popup

COD only, two fields:

- Name.
- Kuwait phone number.

Validation:

- Name: 2-80 chars, Arabic/English spaces allowed.
- Phone: valid Kuwait mobile number or whitelisted `55000000`, `60000000`, or `90000000`.
- Accept display formats like `50000000`, `+96550000000`, `96550000000`.
- The three test numbers are whitelisted even if fraud checks would otherwise block a local test.
- Normalize real Kuwait phone to `+965XXXXXXXX`.

Popup content:

- Order summary.
- COD badge.
- Social proof/authority line.
- Scarcity line.
- Privacy reassurance.

CTA:

`ثبت طلبي والدفع عند الاستلام`

After submit:

1. Backend validates Kuwait phone.
2. Backend checks MaxMind fraud/Kuwait IP gate.
3. Backend creates order and sends server events.
4. Frontend shows 10-15 second upsell modal.

## Post-Order Upsell

After valid initial order, show an upsell for 10-15 seconds.

Rules:

- This is the only place a product is discounted.
- Upsell price: `18.900 KWD`.
- User can accept or skip.
- Accept should call backend to append upsell item to existing order.
- If timer ends, continue to thank-you.

Copy:

`عرض خاص لطلبك فقط`
`أضف قطعة إضافية بسعر خاص 18.900 د.ك قبل تجهيز الطلب.`

## Thank You Page

Show:

- Order ID.
- Summary.
- `تم استلام طلبك`
- COD confirmation.
- Expected contact/delivery note.
- WhatsApp support link.
- Reminder: keep phone available.

Also fire client-side purchase pixels with same `event_id` returned by backend/order flow where applicable.

