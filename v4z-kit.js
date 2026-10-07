/* V4Z Mini App Kit v1 — এক লাইনে Mini App-এ প্যানেল-config, join-gate, key-gate আর অ্যাড।
 *
 * ব্যবহার (Mini App পেজে):
 *   <script src="https://telegram.org/js/telegram-web-app.js"></script>
 *   <script src="https://v4zrashd.github.io/rashd-app--store/v4z-kit.js" data-app="myapp"></script>
 *
 * data-app        = mini-control.json -> apps[]-এর id (Admin Panel -> Control Center -> Mini App Kit-এ যোগ করা)
 * data-check      = (ঐচ্ছিক) checker API base, default: /api/kitcheck  (একই Vercel সাইটে হলে ঠিক আছে)
 * data-config     = (ঐচ্ছিক) config URL, default: GitHub Pages-এর mini-control.json
 *
 * পেজে চাইলে এই slot গুলো রাখা যায় (কিট নিজে ভরে দেবে):
 *   <img data-v4z="logo">  <span data-v4z="name"></span>  <div data-v4z="announcement"></div>
 *
 * JS API:
 *   V4ZKit.ready(fn)            -> config লোড হলে fn(kit) চলবে; state: kit.state / kit.entry
 *   V4ZKit.gate()               -> Promise; membership (+ gate.key থাকলে key check) পাস হলে resolve {ok:true,...}
 *                                  পাস না হলে কিট নিজেই lock screen দেখাবে, ইউজার ঠিক করলে আবার চেষ্টা হবে
 *   V4ZKit.checkKey(key)        -> Promise<{ok, reason}>  (key unused কিনা, burn হয় না)
 *   V4ZKit.burnKey(key, fileUrl?)-> Promise<{ok, reason}> (সফল কাজের পরেই ডাকতে হয়)
 *   V4ZKit.showAd()             -> Promise<boolean> (config-এ ads on থাকলে Monetag অ্যাড; না থাকলে সাথে সাথে true)
 *
 * নীতি: config না পেলে পেজ আগের মতোই চলবে (branding/ads শুধু বাদ), কিন্তু gate সবসময়
 * সার্ভার (kitcheck) দিয়ে যাচাই হয় — সার্ভারই আসল নিয়ম জানে। Telegram-এর বাইরে খুললে
 * membership gate fail-closed: Telegram থেকে খুলতে বলবে।
 */
(function () {
  'use strict';
  var DEFAULT_CONFIG = 'https://v4zrashd.github.io/rashd-app--store/mini-control.json';
  var script = null;
  try { script = document.currentScript; } catch (e) {}
  if (!script) { try { script = document.querySelector('script[data-app]'); } catch (e) {} }
  var ds = (script && script.dataset) || {};
  var APP = ds.app || (typeof window !== 'undefined' && window.V4Z_APP_ID) || '';
  var CHECK_URL = ds.check || '/api/kitcheck';
  var CONFIG_URL = ds.config || DEFAULT_CONFIG;
  var CHANNEL_URL = 'https://t.me/rashdteem';
  var KEY_URL = 'https://t.me/rashd12bot/rashdstore';

  var REASONS = {
    not_member: 'আগে @rashdteem চ্যানেলে জয়েন করো, তারপর আবার চেষ্টা করো।',
    key_invalid: 'কী-টা ঠিক নেই। আবার দেখে লেখো।',
    key_used: 'এই কী আগেই ব্যবহার হয়ে গেছে। নতুন কী লাগবে।',
    key_off: 'এই সার্ভিসে কী লাগে না।',
    disabled: 'এই সার্ভিসটা এখন বন্ধ আছে। পরে আবার এসো।',
    auth: 'Telegram থেকে আবার খোলো।',
    network: 'নেটওয়ার্ক সমস্যা — একটু পরে আবার চেষ্টা করো।',
    setup: 'সার্ভিসের সেটআপ বাকি আছে।',
    unknown_app: 'এই অ্যাপটা এখনো প্যানেলে যোগ হয়নি।'
  };

  var kit = {
    app: APP,
    entry: null,
    state: 'loading',
    readyCbs: [],
    ready: function (fn) {
      if (typeof fn !== 'function') return;
      if (kit.state !== 'loading') { try { fn(kit); } catch (e) {} }
      else kit.readyCbs.push(fn);
    }
  };
  window.V4ZKit = kit;

  function tg() { try { return (window.Telegram && window.Telegram.WebApp) || null; } catch (e) { return null; } }
  function initData() { var t = tg(); return (t && t.initData) || ''; }

  function fireReady() {
    var cbs = kit.readyCbs.splice(0);
    cbs.forEach(function (fn) { try { fn(kit); } catch (e) {} });
    try { document.dispatchEvent(new window.CustomEvent('v4zkit-ready', { detail: kit })); } catch (e) {}
  }

  function applyBranding(entry) {
    if (!entry) return;
    try {
      if (entry.name) {
        var names = document.querySelectorAll('[data-v4z="name"]');
        for (var i = 0; i < names.length; i++) names[i].textContent = entry.name;
        if (document.title && document.querySelector('[data-v4z="name"]')) document.title = entry.name;
      }
      var logos = document.querySelectorAll('[data-v4z="logo"]');
      for (var j = 0; j < logos.length; j++) {
        if (entry.logo) { logos[j].src = entry.logo; logos[j].style.display = ''; }
        else logos[j].style.display = 'none';
      }
      var anns = document.querySelectorAll('[data-v4z="announcement"]');
      for (var k = 0; k < anns.length; k++) {
        if (entry.announcement) { anns[k].textContent = entry.announcement; anns[k].style.display = ''; }
        else anns[k].style.display = 'none';
      }
    } catch (e) {}
  }

  var LOCK_ID = 'v4z-kit-lock';
  function lockEl() { return document.getElementById(LOCK_ID); }
  function hideLock() { var el = lockEl(); if (el && el.parentNode) el.parentNode.removeChild(el); }
  function showLock(html) {
    hideLock();
    var el = document.createElement('div');
    el.id = LOCK_ID;
    el.setAttribute('style', 'position:fixed;inset:0;z-index:99999;background:rgba(3,10,7,.94);display:flex;align-items:center;justify-content:center;padding:18px;');
    el.innerHTML = '<div style="max-width:420px;width:100%;background:linear-gradient(180deg,#0c1512,#08100c);border:1px solid #123528;border-radius:18px;padding:24px 18px;text-align:center;color:#d9ffef;font-family:\'Segoe UI\',system-ui,sans-serif;box-shadow:0 14px 40px rgba(0,0,0,.5)">' + html + '</div>';
    document.body.appendChild(el);
    return el;
  }
  function btnHtml(act, label, green) {
    return '<button data-act="' + act + '" style="display:inline-block;margin-top:14px;border:none;border-radius:12px;padding:13px 20px;font-weight:800;font-size:15px;cursor:pointer;' +
      (green ? 'background:#00ff9d;color:#032117;box-shadow:0 0 18px rgba(0,255,157,.35)' : 'background:#0b1512;color:#9fd8c3;border:1px solid #123528') + '">' + label + '</button>';
  }

  function post(body) {
    return fetch(CHECK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.assign({ app: APP, initData: initData() }, body || {}))
    }).then(function (r) { return r.json(); }).catch(function () { return { ok: false, reason: 'network' }; });
  }

  kit.checkKey = function (key) { return post({ action: 'check', key: String(key || '').trim() }); };
  kit.burnKey = function (key, fileUrl) {
    var b = { action: 'burn', key: String(key || '').trim() };
    if (fileUrl) b.fileUrl = String(fileUrl);
    return post(b);
  };

  function gateError(reason) {
    var msg = REASONS[reason] || REASONS.network;
    var el = showLock('<div style="font-size:42px">🔒</div>' +
      '<h2 style="font-size:18px;margin:10px 0 6px;color:#eafff5">সার্ভিস বন্ধ</h2>' +
      '<p style="font-size:13.5px;color:#9fd8c3;line-height:1.7">' + msg + '</p>');
    return el;
  }

  kit.gate = function (opts) {
    opts = opts || {};
    return new Promise(function (resolve) {
      var entry = kit.entry || {};
      var gate = entry.gate || {};
      function deny(reason) {
        if (reason === 'not_member') {
          var el = showLock('<div style="font-size:42px">🔒</div>' +
            '<h2 style="font-size:18px;margin:10px 0 6px;color:#eafff5">আগে চ্যানেলে জয়েন করো</h2>' +
            '<p style="font-size:13.5px;color:#9fd8c3;line-height:1.7">এই সার্ভিস শুধু @rashdteem মেম্বারদের জন্য। জয়েন করে ফিরে এসো।</p>' +
            '<a href="' + CHANNEL_URL + '" target="_blank" rel="noopener" style="display:inline-block;margin-top:14px;background:#00ff9d;color:#032117;text-decoration:none;font-weight:900;padding:13px 22px;border-radius:12px;font-size:15px;box-shadow:0 0 18px rgba(0,255,157,.35)">📢 চ্যানেলে জয়েন করো</a><br>' +
            btnHtml('recheck', '✅ জয়েন করেছি — আবার চেক করো', false));
          var b = el.querySelector('[data-act="recheck"]');
          if (b) b.addEventListener('click', function () { attempt(); });
        } else if (reason === 'disabled' || reason === 'unknown_app' || reason === 'setup') {
          gateError(reason);
        } else {
          var el2 = showLock('<div style="font-size:42px">⚠️</div>' +
            '<p style="font-size:14px;color:#9fd8c3;line-height:1.7">' + (REASONS[reason] || REASONS.network) + '</p>' +
            btnHtml('retry', '🔄 আবার চেষ্টা করো', true));
          var b2 = el2.querySelector('[data-act="retry"]');
          if (b2) b2.addEventListener('click', function () { attempt(); });
        }
      }
      function keyStep() {
        var el = showLock('<div style="font-size:42px">🔑</div>' +
          '<h2 style="font-size:18px;margin:10px 0 6px;color:#eafff5">কী লাগবে</h2>' +
          '<p style="font-size:13.5px;color:#9fd8c3;line-height:1.7">এই সার্ভিসে একটা App Store কী লাগে। কী না থাকলে <a href="' + KEY_URL + '" target="_blank" rel="noopener" style="color:#00ff9d;font-weight:800">Key Bot</a> থেকে নিয়ে এসো।</p>' +
          '<input id="v4z-kit-key" type="text" placeholder="তোমার কী এখানে বসাও" style="width:100%;margin-top:14px;background:#07110c;border:1px solid #123528;color:#eafff5;border-radius:12px;padding:13px 12px;font-size:14px;text-align:center">' +
          '<div id="v4z-kit-keymsg" style="margin-top:10px;font-size:13px;color:#fb7185;min-height:18px"></div>' +
          btnHtml('usekey', '✔️ কী যাচাই করো', true));
        var btn = el.querySelector('[data-act="usekey"]');
        var input = el.querySelector('#v4z-kit-key');
        var msg = el.querySelector('#v4z-kit-keymsg');
        if (btn) btn.addEventListener('click', function () {
          var key = input ? String(input.value || '').trim() : '';
          if (!key) { if (msg) msg.textContent = REASONS.key_invalid; return; }
          btn.disabled = true; if (msg) msg.textContent = '⏳ যাচাই হচ্ছে...';
          kit.checkKey(key).then(function (r) {
            btn.disabled = false;
            if (r && r.ok) { hideLock(); resolve({ ok: true, key: key, keyChecked: true }); }
            else if (msg) msg.textContent = REASONS[(r && r.reason)] || REASONS.network;
          });
        });
      }
      function attempt() {
        if (!initData()) {
          var el = showLock('<div style="font-size:42px">📱</div>' +
            '<h2 style="font-size:18px;margin:10px 0 6px;color:#eafff5">Telegram থেকে খোলো</h2>' +
            '<p style="font-size:13.5px;color:#9fd8c3;line-height:1.7">এই Mini App শুধু Telegram বট থেকে খোলে।</p>');
          resolve({ ok: false, reason: 'auth' });
          return;
        }
        post({ action: 'member' }).then(function (r) {
          if (!r || !r.ok) { deny((r && r.reason) || 'network'); if (!r || r.reason === 'disabled' || r.reason === 'unknown_app' || r.reason === 'setup') resolve({ ok: false, reason: (r && r.reason) || 'network' }); return; }
          if (gate.key === true && opts.key !== false) keyStep();
          else { hideLock(); resolve({ ok: true }); }
        });
      }
      attempt();
    });
  };

  var adLoaded = false;
  kit.showAd = function () {
    return new Promise(function (resolve) {
      var ads = (kit.entry && kit.entry.ads) || {};
      if (!ads.enabled || !ads.zone) { resolve(true); return; }
      var zone = String(ads.zone).replace(/[^0-9]/g, '');
      if (!zone) { resolve(true); return; }
      var done = false;
      var finish = function (v) { if (!done) { done = true; resolve(v); } };
      setTimeout(function () { finish(false); }, 45000);
      function callShow() {
        var fn = window['show_' + zone];
        if (typeof fn !== 'function') { finish(false); return; }
        try {
          var p = fn();
          if (p && typeof p.then === 'function') p.then(function () { finish(true); }, function () { finish(false); });
          else finish(true);
        } catch (e) { finish(false); }
      }
      if (typeof window['show_' + zone] === 'function') { callShow(); return; }
      if (!adLoaded) {
        adLoaded = true;
        var s = document.createElement('script');
        s.src = '//libtl.com/sdk.js';
        s.setAttribute('data-zone', zone);
        s.setAttribute('data-sdk', 'show_' + zone);
        s.onload = function () { setTimeout(callShow, 300); };
        s.onerror = function () { finish(false); };
        document.head.appendChild(s);
      } else {
        var tries = 0;
        var iv = setInterval(function () {
          tries++;
          if (typeof window['show_' + zone] === 'function') { clearInterval(iv); callShow(); }
          else if (tries > 20) { clearInterval(iv); finish(false); }
        }, 300);
      }
    });
  };

  function init() {
    if (!APP) { kit.state = 'no-app'; fireReady(); return; }
    fetch(CONFIG_URL, { cache: 'no-cache' }).then(function (r) { return r.json(); }).then(function (cfg) {
      var list = (cfg && Array.isArray(cfg.apps)) ? cfg.apps : [];
      for (var i = 0; i < list.length; i++) { if (list[i] && list[i].id === APP) { kit.entry = list[i]; break; } }
      if (kit.entry && kit.entry.enabled === false) {
        kit.state = 'disabled';
        gateError('disabled');
      } else {
        kit.state = kit.entry ? 'ready' : 'unknown-app';
        applyBranding(kit.entry);
      }
      fireReady();
    }).catch(function () {
      kit.state = 'no-config';
      fireReady();
    });
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
