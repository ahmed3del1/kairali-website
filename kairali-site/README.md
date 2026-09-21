# Kairali Spa — website rebuild

Static, bilingual (Arabic RTL / English LTR) site. No framework, no build step for hosting — deploy the folder as-is
(Vercel: framework preset **Other**, no build command, output = repo root).

```
index.html            Home            /about/  /services/  /ayurveda/  /reviews/
about/ … book/        real routes     /contact/  /complaints/  /book/  /privacy/
assets/css/style.css  design system (ivory · deep olive · matte gold, logical properties for RTL/LTR)
assets/js/app.js      language toggle, nav, booking wizard, recommender, reviews, complaints, consent + pixels
assets/js/config.js   public endpoints (Supabase anon key, Apps Script URL, pixel IDs, opening hours)
assets/js/data.js     GENERATED (services, recommender keywords, UI strings)
assets/img, video     photos (see CREDITS.md) + 12 s hero loop
tools/content.py      services, prices, FAQ, keywords, UI strings  ← edit copy/prices here
tools/build.py        generates all HTML + data.js + sitemap/robots/vercel.json   → python3 tools/build.py
```

Change a price, a service, a sentence or a photo → edit `tools/content.py` / `tools/build.py` → `python3 tools/build.py`.
Local preview: `python3 -m http.server 8000` then open http://localhost:8000.

## Safe local testing
On `localhost` the site is in **demo mode**: bookings / reviews / complaints are *not* written to Supabase, Telegram or the
Sheet, and the ad pixels never load. Available times are still read from the live `booking_slots` view (read-only).

## What follows the client's written change lists (Part 6) verbatim
Home hero, "تجربة كيرالي تبدأ من التفاصيل" block, "اكتشفي جلسات كيرالي سبا" cards (01/02/03, gold line, Abhyanga text),
reviews block heading / KAIRALI EXPERIENCE label (hidden when no approved reviews — two real ones exist today, so it shows),
dark-olive footer with `© KAIRALI SPA 2026`, About ("من نحن", THE KAIRALI STORY, quote block, 01/02/03 list, closing quote),
ivory/olive/gold palette, no emoji in the UI, real-space photography where we have it.

## DRAFT copy that needs client approval  (marked [OPEN] in the brief)
- Whole site moved to consistent formal Arabic (old copy was Kuwaiti dialect) — brief 6.5-3.
- Shirodhara and Kizhi card descriptions on Home (client only supplied Abhyanga) and their Arabic names.
- Shortened About story chunks (3 short lines, adapted from the old text).
- English versions of every new string.
- Service descriptions / FAQ / Ayurveda / Reviews / Complaints / Booking copy rewritten in MSA with the softer claims
  ("inspired by", no "100% natural / imported / trained in Indian medicine").
- Booking confirmation now says "تم تسجيل حجزك — سيتواصل معك فريقنا عبر واتساب" (the old "we'll send a WhatsApp confirmation"
  is not implemented — brief item 7.7).
- Privacy Policy page is a template. Freelancer credit line kept small/muted in the footer — remove if the client says no.
- Brand name: "Kairali Spa" used (client's new copy). Map link is a search URL — replace with the real Google Maps link.

## Before going live
1. **Logo** — the mark in the header/footer is a placeholder line-art lotus + wordmark. Replace the `#i-logo` symbol in
   `tools/build.py` (or swap `brand()` for an `<img>`) with the real vector logo.
2. **Photos** — the Kairali stills/hero video are real (frames from the client's own videos: sign, uniforms, treatment rooms).
   Confirm the guests shown have agreed to appear. The stock photos (Unsplash licence) are placeholders for the shots the
   client still owes us (copper vessel, bed, herbs, hot stones…). See CREDITS.md.
3. **Domain** — set `SITE` in `tools/build.py`, rebuild (canonicals, sitemap, OG tags), attach the domain in Vercel.
4. **Hosting plan** — Vercel Hobby is non-commercial; pick a paid plan / other host.
5. **Secrets** — rotate the Telegram bot token and the Meta / TikTok access tokens that were pasted into chats (they live in the Apps Script).
6. **Data** — delete the test rows in `bookings` before launch.
7. **Apps Script** — the booking payload now also carries `event_id`; use it as the Meta/TikTok server-event `event_id`
   so browser and server events de-duplicate.

## Known limits (brief Part 7 — not solved by a static front-end)
- Double-booking is re-checked in the browser right before insert, but only a database constraint can fully prevent a race
  (Postgres exclusion constraint / `create_booking()` RPC).
- Notifications are still browser → Apps Script (`no-cors`, fire-and-forget); move to a server-side function.
- Honeypot fields reduce spam; real rate-limiting / CAPTCHA needs a server component.
- English/Arabic share one URL (language toggle), so no `hreflang`.
- Fonts come from Google Fonts; self-host them for the last bit of speed.
