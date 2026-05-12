# Design System

## Visual Direction

Khafeefa should look like a premium Gulf comfort brand, not a gadget reseller.

Style:

- Clean Arabic-first RTL ecommerce.
- Warm luxury, practical, not overly feminine.
- Soft rounded cards.
- Strong contrast CTAs.
- Plenty of proof badges.
- Product images should feel owned by the brand with consistent background, shadows, and packaging mockups.

## Colors

Use CSS variables and Tailwind theme tokens.

Primary:

- `khafeefa-olive`: `#5A6B42`
- Reason: grounded, calm, practical, premium, unisex.

Secondary:

- `sand`: `#F3E8D2`
- `warm-cream`: `#FFF9EF`
- `date-brown`: `#5B3B27`
- `cool-mint`: `#D8E7DE`

Accent:

- CTA orange: `#D97706`
- Trust green: `#168A52`
- Alert/scarcity: `#B45309`

Text:

- `ink`: `#181612`
- `muted`: `#6F675C`
- `border`: `#E7DCC8`

## Typography

Recommended:

- Arabic/body/headlines: `IBM Plex Sans Arabic` or `Noto Kufi Arabic`.
- English logo subtitle: `Inter`.

Load fonts through `next/font/google`.

Logo text:

- Arabic `خفيفة`: weight 700, rounded feel.
- English `khafeefa`: small uppercase/lowercase subtitle, letter spacing subtle.

## Logo Mark

Header mark:

- Circle filled with `khafeefa-olive`.
- Arabic letter `ن` inside in `warm-cream`.
- The user requested `N`; since brand is Arabic, use `ن` for Arabic identity. If an English-only fallback is needed, use `K`.

## Layout Rules

- Entire app uses `dir="rtl"` and `lang="ar-KW"`.
- Desktop sections alternate:
  - Section 1: text right, image left.
  - Section 2: image right, text left.
- Mobile stacks image then copy unless CTA needs to be above fold.
- Max content width: `1200px`.
- Rounded cards: `rounded-2xl` or `rounded-3xl`.
- Buttons: large, thumb-friendly, 48-56px height.

## Components

Required shared components:

- `Header`
- `Footer`
- `Logo`
- `TrustBadge`
- `ProductCard`
- `OfferSelector`
- `CartDrawer`
- `CheckoutModal`
- `UpsellModal`
- `ReviewCard`
- `VideoProofCard`
- `FAQAccordion`
- `SectionImagePlaceholder`
- `StickyMobileCTA`
- `PixelLoader`

## Image Placeholders

Use sample placeholders now and make them easy to replace later:

- Hero: lifestyle mock with product clipped to waist.
- Product gallery:
  - Product front.
  - Product on waist/belt.
  - Charging phone.
  - Packaging/what is in the box.
- Collection card.
- About page brand/process image.

Implementation options:

- Use local SVG/gradient placeholders in `frontend/public/images/placeholders`.
- Use CSS cards with Arabic labels until final images are provided.
- Do not rely on external image URLs for production.

## Motion

Use subtle motion only:

- Cart drawer slide.
- Modal fade/scale.
- Offer card selected state.
- Review carousel.

Library:

- `framer-motion` is acceptable for drawer/modal polish.
- Keep animations short and accessible.

## Accessibility

- All buttons need accessible labels.
- Modals trap focus and close on Escape.
- Color contrast must pass WCAG AA.
- Do not use motion that blocks checkout.

