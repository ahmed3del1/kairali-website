#!/usr/bin/env python3
"""Generates every page of the Kairali Spa site.

    python3 tools/build.py

Copy that the client supplied verbatim is marked CLIENT. Everything marked DRAFT was written by us
in formal Arabic / English and needs client approval (see README).
"""
import html, json, pathlib, urllib.parse
from content import SERVICES, FAQ, SYMPTOMS, STR

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = "https://kairali-website.vercel.app"      # change when the custom domain is attached
PHONE_DISPLAY = "+965 9770 6554"
WA_TEXT = "مرحبًا، أودّ الاستفسار عن جلسات كيرالي سبا"
WA = "https://wa.me/96597706554?text=" + urllib.parse.quote(WA_TEXT)
IG = "https://instagram.com/kairali_kw"
MAPS = "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote("Kairali Sabah Al-Salem Block 3 Street 306 Building 26 Kuwait")
ADDR = "Sabah Alsalem, Block 3, Street 306, Building 26, Floor 2"

esc = lambda s: html.escape(s, quote=True)
L = lambda en: f'data-en="{esc(en)}"'
def T(tag, ar, en, cls="", extra=""):
    c = f' class="{cls}"' if cls else ""
    return f"<{tag}{c} {L(en)}{(' ' + extra) if extra else ''}>{ar}</{tag}>"
def LA(attr, ar, en): return f'{attr}="{esc(ar)}" data-en-{attr}="{esc(en)}"'
def ic(name, cls=""): return f'<svg class="ic {cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'
def img(name, alt_ar, alt_en, cls="", style="", eager=False, w=None, h=None):
    parts = [f'src="/assets/img/{name}.webp"', LA("alt", alt_ar, alt_en)]
    if w: parts.append(f'width="{w}" height="{h}"')
    if not eager: parts.append('loading="lazy" decoding="async"')
    if cls: parts.append(f'class="{cls}"')
    if style: parts.append(f'style="{style}"')
    return "<img " + " ".join(parts) + ">"

SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>
<symbol id="i-logo" viewBox="0 0 48 48"><circle cx="24" cy="24" r="22.5"/><path d="M24 10c3.4 3.6 5 7 5 10.5S27 27 24 29c-3-2-5-5-5-8.5S20.6 13.6 24 10Z"/><path d="M24 29c-5.2 0-10.6-2.6-13.4-8 4-.7 7.8.6 10.6 3.3"/><path d="M24 29c5.2 0 10.6-2.6 13.4-8-4-.7-7.8.6-10.6 3.3"/><path d="M15 35h18"/></symbol>
<symbol id="i-drop" viewBox="0 0 24 24"><path d="M12 3c3.5 4.6 6 7.6 6 11a6 6 0 0 1-12 0c0-3.4 2.5-6.4 6-11Z"/><path d="M9.2 14.4a3 3 0 0 0 2.4 2.6"/></symbol>
<symbol id="i-leaf" viewBox="0 0 24 24"><path d="M5 19c0-8 5-14 14-14 0 9-5 14-14 14Z"/><path d="M5 19c3-4 6-7 10-9"/></symbol>
<symbol id="i-lamp" viewBox="0 0 24 24"><path d="M12 2.5c1.3 1.7 2 2.8 2 4a2 2 0 0 1-4 0c0-1.2.7-2.3 2-4Z"/><path d="M3.5 12h17c0 3.4-3.8 6-8.5 6s-8.5-2.6-8.5-6Z"/><path d="M9 21.5h6M12 18v3.5"/></symbol>
<symbol id="i-door" viewBox="0 0 24 24"><path d="M6 21V9.5a6 6 0 0 1 12 0V21"/><path d="M3.5 21h17"/><path d="M14.8 13.5v2"/></symbol>
<symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11Z"/><circle cx="12" cy="10" r="2.4"/></symbol>
<symbol id="i-phone" viewBox="0 0 24 24"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2Z"/></symbol>
<symbol id="i-insta" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><path d="M17.4 6.6v.01"/></symbol>
<symbol id="i-wa" viewBox="0 0 24 24"><path d="M4 20l1.3-4.2A8.5 8.5 0 1 1 8.4 19L4 20Z"/><path d="M9.2 8.8c.2 2.4 2.5 5 5.4 5.9l1.2-1.4-1.9-1-.9.8c-.9-.3-1.9-1.2-2.2-2.2l.8-.9-1-1.9-1.4 1.1Z"/></symbol>
<symbol id="i-arrow" viewBox="0 0 24 24"><path d="M19 12H5M11 6l-6 6 6 6"/></symbol>
<symbol id="i-plus" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></symbol>
<symbol id="i-check" viewBox="0 0 24 24"><path d="M5 12.5l4.5 4.5L19 7.5"/></symbol>
<symbol id="i-close" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></symbol>
<symbol id="i-quote" viewBox="0 0 48 48"><path d="M20 12c-6 3-10 8-10 16v8h12V24h-6c0-4 2-7 6-9l-2-3ZM42 12c-6 3-10 8-10 16v8h12V24h-6c0-4 2-7 6-9l-2-3Z"/></symbol>
<symbol id="i-wind" viewBox="0 0 24 24"><path d="M3 9h11a3 3 0 1 0-3-3"/><path d="M3 14h15a3 3 0 1 1-3 3"/><path d="M3 19h6"/></symbol>
<symbol id="i-flame" viewBox="0 0 24 24"><path d="M12 3c1 3.5 5 5.5 5 10a5 5 0 0 1-10 0c0-2 1-3.2 2-4.2.3 1.4 1 2.2 2 2.2-.2-3.2-.5-5.2 1-8Z"/></symbol>
<symbol id="i-mountain" viewBox="0 0 24 24"><path d="M2.5 19.5l6-10 4 6 3-4 6 8h-19Z"/></symbol>
<symbol id="i-star" viewBox="0 0 24 24"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9L12 3Z"/></symbol>
</defs></svg>"""

NAV = [("/", "الرئيسية", "Home"), ("/about/", "من نحن", "About Us"), ("/services/", "خدماتنا", "Services"),
       ("/ayurveda/", "الأيورفيدا", "Ayurveda"), ("/reviews/", "آراء العملاء", "Reviews"),
       ("/contact/", "تواصل معنا", "Contact"), ("/complaints/", "الشكاوى", "Complaints")]

def brand(sub=True):
    subtxt = '<span class="brand__sub">Indian Wellness &amp; Massage</span>' if sub else ""
    return (f'<a class="brand" href="/" aria-label="Kairali Spa">{ic("logo")}'
            f'<span class="brand__txt"><span class="brand__name">KAIRALI</span>{subtxt}</span></a>')

def header():
    links = "".join(f'<a href="{h}" {L(en)}>{ar}</a>' for h, ar, en in NAV)
    dlinks = "".join(f'<a href="{h}"><span {L(en)}>{ar}</span>{ic("arrow", "flip")}</a>' for h, ar, en in NAV + [("/book/", "الحجز", "Book")])
    return f"""<a class="skip" href="#main" {L("Skip to content")}>تخطي إلى المحتوى</a>
<header class="nav"><div class="wrap nav__in">
  {brand()}
  <nav class="nav__links" {LA("aria-label", "القائمة الرئيسية", "Main navigation")}>{links}</nav>
  <div class="nav__side">
    <button class="lang-btn" type="button">EN</button>
    <a class="btn nav__cta" href="/book/" {L("Book")}>الحجز</a>
    <button class="burger" type="button" {LA("aria-label", "فتح القائمة", "Open menu")} aria-expanded="false"><span></span></button>
  </div>
</div></header>
<div class="drawer" role="dialog" aria-modal="true" {LA("aria-label", "القائمة", "Menu")}>
  <div class="drawer__top">{brand(False)}<button class="drawer__close btn btn--line-lt" type="button" style="min-height:44px;padding:.4rem 1rem" {LA("aria-label", "إغلاق", "Close")}>{ic("close")}</button></div>
  <nav class="drawer__links">{dlinks}</nav>
  <div class="drawer__foot"><button class="lang-btn btn btn--line-lt" type="button">EN</button><a class="btn btn--gold" href="{WA}" rel="noopener">{ic("wa")} WhatsApp</a></div>
</div>"""

def footer():
    links = "".join(f'<li><a href="{h}" {L(en)}>{ar}</a></li>' for h, ar, en in NAV + [("/book/", "الحجز", "Book"), ("/privacy/", "سياسة الخصوصية", "Privacy Policy")])
    return f"""<footer class="footer"><div class="wrap">
  <div class="footer__grid">
    <div>{brand()}</div>
    <div><h4 {L("Contact")}>تواصل</h4>
      <ul class="info-list">
        <li>{ic("pin")}<span>{ADDR} — <span {L("Kuwait")}>الكويت</span></span></li>
        <li>{ic("phone")}<a href="tel:+96597706554" dir="ltr">{PHONE_DISPLAY}</a></li>
        <li>{ic("insta")}<a href="{IG}" rel="noopener" dir="ltr">@kairali_kw</a></li>
        <li>{ic("clock")}<span {L("Daily: 10:00 AM – 9:00 PM")}>يوميًا: 10:00 ص – 9:00 م</span></li>
      </ul></div>
    <nav {LA("aria-label", "روابط التذييل", "Footer links")}><h4 {L("Explore")}>استكشفي</h4><ul>{links}</ul></nav>
  </div>
  <div class="footer__bottom">© KAIRALI SPA 2026
    <span class="footer__credit"><span {L("This website was created by")}>تم إنشاء هذا الموقع بواسطة</span> Eng: Ahmed Adel · <a href="mailto:ahmedautomation@hotmail.com">ahmedautomation@hotmail.com</a></span>
  </div>
</div></footer>"""

def floats(show_mbar=True):
    out = f'<div class="floats"><a class="float" href="{IG}" rel="noopener" {LA("aria-label", "انستجرام", "Instagram")}>{ic("insta")}</a><a class="float float--wa" href="{WA}" rel="noopener" {LA("aria-label", "واتساب", "WhatsApp")}>{ic("wa")}</a></div>'
    if show_mbar:
        out += (f'<div class="mbar"><a class="btn btn--solid" href="/book/" {L("Book")}>الحجز</a>'
                f'<a class="btn btn--line sq" href="{WA}" rel="noopener" {LA("aria-label", "واتساب", "WhatsApp")}>{ic("wa")}</a>'
                f'<a class="btn btn--line sq" href="{IG}" rel="noopener" {LA("aria-label", "انستجرام", "Instagram")}>{ic("insta")}</a></div>')
    return out

CONSENT = f"""<div class="consent" id="consent" hidden role="dialog" {LA("aria-label", "ملفات تعريف الارتباط", "Cookies")}>
  <p {L('We use cookies and ad-measurement tools to improve your experience and measure our campaigns. <a href="/privacy/">Privacy Policy</a>')}>نستخدم ملفات تعريف الارتباط وأدوات قياس الإعلانات لتحسين تجربتك وقياس أداء حملاتنا. <a href="/privacy/">سياسة الخصوصية</a></p>
  <div class="consent__act"><button class="btn btn--gold" type="button" data-consent="yes" {L("Accept")}>أوافق</button><button class="btn btn--line-lt" type="button" data-consent="no" {L("Decline")}>رفض</button></div>
</div>"""

def head(title_ar, title_en, desc_ar, desc_en, path, og="og-image.jpg", extra="", noindex=False):
    url = SITE + path
    return f"""<!doctype html>
<html lang="ar" dir="rtl" data-title-en="{esc(title_en)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title_ar)}</title>
<meta name="description" content="{esc(desc_ar)}" data-en-content="{esc(desc_en)}">
{'<meta name="robots" content="noindex">' if noindex else ''}
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Kairali Spa">
<meta property="og:title" content="{esc(title_ar)}"><meta property="og:description" content="{esc(desc_ar)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/assets/img/{og}"><meta property="og:locale" content="ar_KW"><meta property="og:locale:alternate" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#2A3318">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Sans+Arabic:wght@300;400;500&display=swap">
<link rel="stylesheet" href="/assets/css/style.css">
{extra}
</head>"""

def page(path, slug, title, desc, body, hero=False, mbar=True, extra_head="", noindex=False, scripts=True):
    (t_ar, t_en), (d_ar, d_en) = title, desc
    out = head(t_ar, t_en, d_ar, d_en, path, extra=extra_head, noindex=noindex)
    out += f'\n<body data-page="{slug}" class="{"" if hero else "page-inner"}">\n{SPRITE}\n{header()}\n<main id="main">\n{body}\n</main>\n{footer()}\n{floats(mbar)}\n{CONSENT}\n'
    if scripts:
        out += '<script src="/assets/js/config.js"></script>\n<script src="/assets/js/data.js"></script>\n<script src="/assets/js/app.js" defer></script>\n'
    out += "</body>\n</html>\n"
    target = ROOT / path.strip("/") / "index.html" if path != "/" else ROOT / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(out, encoding="utf-8")

def page_head(eyebrow, ar, en, lead=None, lead_en=None):
    lead_html = f'<p class="lead reveal" data-d="1" {L(lead_en)}>{lead}</p>' if lead else ""
    return (f'<section class="wrap page-head"><p class="eyebrow">{eyebrow}</p>{T("h1", ar, en, "h1 reveal", "")}{lead_html}</section>')

def stars_static(n=5):
    return '<span class="stars" aria-hidden="true">' + "".join(ic("star") for _ in range(n)) + "</span>"

svc = {s["id"]: s for s in SERVICES}

# ============================================================================ HOME
def home():
    cards = []
    for i, (sid, pos) in enumerate([("abhyanga", "50% 50%"), ("shirodhara", "12% 50%"), ("kizhi", "50% 50%")], 1):
        s = svc[sid]
        cards.append(f"""<a class="s-card reveal" data-d="{i}" href="/services/#svc-{sid}">
  {img(s["img"], s["ar"], s["latin"], style="object-position:" + pos)}
  <span class="s-card__num">0{i}</span>
  <div class="s-card__body"><div class="s-card__latin">{s["latin"].upper()}</div>
  {T("div", s["ar"], s["latin"], "s-card__ar")}
  {T("p", s["short"][0], s["short"][1], "s-card__desc")}
  <span class="s-card__link"><span {L("Discover the session")}>اكتشفي الجلسة</span>{ic("arrow", "flip")}</span></div></a>""")
    pts = [("drop", "زيوت مختارة بعناية", "Carefully chosen oils", "زيوت وأعشاب مستوحاة من تقاليد العناية الهندية.", "Oils and herbs inspired by Indian care traditions."),
           ("door", "خصوصية وراحة", "Privacy & comfort", "أجواء هادئة وتجربة مصممة لراحتك من لحظة وصولك.", "A calm atmosphere and an experience designed for your comfort from the moment you arrive."),
           ("lamp", "خبرة هندية أصيلة", "Authentic Indian expertise", "جلسات تقدمها أخصائيات بخبرة في أساليب المساج الهندي.", "Sessions delivered by specialists experienced in Indian massage techniques.")]
    points = "".join(f'<div class="point reveal" data-d="{i}">{ic(n)}<div>{T("h3", a, ae)}{T("p", b, be)}</div></div>' for i, (n, a, ae, b, be) in enumerate(pts, 1))
    body = f"""
<section class="hero">
  <div class="hero__media"><video autoplay muted loop playsinline preload="metadata" poster="/assets/img/hero-poster.webp" aria-hidden="true"><source src="/assets/video/hero.mp4" type="video/mp4"></video></div>
  <div class="wrap hero__in"><div class="hero__copy">
    <p class="eyebrow">Kairali Spa · Indian Wellness &amp; Massage</p>
    {T("h1", "من قلب الهند... تجربة عناية صنعت لراحتك", "From the heart of India… a care experience made for your comfort", "h1")}
    {T("p", "في Kairali، نقدم لك تجربة مستوحاة من تقاليد العناية الهندية العريقة، بزيوت طبيعية وأجواء مصممة للراحة والاسترخاء.", "At Kairali we offer an experience inspired by long-standing Indian care traditions, with natural oils and an atmosphere designed for comfort and relaxation.", "lead")}
    <div class="hero__cta"><a class="btn btn--gold" href="/book/" {L("Book")}>الحجز</a><a class="btn btn--line-lt" href="/services/" {L("Our Services")}>خدماتنا</a></div>
    <ul class="hero__facts"><li>{ic("pin")}<span>Sabah Alsalem · <span {L("Kuwait")}>الكويت</span></span></li><li>{ic("clock")}<span {L("Daily 10:00 AM – 9:00 PM")}>يوميًا 10:00 ص – 9:00 م</span></li></ul>
  </div></div>
  <div class="hero__scroll" aria-hidden="true">Scroll</div>
</section>

<section class="sec">
  <div class="wrap split split--rev">
    <div class="stack-lg">
      <p class="eyebrow">The Kairali Experience</p>
      {T("h2", "تجربة كيرالي تبدأ من التفاصيل", "The Kairali experience begins with the details", "h2 reveal")}
      {T("p", "عناية هندية أصيلة، بتفاصيل مختارة لتمنحك تجربة هادئة ومتكاملة.", "Authentic Indian care, with carefully chosen details for a calm, complete experience.", "lead reveal")}
      <div class="points">{points}</div>
    </div>
    <div class="photo photo--tall photo--arch reveal">{img("real-tray", "طاولة العلاج في كيرالي سبا: مصابيح نحاسية وكمادات عشبية وشموع", "Kairali Spa treatment table: brass lamps, herbal compresses and candles", style="object-position:50% 82%")}</div>
  </div>
</section>

<section class="sec sec--tight sec--sand">
  <div class="wrap">
    <div class="sec-head">
      <p class="eyebrow">The Sessions</p>
      {T("h2", "اكتشفي جلسات كيرالي سبا", "Discover Kairali Spa sessions", "h2 reveal")}
    </div>
    <div class="sessions">{''.join(cards)}</div>
    <div class="sessions-foot"><a class="btn btn--line" href="/services/" {L("Explore all sessions")}>استكشفي جميع الجلسات</a></div>
  </div>
</section>

<section class="sec" id="homeReviews" hidden>
  <div class="wrap">
    <p class="eyebrow">Kairali Experience</p>
    {T("h2", "من تجارب عملاء كيرالي", "From Kairali guests' experiences", "h2 reveal")}
    <div class="reviews-grid" id="homeRevGrid"></div>
    <p style="margin-top:32px"><a class="link-arrow" href="/reviews/"><span {L("All reviews")}>كل الآراء</span>{ic("arrow", "flip")}</a></p>
  </div>
</section>

<section class="sec sec--olive on-dark">
  <div class="wrap split">
    <div class="photo photo--port reveal">{img("real-sign", "لافتة كيرالي المضيئة عند مدخل المركز", "The illuminated Kairali sign at the entrance", style="object-position:50% 40%")}</div>
    <div class="stack-lg">
      <p class="eyebrow">Visit Us</p>
      {T("h2", "نحن بانتظارك", "We're waiting for you", "h2 reveal")}
      <ul class="info-list reveal">
        <li>{ic("pin")}<div><b {L("Location")}>الموقع</b><span>{ADDR} — <span {L("Kuwait")}>الكويت</span></span></div></li>
        <li>{ic("clock")}<div><b {L("Working Hours")}>ساعات العمل</b><span {L("Daily: 10:00 AM – 9:00 PM")}>يوميًا: 10:00 ص – 9:00 م</span></div></li>
        <li>{ic("phone")}<div><b {L("Phone / WhatsApp")}>الهاتف / واتساب</b><a href="tel:+96597706554" dir="ltr">{PHONE_DISPLAY}</a></div></li>
      </ul>
      <div style="display:flex;gap:14px;flex-wrap:wrap"><a class="btn btn--gold" href="/book/" {L("Book")}>الحجز</a><a class="btn btn--line-lt" href="{MAPS}" rel="noopener" target="_blank" {L("View on map")}>عرض على الخريطة</a></div>
    </div>
  </div>
</section>"""
    ld = {"@context": "https://schema.org", "@type": "DaySpa", "name": "Kairali Spa", "alternateName": ["كيرالي سبا", "Kairali Ayurvedic Centre"],
          "url": SITE, "telephone": "+96597706554", "image": SITE + "/assets/img/og-image.jpg", "priceRange": "KWD 10–40",
          "address": {"@type": "PostalAddress", "streetAddress": ADDR, "addressLocality": "Sabah Al-Salem", "addressCountry": "KW"},
          "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "10:00", "closes": "21:00"}],
          "sameAs": [IG]}
    page("/", "home", ("كيرالي سبا | Kairali Spa — عناية هندية أصيلة في الكويت", "Kairali Spa — Indian Wellness & Massage in Kuwait"),
         ("كيرالي سبا في الكويت: مساج هندي وجلسات أيورفيدا وعناية مستوحاة من التقاليد الهندية العريقة. احجزي جلستك أونلاين.",
          "Kairali Spa in Kuwait: Indian massage, Ayurvedic-inspired sessions and care rooted in long-standing Indian traditions. Book online."),
         body, hero=True, extra_head=f'<link rel="preload" as="image" href="/assets/img/hero-poster.webp">\n<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')

# ============================================================================ ABOUT
def about():
    chunks = [("لسنا مجرّد مركز مساج؛ نحن مساحة صغيرة صنعناها لتستعيدي فيها توازنك، بعيدًا عن ضجيج اليوم.",
               "We're not just another massage centre; we're a small space built so you can find your balance, away from the noise of the day."),
              ("الفكرة بدأت من إيمان بسيط: الجسم والعقل لا ينفصلان، وهو ما عرفته تقاليد العناية الهندية منذ آلاف السنين.",
               "The idea began with a simple belief: body and mind are never separate — something Indian care traditions have known for thousands of years."),
              ("نتعامل مع كل جلسة كأنها الأولى: بالاهتمام نفسه والدقة نفسها، لتكون كل تفصيلة مضبوطة لكِ أنتِ.",
               "We treat every session as if it were our first: the same care and precision, so every detail is right for you.")]
    chunk_html = "".join(f'<div class="chunk reveal" data-d="{i}" {L(e)}>{a}</div>' for i, (a, e) in enumerate(chunks, 1))
    items = [("01", "أصالة هندية", "Indian authenticity", "جلسات مستوحاة من تقاليد العناية الهندية العريقة.", "Sessions inspired by long-standing Indian care traditions."),
             ("02", "عناية بالتفاصيل", "Attention to detail", "من اختيار الزيوت إلى أجواء الجلسة، كل تفصيلة لها اهتمامها.", "From choosing the oils to the atmosphere of the session, every detail is cared for."),
             ("03", "خصوصية وراحة", "Privacy & comfort", "تجربة نسائية هادئة صُمّمت لتمنحك مساحتك الخاصة.", "A calm women's experience designed to give you your own space.")]
    nl = "".join(f'<li class="reveal" data-d="{i}"><span class="numlist__n">{n}</span><div>{T("h3", a, ae)}{T("p", b, be)}</div></li>' for i, (n, a, ae, b, be) in enumerate(items, 1))
    body = f"""
<section class="sec">
  <div class="wrap split split--55">
    <div class="stack-lg">
      <p class="eyebrow">The Kairali Story</p>
      {T("h1", "عناية هندية عريقة", "Timeless Indian Care", "h1 reveal")}
      {T("p", "في كيرالي سبا، نقدم تجربة عناية مستوحاة من تقاليد الهند العريقة، تجمع بين الزيوت الطبيعية، اللمسات المتخصصة والأجواء الهادئة؛ لنمنحك مساحة للراحة والاسترخاء بعيدًا عن إيقاع اليوم.",
           "At Kairali Spa, we offer a care experience inspired by India's long-standing traditions, combining natural oils, specialised touch and a calm atmosphere — to give you a space to rest and unwind, away from the rhythm of the day.", "lead reveal")}
      <div class="chunks">{chunk_html}</div>
    </div>
    <div class="photo photo--tall reveal">{img("real-robe", "ضيفة في رداء أبيض داخل غرفة العلاج بينما تجهّز المعالجة الزيوت", "A guest in a white robe inside the treatment room while the therapist prepares the oils", eager=True, style="object-position:60% 40%")}</div>
  </div>
</section>

<section class="quote-block reveal">
  <div class="photo">{img("st-herbs", "أعشاب مجففة معلّقة", "Dried herbs hanging to dry", style="object-position:50% 40%")}</div>
  <div class="quote-block__panel on-dark">{ic("quote", "quote-mark ic--fill")}
    <blockquote {L("From India... we took the roots of care, and at Kairali Spa we shaped a special experience around them.")}>«من الهند... أخذنا جذور العناية، وفي كيرالي سبا صنعنا لها تجربة خاصة.»</blockquote>
    <span class="gold-rule" style="background:var(--gold-lt)"></span>
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div class="stack-lg">
      <p class="eyebrow">Every Detail</p>
      {T("h2", "لأن الراحة تكمن في التفاصيل.", "Because comfort lives in the details.", "h2 reveal")}
      {T("p", "من لحظة وصولك إلى نهاية الجلسة، نصنع في كيرالي سبا تجربة هادئة تهتم بالتفاصيل.", "From the moment you arrive to the end of your session, Kairali Spa creates a calm experience that cares for every detail.", "lead reveal")}
      <ol class="numlist">{nl}</ol>
    </div>
    <div class="photo photo--tall reveal">{img("st-copper", "وعاء نحاسي وزيوت عشبية على طاولة العلاج", "A copper vessel and herbal oils on the treatment table", style="object-position:50% 50%")}</div>
  </div>
</section>

<section class="band reveal">
  {img("st-copper-still", "وعاء نحاسي وأعشاب طازجة على جدار وردي هادئ", "A copper vessel and fresh herbs against a calm rose wall")}
  <div class="wrap"><span class="gold-rule"></span>
    <p {L("From India's roots... we craft the Kairali Spa experience.")}>«من جذور الهند... نصنع تجربة كيرالي سبا.»</p></div>
</section>"""
    page("/about/", "about", ("من نحن | كيرالي سبا", "About Us | Kairali Spa"),
         ("عناية هندية عريقة: قصة كيرالي سبا وتجربة العناية المستوحاة من تقاليد الهند بالزيوت الطبيعية والأجواء الهادئة.",
          "Timeless Indian care: the story of Kairali Spa and a care experience inspired by India's traditions."), body)

# ============================================================================ SERVICES
def services():
    body = f"""
{page_head("Services", "كل المساجات والعلاجات", "All Massages & Treatments")}
<div class="page-banner reveal">{img("st-oils", "زجاجات زيوت عطرية بتلات ورد", "Aromatic oil bottles with flower petals", eager=True, style="object-position:50% 55%")}</div>
<section class="wrap sec--tight" style="padding-block:clamp(40px,6vw,72px)">
  <div class="recommender reveal">
    {T("h2", "لا تعرفين ماذا تختارين؟ أخبرينا بما تشعرين به", "Not sure what to choose? Tell us how you feel", "h3")}
    <div class="recommender__row">
      <input id="symptomInput" class="input" type="text" {LA("placeholder", "مثال: متعبة من العمل المكتبي ولدي شدّ في الرقبة", "e.g. tired from office work and my neck is tense")} {LA("aria-label", "صفي ما تشعرين به", "Describe how you feel")}>
      <button id="recBtn" class="btn btn--solid" type="button" {L("Recommend my session")}>اقترحي لي الجلسة الأنسب</button>
    </div>
    <div id="recOut" aria-live="polite"></div>
  </div>
  <div style="margin-top:44px">
    <div class="tabs" id="svcTabs" role="tablist">
      <button type="button" role="tab" data-cat="indian" aria-selected="true" {L("Indian Massages")}>مساجات هندية</button>
      <button type="button" role="tab" data-cat="other" aria-selected="false" {L("International Massages")}>مساجات عالمية</button>
    </div>
    <div class="svc-list" id="svcList"></div>
  </div>
</section>"""
    page("/services/", "services", ("خدماتنا | كيرالي سبا", "Services | Kairali Spa"),
         ("جميع مساجات كيرالي سبا وأسعارها: الأبيانغا، الشيرودهارا، الكيزهي، الأحجار الساخنة والمزيد. اختاري الجلسة الأنسب واحجزي أونلاين.",
          "All Kairali Spa massages and prices: Abhyanga, Shirodhara, Kizhi, hot stone and more. Find your session and book online."), body)

# ============================================================================ AYURVEDA
def ayurveda():
    d = [("wind", "Vata", "فاتا", "طاقة الحركة — ترتبط بالتنفس والدورة الدموية والجهاز العصبي", "The energy of movement — linked to breathing, blood circulation and the nervous system"),
         ("flame", "Pitta", "بيتا", "طاقة الحرارة — ترتبط بالهضم والتمثيل الغذائي والتحوّل", "The energy of heat — linked to digestion, metabolism and transformation"),
         ("mountain", "Kapha", "كافا", "طاقة البنية — تمنح الجسم ثباته وقوته ومقاومته", "The energy of structure — gives the body its stability and strength")]
    cards = "".join(f'<div class="dosha reveal" data-d="{i}">{ic(n)}<h3>{en} <small>{ar}</small></h3>{T("p", a, e)}</div>' for i, (n, en, ar, a, e) in enumerate(d, 1))
    body = f"""
{page_head("Our Philosophy", "ما هي الأيورفيدا؟", "What Is Ayurveda?")}
<section class="wrap" style="padding-bottom:clamp(56px,8vw,110px)">
  <div class="split split--55">
    <div class="stack-lg">
      {T("p", "الأيورفيدا (Ayurveda) نظام هندي عريق للعناية يزيد عمره على ثلاثة آلاف عام، ينظر إلى الجسم والعقل كوحدة واحدة مترابطة. وبدلًا من التركيز على عَرَض واحد، يبحث عن التوازن الشامل بين الجسم والطاقة والحواس.",
           "Ayurveda is a long-standing Indian system of care, over 3,000 years old, which sees the body and mind as one connected whole. Instead of focusing on a single symptom, it looks for complete balance between the body, energy and senses.", "lead reveal")}
      {T("p", "وفق هذه الفلسفة، يتكوّن جسم كل إنسان من مزيج من ثلاث «دوشات» (طاقات حيوية) بنسب مختلفة، وفهم هذا المزيج هو أساس أي جلسة مستوحاة من الأيورفيدا.",
           "According to this philosophy, every person's body is made of a mix of three “doshas” (vital energies) in different proportions, and understanding that mix is the basis of any Ayurveda-inspired session.", "lead reveal")}
    </div>
    <div class="photo photo--tall reveal">{img("st-mortar", "طحن الأعشاب بالهاون الحجري", "Grinding herbs with a stone mortar", eager=True, style="object-position:50% 50%")}</div>
  </div>
  <div class="doshas">{cards}</div>
  <div class="split" style="margin-top:clamp(48px,7vw,96px)">
    <div class="photo photo--wide reveal">{img("st-lamp", "مصباح نحاسي هندي تقليدي", "A traditional Indian brass lamp", style="object-position:50% 38%")}</div>
    <div class="stack-lg">
      {T("p", "في كيرالي سبا، جلساتنا (مثل الشيرودهارا والأبيانغا والكيزهي) مستوحاة من تقاليد العناية الهندية العريقة، وتعتمد على زيوت وأعشاب مختارة بعناية لتدعم هذا التوازن، لا مجرد استرخاء عابر.",
           "At Kairali Spa, our sessions (such as Shirodhara, Abhyanga and Kizhi) are inspired by long-standing Indian care traditions, using carefully chosen oils and herbs to support this balance — not just temporary relaxation.", "lead reveal")}
      <a class="btn btn--solid reveal" href="/services/" style="align-self:start" {L("Explore the sessions")}>استكشفي الجلسات</a>
    </div>
  </div>
</section>"""
    page("/ayurveda/", "ayurveda", ("عن الأيورفيدا | كيرالي سبا", "Ayurveda | Kairali Spa"),
         ("تعرّفي على فلسفة الأيورفيدا الهندية والدوشات الثلاث (فاتا وبيتا وكافا) وكيف تستلهمها جلسات كيرالي سبا.",
          "Discover the Indian philosophy of Ayurveda and the three doshas (Vata, Pitta, Kapha) that inspire Kairali Spa sessions."), body)

# ============================================================================ REVIEWS
def reviews():
    body = f"""
{page_head("Guest Reviews", "تجارب حقيقية من ضيوفنا", "Real Experiences From Our Guests")}
<section class="wrap" style="padding-bottom:clamp(56px,8vw,110px)">
  <div class="split" style="align-items:start">
    <div>
      <div class="rating-sum" id="revSum"></div>
      <div id="revList" style="display:grid;gap:18px" aria-live="polite"></div>
    </div>
    <form class="card form reveal" id="reviewForm" novalidate>
      {T("h2", "شاركينا تجربتك", "Share Your Experience", "h3")}
      <div class="field"><span class="label" {L("Your rating")}>تقييمك</span><div class="star-picker" id="starPicker" role="group" {LA("aria-label", "التقييم", "Rating")}></div></div>
      <div class="field"><label for="reviewName" {L("Your Name")}>الاسم</label><input class="input" id="reviewName" type="text" autocomplete="name" maxlength="80" {LA("placeholder", "مثال: هيا الفهد", "e.g. Sarah Ahmed")}></div>
      <div class="field"><label for="reviewText" {L("Your Experience With Us")}>تجربتك معنا</label><textarea class="textarea" id="reviewText" maxlength="1000" {LA("placeholder", "كيف كانت تجربتك في كيرالي؟", "How was your experience at Kairali?")}></textarea></div>
      <input class="hp" id="hpField" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
      <button class="btn btn--solid" type="submit" {L("Post Review")}>انشري رأيك</button>
      <p class="note" id="reviewMsg" role="status"></p>
      <p class="note" {L("Reviews appear after a quick check by our team.")}>تظهر الآراء بعد مراجعة سريعة من فريقنا.</p>
    </form>
  </div>
</section>"""
    page("/reviews/", "reviews", ("آراء العملاء | كيرالي سبا", "Guest Reviews | Kairali Spa"),
         ("اقرئي تجارب ضيوف كيرالي سبا الحقيقية وشاركينا رأيك.", "Read real Kairali Spa guest reviews and share your own."), body)

# ============================================================================ CONTACT
def contact():
    cards = [
        ("pin", "الموقع", "Location", f'<p>{ADDR}<br><span {L("Kuwait")}>الكويت</span></p>', f'href="{MAPS}" target="_blank" rel="noopener"'),
        ("phone", "الهاتف", "Phone", f'<p dir="ltr" style="text-align:start">{PHONE_DISPLAY}</p>', 'href="tel:+96597706554"'),
        ("insta", "انستجرام", "Instagram", '<p dir="ltr" style="text-align:start">@kairali_kw</p>', f'href="{IG}" target="_blank" rel="noopener"'),
        ("clock", "ساعات العمل", "Working Hours", f'<p {L("Daily: 10:00 AM – 9:00 PM")}>يوميًا: 10:00 ص – 9:00 م</p>', ""),
    ]
    ch = "".join(f'<{"a" if h else "div"} class="c-card reveal" data-d="{i % 2 + 1}" {h}>{ic(n)}{T("h3", a, e)}{p}</{"a" if h else "div"}>' for i, (n, a, e, p, h) in enumerate(cards))
    faq = "".join(f'<details class="reveal"><summary><span {L(q[1])}>{q[0]}</span>{ic("plus")}</summary><p {L(a[1])}>{a[0]}</p></details>' for q, a in FAQ)
    body = f"""
{page_head("Contact Us", "نحن بانتظارك", "We're Waiting For You")}
<section class="wrap" style="padding-bottom:clamp(40px,6vw,80px)">
  <div class="photo-pair">
    <div class="photo reveal">{img("real-reception", "مكتب الاستقبال في كيرالي سبا", "The Kairali Spa reception", eager=True, style="object-position:50% 34%")}</div>
    <div class="photo reveal" data-d="1">{img("real-sign", "لافتة كيرالي المضيئة", "The illuminated Kairali sign", eager=True, style="object-position:50% 40%")}</div>
  </div>
  <div class="contact-cards" style="margin-top:20px">{ch}</div>
  <div style="margin-top:28px;display:flex;gap:14px;flex-wrap:wrap"><a class="btn btn--solid" href="/book/" {L("Book")}>الحجز</a><a class="btn btn--line" href="{WA}" rel="noopener" target="_blank">{ic("wa")} WhatsApp</a></div>
</section>
<section class="sec sec--sand"><div class="wrap">
  <p class="eyebrow">Before You Book</p>
  {T("h2", "أسئلة شائعة", "Frequently Asked Questions", "h2 reveal")}
  <div class="faq" style="margin-top:36px">{faq}</div>
</div></section>"""
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q[0], "acceptedAnswer": {"@type": "Answer", "text": a[0]}} for q, a in FAQ]}
    page("/contact/", "contact", ("تواصل معنا | كيرالي سبا", "Contact | Kairali Spa"),
         ("عنوان كيرالي سبا في صباح السالم، الكويت، وساعات العمل وأرقام التواصل، مع إجابات على الأسئلة الشائعة.",
          "Kairali Spa address in Sabah Al-Salem, Kuwait, opening hours, contact details and answers to common questions."), body,
         extra_head=f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')

# ============================================================================ COMPLAINTS
def complaints():
    body = f"""
{page_head("We're Listening", "لديك ملاحظة أو شكوى؟", "Have a Complaint?", "أخبرينا بما حدث؛ نأخذ كل شكوى بجدية ونتواصل معك مباشرة.", "Tell us what happened — we take every complaint seriously and will follow up with you directly.")}
<section class="wrap" style="padding-bottom:clamp(56px,8vw,110px)"><form class="card form form--2 reveal" id="complaintForm" novalidate style="max-width:820px">
  <div class="field"><label for="complaintName" {L("Your Name")}>الاسم</label><input class="input" id="complaintName" type="text" autocomplete="name" maxlength="80" {LA("placeholder", "مثال: نورة العتيبي", "e.g. Sarah Ahmed")}></div>
  <div class="field"><label for="complaintPhone" {L("WhatsApp Number")}>رقم واتساب</label><input class="input" id="complaintPhone" type="tel" inputmode="tel" autocomplete="tel" maxlength="20" placeholder="+965 5xxx xxxx"></div>
  <div class="field full"><label for="complaintEmployee">{T("span", "اسم الموظفة", "Employee name")} <span class="opt" {L("(optional)")}>(اختياري)</span></label><input class="input" id="complaintEmployee" type="text" maxlength="80" {LA("placeholder", "إن كنتِ تعرفين اسمها", "If you know her name")}></div>
  <div class="field full"><label for="complaintText" {L("Your Complaint")}>الشكوى</label><textarea class="textarea" id="complaintText" maxlength="2000" {LA("placeholder", "اكتبي شكواك بالتفصيل هنا...", "Describe your complaint here...")}></textarea></div>
  <input class="hp" id="hpField" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
  <div class="full"><button class="btn btn--solid" type="submit" {L("Submit Complaint")}>إرسال الشكوى</button><p class="note" id="complaintMsg" role="status" style="margin-top:16px"></p></div>
</form></section>"""
    page("/complaints/", "complaints", ("الشكاوى | كيرالي سبا", "Complaints | Kairali Spa"),
         ("نصغي إلى ملاحظاتك. أرسلي شكواك إلى فريق كيرالي سبا وسنتواصل معك مباشرة.", "We're listening. Send your complaint to the Kairali Spa team and we'll follow up directly."), body, noindex=True)

# ============================================================================ BOOKING
def booking():
    body = f"""
<section class="wrap page-head" style="padding-bottom:20px">
  <p class="eyebrow">Book Your Session</p>
  {T("h1", "احجزي جلستك", "Book Your Session", "h1 reveal")}
  {T("p", "الخدمات مخصصة للنساء فقط. اختاري الجلسة والموعد، وسيصلنا حجزك فورًا.", "Our services are for women only. Choose your session and time — your booking reaches us instantly.", "lead reveal")}
</section>
<section class="wrap" style="padding-bottom:clamp(56px,8vw,110px)">
  <ol class="stepper" id="stepper" {LA("aria-label", "خطوات الحجز", "Booking steps")}>
    <li class="on"><i>1</i><span {L("Service")}>الخدمة</span></li><li><i>2</i><span {L("Date & Time")}>الموعد</span></li><li><i>3</i><span {L("Your Details")}>بياناتك</span></li>
  </ol>
  <div class="booking-grid">
    <div class="card" id="panel" style="scroll-margin-top:calc(var(--nav-h) + 16px)">
      <section id="step1">
        {T("h2", "اختاري جلستك", "Choose Your Session", "panel-title")}
        <div class="tabs" id="bookTabs" role="tablist" style="margin-bottom:22px">
          <button type="button" role="tab" data-cat="indian" aria-selected="true" {L("Indian Massages")}>مساجات هندية</button>
          <button type="button" role="tab" data-cat="other" aria-selected="false" {L("International Massages")}>مساجات عالمية</button>
        </div>
        <div class="pick" id="pickList"></div>
      </section>
      <section id="step2" hidden>
        {T("h2", "اليوم والوقت", "Date & Time", "panel-title")}
        <div class="chosen"><span id="chosen2"></span><button class="change" type="button" data-goto="1" {L("Change")}>تغيير</button></div>
        <div class="field" id="durField" style="margin-bottom:22px"><span class="label" {L("Duration")}>المدة</span><div class="dur-btns" id="durBtns"></div></div>
        <div class="field" style="margin-bottom:22px"><label for="dateInput" {L("Date")}>التاريخ</label><input class="input" id="dateInput" type="date"></div>
        <div class="field"><span class="label" {L("Available times")}>الأوقات المتاحة</span><div class="slots" id="slots"></div><p class="note" id="slotNote" role="status"></p></div>
        <div class="actions"><button class="btn btn--solid" id="to3" type="button" disabled {L("Continue")}>متابعة</button></div>
      </section>
      <section id="step3" hidden>
        {T("h2", "بياناتك", "Your Details", "panel-title")}
        <div class="chosen"><span id="chosen3"></span><button class="change" type="button" data-goto="2" {L("Change")}>تغيير</button></div>
        <div class="form">
          <div class="field"><label for="nameInput" {L("Name")}>الاسم</label><input class="input" id="nameInput" type="text" autocomplete="name" maxlength="80" {LA("placeholder", "مثال: نورة العتيبي", "e.g. Sarah Ahmed")}></div>
          <div class="field"><label for="phoneInput" {L("WhatsApp Number")}>رقم واتساب</label><input class="input" id="phoneInput" type="tel" inputmode="tel" autocomplete="tel" maxlength="20" placeholder="+965 5xxx xxxx"></div>
          <div class="field"><label for="emailInput">{T("span", "البريد الإلكتروني", "Email")} <span class="opt" {L("(optional)")}>(اختياري)</span></label><input class="input" id="emailInput" type="email" autocomplete="email" maxlength="120" placeholder="example@email.com"></div>
          <input class="hp" id="hpField" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">
          <p class="note note--err" id="bookErr" role="alert" hidden></p>
        </div>
        <div class="actions"><button class="btn btn--solid" id="confirmBtn" type="button" disabled {L("Confirm Booking")}>تأكيد الحجز</button></div>
      </section>
      <section id="stepDone" class="done" hidden>
        <div class="check">{ic("check")}</div>
        {T("h2", "تم تسجيل حجزك", "Your booking is registered", "panel-title")}
        {T("p", "سيتواصل معك فريقنا عبر واتساب لتأكيد التفاصيل.", "Our team will contact you on WhatsApp to confirm the details.", "lead")}
        <dl class="receipt" id="receipt"></dl>
        <p class="note" id="demoNote" hidden {L("Demo mode: nothing was sent to the system.")}>وضع تجريبي: لم يُرسل أي شيء إلى النظام.</p>
        <button class="btn btn--line" id="again" type="button" {L("Book another session")}>احجزي جلسة أخرى</button>
      </section>
    </div>
    <aside class="summary" id="summary" {LA("aria-label", "ملخص الحجز", "Booking summary")}>
      {T("h3", "ملخص الحجز", "Booking summary")}
      <dl id="sumList"></dl>
      <div style="display:flex;justify-content:space-between;align-items:baseline;margin-top:18px"><span {L("Total")} style="opacity:.75">الإجمالي</span><span class="total" id="sumTotal">—</span></div>
      <p style="font-size:.82rem;opacity:.7;margin-top:14px" {L("Cancel or reschedule at least 24 hours ahead via WhatsApp.")}>للإلغاء أو التأجيل يُرجى إبلاغنا قبل 24 ساعة عبر واتساب.</p>
    </aside>
  </div>
</section>"""
    page("/book/", "book", ("احجزي جلستك | كيرالي سبا", "Book Your Session | Kairali Spa"),
         ("احجزي جلسة مساج هندي في كيرالي سبا خلال دقيقة: اختاري الخدمة والموعد المتاح وأكّدي حجزك أونلاين.",
          "Book an Indian massage at Kairali Spa in under a minute: choose your service, an available time, and confirm online."), body, mbar=False)

# ============================================================================ PRIVACY
def privacy():
    body = f"""
{page_head("Privacy Policy", "سياسة الخصوصية", "Privacy Policy")}
<section class="wrap" style="padding-bottom:clamp(56px,8vw,110px)"><div class="prose">
  {T("p", "مسودة للمراجعة: يُرجى اعتماد النص النهائي من كيرالي سبا قبل الإطلاق.", "Draft for review: the final text must be approved by Kairali Spa before launch.", "note")}
  {T("h2", "البيانات التي نجمعها", "Data we collect")}
  {T("p", "عند الحجز نجمع الاسم ورقم واتساب والبريد الإلكتروني (اختياري) والخدمة والموعد. وعند إرسال رأي أو شكوى نجمع الاسم والرقم والنص الذي تكتبينه.", "When you book we collect your name, WhatsApp number, optional email, service and time. When you send a review or complaint we collect your name, number and the text you write.")}
  {T("h2", "كيف نستخدمها", "How we use it")}
  {T("p", "نستخدم بياناتك لإدارة الحجوزات والتواصل معك بشأنها ومعالجة الآراء والشكاوى. لا نبيع بياناتك لأي جهة.", "We use your data to manage bookings, contact you about them, and handle reviews and complaints. We do not sell your data.")}
  {T("h2", "ملفات تعريف الارتباط وقياس الإعلانات", "Cookies and ad measurement")}
  {T("p", "بموافقتك، نستخدم أدوات قياس من Meta وTikTok لفهم أداء إعلاناتنا. قد يُرسل إليها رقم هاتف مُشفّر (Hash) عند إتمام الحجز. يمكنك الرفض ولن تُحمَّل هذه الأدوات.", "With your consent we use Meta and TikTok measurement tools to understand how our ads perform. A hashed phone number may be sent to them when a booking is completed. If you decline, these tools are not loaded.")}
  {T("h2", "التواصل", "Contact")}
  {T("p", "لأي استفسار عن بياناتك راسلينا عبر واتساب على +965 9770 6554.", "For any question about your data, message us on WhatsApp at +965 9770 6554.")}
</div></section>"""
    page("/privacy/", "privacy", ("سياسة الخصوصية | كيرالي سبا", "Privacy Policy | Kairali Spa"), ("سياسة الخصوصية لموقع كيرالي سبا.", "Privacy policy for the Kairali Spa website."), body, noindex=True)

# ============================================================================ data + static files
def write_data():
    payload = {
        "services": [{"id": s["id"], "cat": s["cat"], "latin": s["latin"], "ar": s["ar"], "dur": [list(d) for d in s["dur"]],
                      "short": list(s["short"]), "what": list(s["what"]), "benefit": list(s["benefit"])} for s in SERVICES],
        "symptoms": SYMPTOMS, "str": {k: list(v) for k, v in STR.items()}}
    (ROOT / "assets/js/data.js").write_text("window.KAIRALI_DATA = " + json.dumps(payload, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")

def write_static():
    paths = ["/", "/about/", "/services/", "/ayurveda/", "/reviews/", "/contact/", "/book/"]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"  <url><loc>{SITE}{p}</loc></url>\n" for p in paths) + "</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /complaints/\nDisallow: /privacy/\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    (ROOT / "favicon.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><rect width="48" height="48" rx="10" fill="#2A3318"/><g fill="none" stroke="#D6BC81" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M24 9c3.4 3.6 5 7 5 10.5S27 26 24 28c-3-2-5-5-5-8.5S20.6 12.6 24 9Z"/><path d="M24 28c-5.2 0-10.6-2.6-13.4-8 4-.7 7.8.6 10.6 3.3"/><path d="M24 28c5.2 0 10.6-2.6 13.4-8-4-.7-7.8.6-10.6 3.3"/><path d="M15 35h18"/></g></svg>\n', encoding="utf-8")
    (ROOT / "vercel.json").write_text(json.dumps({
        "cleanUrls": True, "trailingSlash": True,
        "headers": [
            {"source": "/assets/(img|video)/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=2592000"}]},
            {"source": "/assets/(css|js)/(.*)", "headers": [{"key": "Cache-Control", "value": "public, max-age=3600, must-revalidate"}]},
            {"source": "/(.*)", "headers": [{"key": "X-Content-Type-Options", "value": "nosniff"}, {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"}, {"key": "X-Frame-Options", "value": "SAMEORIGIN"}]}]}, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    write_data(); write_static()
    home(); about(); services(); ayurveda(); reviews(); contact(); complaints(); booking(); privacy()
    print("built:", ", ".join(sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob("index.html"))))
