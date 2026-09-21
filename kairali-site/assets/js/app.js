/* Kairali Spa — front-end behaviour.
   Static pages carry the Arabic text; English lives in data-en attributes and is swapped here.
   All user-supplied strings are written with textContent (never innerHTML). */
(function () {
  'use strict';
  var C = window.KAIRALI_CONFIG || {};
  var D = window.KAIRALI_DATA || { services: [], symptoms: {}, str: {} };
  var IS_LOCAL = /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname) || location.protocol === 'file:';
  var PAGE = document.body.getAttribute('data-page') || '';

  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var store = function (k, v) {
    try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; }
  };
  var el = function (tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  };
  var icon = function (id, cls) {
    var s = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    s.setAttribute('class', 'ic' + (cls ? ' ' + cls : ''));
    s.setAttribute('aria-hidden', 'true');
    var u = document.createElementNS('http://www.w3.org/2000/svg', 'use');
    u.setAttribute('href', '#i-' + id);
    s.appendChild(u);
    return s;
  };

  /* ------------------------------------------------------------------ language */
  var lang = store('kairali_lang') === 'en' ? 'en' : 'ar';
  var langHooks = [];
  var S = function (key) { var v = D.str[key]; return v ? (lang === 'en' ? v[1] : v[0]) : key; };
  var tr = function (pair) { return lang === 'en' ? pair[1] : pair[0]; };
  var ATTRS = ['placeholder', 'aria-label', 'alt', 'title', 'content'];

  function applyLang() {
    var root = document.documentElement;
    root.lang = lang; root.dir = lang === 'ar' ? 'rtl' : 'ltr';
    $$('[data-en]').forEach(function (n) {
      if (n.getAttribute('data-ar') === null) n.setAttribute('data-ar', n.innerHTML);
      n.innerHTML = lang === 'en' ? n.getAttribute('data-en') : n.getAttribute('data-ar');
    });
    ATTRS.forEach(function (a) {
      $$('[data-en-' + a + ']').forEach(function (n) {
        if (n.getAttribute('data-ar-' + a) === null) n.setAttribute('data-ar-' + a, n.getAttribute(a) || '');
        n.setAttribute(a, lang === 'en' ? n.getAttribute('data-en-' + a) : n.getAttribute('data-ar-' + a));
      });
    });
    if (root.getAttribute('data-title-en')) {
      if (root.getAttribute('data-title-ar') === null) root.setAttribute('data-title-ar', document.title);
      document.title = lang === 'en' ? root.getAttribute('data-title-en') : root.getAttribute('data-title-ar');
    }
    $$('.lang-btn').forEach(function (b) { b.textContent = lang === 'ar' ? 'EN' : 'عربي'; b.setAttribute('aria-label', lang === 'ar' ? 'Switch to English' : 'التبديل إلى العربية'); });
    langHooks.forEach(function (fn) { fn(); });
  }
  function setLang(l) { lang = l; store('kairali_lang', l); applyLang(); }
  $$('.lang-btn').forEach(function (b) { b.addEventListener('click', function () { setLang(lang === 'ar' ? 'en' : 'ar'); }); });

  /* ---------------------------------------------------------------- navigation */
  var nav = $('.nav');
  var hasHero = !!$('.hero');
  function onScroll() {
    if (nav && hasHero) nav.classList.toggle('solid', window.scrollY > 40);
    var mbar = $('.mbar');
    if (mbar) mbar.classList.toggle('show', window.scrollY > (hasHero ? 420 : 120));
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  var drawer = $('.drawer');
  function setDrawer(open) {
    if (!drawer) return;
    drawer.classList.toggle('open', open);
    document.body.style.overflow = open ? 'hidden' : '';
    var b = $('.burger'); if (b) b.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) { var c = $('.drawer__close'); if (c) c.focus(); }
  }
  var burger = $('.burger'); if (burger) burger.addEventListener('click', function () { setDrawer(true); });
  $$('.drawer__close, .drawer a').forEach(function (n) { n.addEventListener('click', function () { setDrawer(false); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setDrawer(false); });

  var here = location.pathname.replace(/index\.html$/, '').replace(/\/+$/, '') || '/';
  $$('.nav__links a, .drawer__links a').forEach(function (a) {
    var p = a.getAttribute('href').replace(/\/+$/, '') || '/';
    if (p === here) a.setAttribute('aria-current', 'page');
  });

  /* ------------------------------------------------------------------- reveal */
  document.documentElement.classList.add('js');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0, rootMargin: '0px 0px -8% 0px' });
    $$('.reveal').forEach(function (n) { io.observe(n); });
  } else { $$('.reveal').forEach(function (n) { n.classList.add('in'); }); }

  var vid = $('.hero video');
  if (vid && window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) { vid.removeAttribute('autoplay'); vid.pause(); }

  /* ------------------------------------------------------------------ tracking */
  var pixelsLoaded = false;
  function loadPixels() {
    if (IS_LOCAL || pixelsLoaded) return; pixelsLoaded = true;
    /* Meta Pixel */
    !function (f, b, e, v, n, t, s) { if (f.fbq) return; n = f.fbq = function () { n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); }; if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0'; n.queue = []; t = b.createElement(e); t.async = !0; t.src = v; s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s); }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
    window.fbq('init', C.metaPixelId); window.fbq('track', 'PageView');
    /* TikTok Pixel */
    !function (w, d, t) { w.TiktokAnalyticsObject = t; var ttq = w[t] = w[t] || []; ttq.methods = ['page', 'track', 'identify', 'instances', 'debug', 'on', 'off', 'once', 'ready', 'alias', 'group', 'enableCookie', 'disableCookie']; ttq.setAndDefer = function (t, e) { t[e] = function () { t.push([e].concat(Array.prototype.slice.call(arguments, 0))); }; }; for (var i = 0; i < ttq.methods.length; i++) ttq.setAndDefer(ttq, ttq.methods[i]); ttq.instance = function (t) { for (var e = ttq._i[t] || [], n = 0; n < ttq.methods.length; n++) ttq.setAndDefer(e, ttq.methods[n]); return e; }; ttq.load = function (e, n) { var r = 'https://analytics.tiktok.com/i18n/pixel/events.js'; ttq._i = ttq._i || {}; ttq._i[e] = []; ttq._i[e]._u = r; ttq._t = ttq._t || {}; ttq._t[e] = +new Date(); ttq._o = ttq._o || {}; ttq._o[e] = n || {}; var s = document.createElement('script'); s.type = 'text/javascript'; s.async = !0; s.src = r + '?sdkid=' + e + '&lib=' + t; var x = document.getElementsByTagName('script')[0]; x.parentNode.insertBefore(s, x); }; ttq.load(C.tiktokPixelId); ttq.page(); }(window, document, 'ttq');
  }
  function trackBooking(svc, price, eventId) {
    if (!pixelsLoaded) return;
    try { window.fbq('trackCustom', 'BookingConfirmed', { service: svc.latin, value: price, currency: 'KWD' }, { eventID: eventId }); } catch (e) {}
    try { window.ttq.track('SubmitForm', { contents: [{ content_id: svc.id, content_type: 'product', content_name: svc.latin }], value: price, currency: 'KWD' }, { event_id: eventId }); } catch (e) {}
  }
  (function consent() {
    var choice = store('kairali_consent');
    if (choice === 'yes') { loadPixels(); return; }
    if (choice === 'no') return;
    var box = $('#consent'); if (!box) return;
    box.hidden = false;
    $('[data-consent="yes"]', box).addEventListener('click', function () { store('kairali_consent', 'yes'); box.hidden = true; loadPixels(); });
    $('[data-consent="no"]', box).addEventListener('click', function () { store('kairali_consent', 'no'); box.hidden = true; });
  })();

  /* ------------------------------------------------------------------ backend */
  function sb(path, opts) {
    opts = opts || {};
    var h = { apikey: C.supabaseAnonKey, Authorization: 'Bearer ' + C.supabaseAnonKey };
    for (var k in (opts.headers || {})) h[k] = opts.headers[k];
    return fetch(C.supabaseUrl + '/rest/v1/' + path, { method: opts.method || 'GET', headers: h, body: opts.body });
  }
  function notify(type, record) {
    if (IS_LOCAL) { console.info('[demo mode] notify', type, record); return Promise.resolve(); }
    return fetch(C.appsScriptUrl, { method: 'POST', mode: 'no-cors', body: JSON.stringify({ type: type, record: record }) });
  }
  function insertRow(table, row) {
    if (IS_LOCAL) { console.info('[demo mode] insert', table, row); return Promise.resolve(); }
    return sb(table, { method: 'POST', headers: { 'Content-Type': 'application/json', Prefer: 'return=minimal' }, body: JSON.stringify(row) })
      .then(function (r) { if (!r.ok) throw new Error(table + ' insert failed: ' + r.status); });
  }

  /* -------------------------------------------------------------------- helpers */
  var svcById = {}; D.services.forEach(function (s) { svcById[s.id] = s; });
  var svcName = function (s) { return lang === 'en' ? s.latin : s.ar; };
  var minPrice = function (s) { return Math.min.apply(null, s.dur.map(function (d) { return d[1]; })); };
  var money = function (n) { return n + ' ' + S('kwd'); };
  var dur = function (m) { return m + ' ' + S('minutes'); };
  function fmtTime(mins) {
    var h = Math.floor(mins / 60), m = mins % 60, ap = h >= 12 ? S('pm') : S('am');
    var h12 = h % 12 === 0 ? 12 : h % 12;
    return h12 + ':' + (m < 10 ? '0' : '') + m + ' ' + ap;
  }
  function kwNow() {
    var f = new Intl.DateTimeFormat('en-CA', { timeZone: C.timezone, year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' });
    var p = {}; f.formatToParts(new Date()).forEach(function (x) { p[x.type] = x.value; });
    return { date: p.year + '-' + p.month + '-' + p.day, min: (+p.hour) * 60 + (+p.minute) };
  }
  function addDays(iso, n) { var d = new Date(iso + 'T00:00:00Z'); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); }
  function fmtDate(iso) {
    var p = iso.slice(0, 10).split('-'); var names = D.str.monthNames[lang === 'en' ? 1 : 0];
    return +p[2] + ' ' + names[+p[1] - 1] + ' ' + p[0];
  }
  function stars(n, total) {
    var w = el('span', 'stars'); w.setAttribute('role', 'img'); w.setAttribute('aria-label', n + '/5');
    for (var i = 1; i <= (total || 5); i++) { var s = icon('star', i > n ? 'off' : ''); w.appendChild(s); }
    return w;
  }

  /* ------------------------------------------------------------ service rows */
  function renderSvcRow(s, idx, opts) {
    opts = opts || {};
    var row = el('article', 'svc' + (opts.badge ? ' is-rec' : '')); row.id = (opts.badge ? 'rec-' : 'svc-') + s.id;
    row.appendChild(el('div', 'svc__n', String(idx + 1).padStart(2, '0')));
    var body = el('div', 'svc__body');
    if (opts.badge) body.appendChild(el('span', 'rec-badge', S('recBadge')));
    body.appendChild(el('div', 'svc__latin', lang === 'en' ? S(s.cat === 'indian' ? 'indianCat' : 'otherCat') : s.latin));
    body.appendChild(el('h3', 'svc__name', svcName(s)));
    body.appendChild(el('p', 'svc__short', tr(s.short)));
    var det = el('details'); var sum = el('summary'); sum.appendChild(icon('plus')); sum.appendChild(el('span', '', S('detailsLabel'))); det.appendChild(sum);
    var more = el('div', 'svc__more');
    var a = el('div'); a.appendChild(el('b', '', S('whatHappensLabel'))); a.appendChild(el('span', '', tr(s.what))); more.appendChild(a);
    var b = el('div'); b.appendChild(el('b', '', S('benefitLabel'))); b.appendChild(el('span', '', tr(s.benefit))); more.appendChild(b);
    det.appendChild(more); body.appendChild(det); row.appendChild(body);
    var side = el('div', 'svc__side'); var prices = el('div', 'prices');
    s.dur.forEach(function (d) { var c = el('span', 'chip'); c.appendChild(document.createTextNode(dur(d[0]) + ' · ')); c.appendChild(el('b', '', String(d[1]))); c.appendChild(document.createTextNode(' ' + S('kwd'))); prices.appendChild(c); });
    side.appendChild(prices);
    var book = el('a', 'btn btn--solid', S('bookBtn')); book.href = '/book/?s=' + s.id; side.appendChild(book);
    row.appendChild(side);
    return row;
  }

  /* -------------------------------------------------------------- services page */
  function initServices() {
    var list = $('#svcList'); if (!list) return;
    var cat = 'indian';
    var tabs = $$('#svcTabs button');
    function render() {
      tabs.forEach(function (t) { t.setAttribute('aria-selected', t.getAttribute('data-cat') === cat ? 'true' : 'false'); });
      list.textContent = '';
      D.services.filter(function (s) { return s.cat === cat; }).forEach(function (s, i) { list.appendChild(renderSvcRow(s, i)); });
    }
    tabs.forEach(function (t) { t.addEventListener('click', function () { cat = t.getAttribute('data-cat'); render(); }); });
    var m = /^#svc-(\w+)/.exec(location.hash);
    if (m && svcById[m[1]]) cat = svcById[m[1]].cat;
    render(); langHooks.push(function () { render(); recRender(); });
    if (m) { var t = $('#svc-' + m[1]); if (t) { var d = $('details', t); if (d) d.open = true; setTimeout(function () { t.scrollIntoView({ behavior: 'smooth', block: 'center' }); }, 250); } }

    /* recommender */
    var input = $('#symptomInput'), out = $('#recOut'), lastMatches = null;
    var norm = function (t) { return t.toLowerCase().replace(/[ً-ٟ]/g, '').replace(/[إأآ]/g, 'ا').replace(/ى/g, 'ي').replace(/ة/g, 'ه'); };
    var tags = {}; Object.keys(D.symptoms).forEach(function (id) { tags[id] = D.symptoms[id].split('،').map(function (k) { return norm(k.trim()); }).filter(Boolean); });
    function recRender() {
      out.textContent = '';
      if (lastMatches === null) return;
      if (lastMatches === 'short') { out.appendChild(el('p', 'note note--err', S('recShort'))); return; }
      if (!lastMatches.length) { out.appendChild(el('p', 'note', S('recFallback'))); return; }
      lastMatches.forEach(function (id, i) { out.appendChild(renderSvcRow(svcById[id], i, { badge: true })); });
    }
    function recommend() {
      var text = norm(input.value.trim());
      if (text.length < 3) { lastMatches = 'short'; recRender(); return; }
      var scored = Object.keys(tags).map(function (id) { var sc = 0; tags[id].forEach(function (k) { if (text.indexOf(k) > -1) sc++; }); return { id: id, sc: sc }; })
        .filter(function (x) { return x.sc > 0; }).sort(function (a, b) { return b.sc - a.sc; }).slice(0, 3);
      lastMatches = scored.map(function (x) { return x.id; }); recRender();
      if (lastMatches.length) out.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
    $('#recBtn').addEventListener('click', recommend);
    input.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); recommend(); } });
  }

  /* ----------------------------------------------------------------- booking */
  function initBooking() {
    var panel = $('#panel'); if (!panel) return;
    var st = { step: 1, cat: 'indian', svc: null, dur: null, price: null, date: '', time: null, booked: [], reqId: 0 };
    var steps = { 1: $('#step1'), 2: $('#step2'), 3: $('#step3'), done: $('#stepDone') };
    var pickList = $('#pickList'), durBtns = $('#durBtns'), dateInput = $('#dateInput'), slotsEl = $('#slots'), slotNote = $('#slotNote');
    var to3 = $('#to3'), confirmBtn = $('#confirmBtn'), errEl = $('#bookErr');
    var nameI = $('#nameInput'), phoneI = $('#phoneInput'), emailI = $('#emailInput'), hp = $('#hpField');
    var now = kwNow();
    dateInput.min = now.date; dateInput.max = addDays(now.date, C.bookingWindowDays); dateInput.value = now.date; st.date = now.date;

    function goStep(n) {
      st.step = n;
      Object.keys(steps).forEach(function (k) { steps[k].hidden = String(k) !== String(n); });
      $$('#stepper li').forEach(function (li, i) { var k = i + 1; li.className = n === 'done' || k < n ? 'done' : (k === n ? 'on' : ''); if (k === n) li.setAttribute('aria-current', 'step'); else li.removeAttribute('aria-current'); });
      $('#summary').hidden = n === 'done';
      if (n !== 1) panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
      renderSummary();
    }
    function renderSummary() {
      var dl = $('#sumList'); dl.textContent = '';
      var rows = [];
      rows.push([S('receiptService'), st.svc ? svcName(st.svc) : '—']);
      rows.push([S('receiptDuration'), st.dur ? dur(st.dur) : '—']);
      rows.push([S('receiptDate'), st.date ? fmtDate(st.date) : '—']);
      rows.push([S('receiptTime'), st.time != null ? fmtTime(st.time) : '—']);
      rows.forEach(function (r) { var d = el('div'); d.appendChild(el('dt', '', r[0])); d.appendChild(el('dd', '', r[1])); dl.appendChild(d); });
      $('#sumTotal').textContent = st.price != null ? money(st.price) : '—';
    }

    /* step 1 */
    function renderPick() {
      $$('#bookTabs button').forEach(function (t) { t.setAttribute('aria-selected', t.getAttribute('data-cat') === st.cat ? 'true' : 'false'); });
      pickList.textContent = '';
      D.services.filter(function (s) { return s.cat === st.cat; }).forEach(function (s) {
        var it = el('div', 'pick-item'); it.appendChild(el('h4', '', svcName(s))); it.appendChild(el('p', '', tr(s.short)));
        var bt = el('div', 'dur-btns');
        s.dur.forEach(function (d) {
          var b = el('button', 'dur-btn'); b.type = 'button'; b.appendChild(document.createTextNode(dur(d[0]))); b.appendChild(el('b', '', d[1] + ' ' + S('kwd')));
          b.addEventListener('click', function () { chooseService(s, d[0]); goStep(2); });
          bt.appendChild(b);
        });
        it.appendChild(bt); pickList.appendChild(it);
      });
    }
    $$('#bookTabs button').forEach(function (t) { t.addEventListener('click', function () { st.cat = t.getAttribute('data-cat'); renderPick(); }); });
    function chooseService(s, d) {
      st.svc = s; st.dur = d; st.price = s.dur.filter(function (x) { return x[0] === d; })[0][1]; st.time = null;
      renderStep2(); loadSlots();
    }

    /* step 2 */
    function renderStep2() {
      if (!st.svc) return;
      $('#chosen2').textContent = svcName(st.svc) + ' · ' + dur(st.dur) + ' · ' + money(st.price);
      durBtns.textContent = '';
      st.svc.dur.forEach(function (d) {
        var b = el('button', 'dur-btn'); b.type = 'button'; b.setAttribute('aria-pressed', d[0] === st.dur ? 'true' : 'false');
        b.appendChild(document.createTextNode(dur(d[0]))); b.appendChild(el('b', '', d[1] + ' ' + S('kwd')));
        b.addEventListener('click', function () { chooseService(st.svc, d[0]); });
        durBtns.appendChild(b);
      });
      $('#durField').hidden = st.svc.dur.length < 2;
      renderSlots(); renderSummary();
    }
    function overlap(a, ad, b, bd) { return a < b + bd && b < a + ad; }
    function loadSlots() {
      if (!st.svc) return;
      var id = ++st.reqId; st.loading = true; st.error = false; renderSlots();
      sb('booking_slots?booking_date=eq.' + st.date + '&select=booking_time,duration').then(function (r) {
        if (!r.ok) throw new Error(r.status); return r.json();
      }).then(function (rows) {
        if (id !== st.reqId) return;
        st.booked = rows.map(function (x) { var p = String(x.booking_time).split(':'); return { s: (+p[0]) * 60 + (+p[1]), d: +x.duration }; });
        st.loading = false; renderSlots();
      }).catch(function () { if (id !== st.reqId) return; st.loading = false; st.error = true; st.booked = []; renderSlots(); });
    }
    function slotList() {
      var out = [], open = C.openHour * 60, close = C.closeHour * 60, n = kwNow();
      for (var t = open; t + st.dur <= close; t += C.slotStepMin) {
        if (st.date === n.date && t <= n.min + C.leadMinutes) continue;
        var taken = st.booked.some(function (b) { return overlap(t, st.dur, b.s, b.d); });
        out.push({ t: t, taken: taken });
      }
      return out;
    }
    function renderSlots() {
      slotsEl.textContent = ''; slotNote.textContent = ''; slotNote.className = 'note';
      if (st.time != null && !st.loading && !slotList().some(function (s) { return s.t === st.time && !s.taken; })) st.time = null;
      if (st.loading) { slotNote.textContent = S('slotsLoading'); }
      else if (st.error) { slotNote.textContent = S('slotsError'); slotNote.className = 'note note--err'; }
      else {
        var list = slotList();
        if (!list.some(function (s) { return !s.taken; })) slotNote.textContent = S('noSlots');
        else slotNote.textContent = S('slotNote');
        list.forEach(function (s) {
          var b = el('button', 'slot', fmtTime(s.t)); b.type = 'button'; b.disabled = s.taken; b.setAttribute('aria-pressed', st.time === s.t ? 'true' : 'false');
          b.addEventListener('click', function () { st.time = s.t; renderSlots(); });
          slotsEl.appendChild(b);
        });
      }
      to3.disabled = st.time == null; renderSummary(); validate();
    }
    dateInput.addEventListener('change', function () {
      var v = dateInput.value; if (!v || v < dateInput.min) v = dateInput.min; if (v > dateInput.max) v = dateInput.max;
      dateInput.value = v; st.date = v; st.time = null; loadSlots();
    });
    to3.addEventListener('click', function () { $('#chosen3').textContent = svcName(st.svc) + ' · ' + dur(st.dur) + ' · ' + fmtDate(st.date) + ' · ' + fmtTime(st.time); goStep(3); });
    $$('[data-goto]').forEach(function (b) { b.addEventListener('click', function () { goStep(+b.getAttribute('data-goto')); }); });

    /* step 3 */
    phoneI.addEventListener('input', function () { phoneI.value = phoneI.value.replace(/[^\d+]/g, ''); validate(); });
    [nameI, emailI].forEach(function (i) { i.addEventListener('input', validate); });
    function validate() {
      confirmBtn.disabled = !(nameI.value.trim().length >= 2 && phoneI.value.replace(/\D/g, '').length >= 7 && st.time != null);
    }
    confirmBtn.addEventListener('click', async function () {
      errEl.hidden = true; errEl.textContent = ''; confirmBtn.disabled = true; var label = confirmBtn.textContent; confirmBtn.textContent = S('sending');
      var reset = function () { confirmBtn.textContent = label; validate(); };
      try {
        var r = await sb('booking_slots?booking_date=eq.' + st.date + '&select=booking_time,duration');
        if (!r.ok) throw new Error('slots ' + r.status);
        var rows = await r.json();
        var clash = rows.some(function (x) { var p = String(x.booking_time).split(':'); return overlap(st.time, st.dur, (+p[0]) * 60 + (+p[1]), +x.duration); });
        if (clash) { st.booked = rows.map(function (x) { var p = String(x.booking_time).split(':'); return { s: (+p[0]) * 60 + (+p[1]), d: +x.duration }; }); st.time = null; renderSlots(); goStep(2); slotNote.textContent = S('conflictAlert'); slotNote.className = 'note note--err'; reset(); return; }
        var hh = String(Math.floor(st.time / 60)).padStart(2, '0'), mm = String(st.time % 60).padStart(2, '0');
        var row = { name: nameI.value.trim(), phone: phoneI.value.trim(), email: emailI.value.trim() || null, service: st.svc.latin, duration: st.dur, price: st.price, booking_date: st.date, booking_time: hh + ':' + mm };
        if (!hp.value) {
          await insertRow('bookings', row);
          var eventId = 'bk_' + Date.now() + '_' + Math.random().toString(36).slice(2, 8);
          notify('booking', Object.assign({}, row, { email: row.email || '', event_id: eventId })).catch(function () {});
          trackBooking(st.svc, st.price, eventId);
        }
        showDone(row); reset();
      } catch (e) {
        console.error(e); errEl.textContent = S('connError'); errEl.hidden = false; reset();
      }
    });
    function showDone(row) {
      var rc = $('#receipt'); rc.textContent = '';
      [[S('receiptService'), svcName(st.svc)], [S('receiptDuration'), dur(st.dur)], [S('receiptDate'), fmtDate(st.date)], [S('receiptTime'), fmtTime(st.time)], [S('receiptPrice'), money(st.price)], [S('receiptName'), row.name]].forEach(function (r) {
        var d = el('div'); d.appendChild(el('dt', '', r[0])); d.appendChild(el('dd', '', r[1])); rc.appendChild(d);
      });
      $('#demoNote').hidden = !IS_LOCAL; goStep('done');
    }
    $('#again').addEventListener('click', function () {
      st.svc = null; st.dur = null; st.price = null; st.time = null; nameI.value = ''; phoneI.value = ''; emailI.value = ''; renderPick(); goStep(1);
    });

    langHooks.push(function () { renderPick(); renderStep2(); renderSummary(); if (st.step === 3) $('#chosen3').textContent = svcName(st.svc) + ' · ' + dur(st.dur) + ' · ' + fmtDate(st.date) + ' · ' + fmtTime(st.time); });
    renderPick(); renderSummary();
    var q = new URLSearchParams(location.search), qs = q.get('s'), qd = +q.get('d');
    if (qs && svcById[qs]) {
      var s = svcById[qs], d = s.dur.some(function (x) { return x[0] === qd; }) ? qd : s.dur[0][0];
      st.cat = s.cat; renderPick(); chooseService(s, d); goStep(2);
    }
    validate();
  }

  /* ------------------------------------------------------------------ reviews */
  function fetchReviews(limitQ) {
    return sb('reviews?approved=eq.true&select=name,rating,comment,created_at&order=' + (limitQ ? 'rating.desc,created_at.desc&limit=3' : 'created_at.desc')).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); });
  }
  function reviewCard(r) {
    var c = el('article', 'review'); c.appendChild(stars(r.rating)); c.appendChild(el('p', '', r.comment));
    var by = el('div', 'review__by'); by.appendChild(el('span', '', r.name)); by.appendChild(el('span', '', fmtDate(r.created_at))); c.appendChild(by); return c;
  }
  function countText(n) {
    if (lang === 'en') return n + ' ' + (n === 1 ? 'review' : 'reviews');
    if (n === 1) return 'رأي واحد';
    if (n === 2) return 'رأيين';
    return n + (n <= 10 ? ' آراء' : ' رأيًا');
  }
  function initReviewsPage() {
    var list = $('#revList'); if (!list) return;
    var rating = 0, data = null, picker = $('#starPicker');
    for (var i = 1; i <= 5; i++) (function (n) {
      var b = el('button'); b.type = 'button'; b.setAttribute('aria-label', n + '/5'); b.appendChild(icon('star'));
      b.addEventListener('click', function () { rating = n; paint(); }); picker.appendChild(b);
    })(i);
    function paint() { $$('button', picker).forEach(function (b, i) { b.classList.toggle('on', i < rating); b.setAttribute('aria-pressed', i < rating ? 'true' : 'false'); }); }
    function render() {
      list.textContent = ''; var sum = $('#revSum'); sum.textContent = '';
      if (!data || !data.length) { list.appendChild(el('div', 'empty', S('reviewsEmpty'))); return; }
      var avg = data.reduce(function (a, r) { return a + r.rating; }, 0) / data.length;
      sum.appendChild(el('span', 'rating-sum__n', avg.toFixed(1)));
      var col = el('div'); col.appendChild(stars(Math.round(avg)));
      col.appendChild(el('p', 'note', S('basedOn') + ' ' + countText(data.length))); sum.appendChild(col);
      data.forEach(function (r) { list.appendChild(reviewCard(r)); });
    }
    fetchReviews(false).then(function (d) { data = d; render(); }).catch(function () { data = []; render(); });
    langHooks.push(render);
    var form = $('#reviewForm'), msg = $('#reviewMsg');
    form.addEventListener('submit', async function (e) {
      e.preventDefault(); msg.className = 'note'; msg.textContent = '';
      var name = $('#reviewName').value.trim(), text = $('#reviewText').value.trim();
      if (!rating || name.length < 2 || text.length < 4) { msg.className = 'note note--err'; msg.textContent = S('reviewInvalid'); return; }
      if ($('#hpField').value) { msg.textContent = S('reviewThanks'); return; }
      var btn = $('button[type=submit]', form); btn.disabled = true;
      try {
        await insertRow('reviews', { name: name, rating: rating, comment: text });
        notify('review', { name: name, rating: rating, comment: text }).catch(function () {});
        form.reset(); rating = 0; paint(); msg.className = 'note note--ok'; msg.textContent = S('reviewThanks') + (IS_LOCAL ? ' — ' + S('demoNote') : '');
      } catch (err) { console.error(err); msg.className = 'note note--err'; msg.textContent = S('connError'); }
      btn.disabled = false;
    });
  }
  function initHomeReviews() {
    var sec = $('#homeReviews'); if (!sec) return;
    fetchReviews(true).then(function (d) {
      if (!d.length) return;
      var g = $('#homeRevGrid'); d.forEach(function (r) { g.appendChild(reviewCard(r)); }); sec.hidden = false;
    }).catch(function () {});
  }

  /* --------------------------------------------------------------- complaints */
  function initComplaints() {
    var form = $('#complaintForm'); if (!form) return;
    var msg = $('#complaintMsg'), phone = $('#complaintPhone');
    phone.addEventListener('input', function () { phone.value = phone.value.replace(/[^\d+]/g, ''); });
    form.addEventListener('submit', async function (e) {
      e.preventDefault(); msg.className = 'note'; msg.textContent = '';
      var rec = { name: $('#complaintName').value.trim(), phone: phone.value.trim(), employee: $('#complaintEmployee').value.trim(), message: $('#complaintText').value.trim() };
      if (rec.name.length < 2 || rec.phone.replace(/\D/g, '').length < 7 || rec.message.length < 4) { msg.className = 'note note--err'; msg.textContent = S('complaintInvalid'); return; }
      if ($('#hpField').value) { msg.textContent = S('complaintThanks'); return; }
      var btn = $('button[type=submit]', form); btn.disabled = true;
      try { await notify('complaint', rec); form.reset(); msg.className = 'note note--ok'; msg.textContent = S('complaintThanks') + (IS_LOCAL ? ' — ' + S('demoNote') : ''); }
      catch (err) { console.error(err); msg.className = 'note note--err'; msg.textContent = S('connError'); }
      btn.disabled = false;
    });
  }

  /* --------------------------------------------------------------------- boot */
  applyLang();
  initServices(); initBooking(); initReviewsPage(); initHomeReviews(); initComplaints();
})();
