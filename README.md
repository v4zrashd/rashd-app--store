<p align="center">
  <img src="https://github.com/v4zrashd/rashd-app--store/raw/main/icons/rashd.png" width="96" alt="RASHD">
</p>

<h1 align="center">📱 RASHD Modded APK Store</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Host-GitHub%20Pages-6366f1" alt="host">
  <img src="https://img.shields.io/badge/Bot-@rashd12bot-229ed9" alt="bot">
  <img src="https://img.shields.io/badge/Group-RASHD-ff5d8f" alt="group">
  <img src="https://img.shields.io/badge/License-MIT-9aa0a0" alt="license">
</p>

<p align="center">
  একটি সুন্দর, লাইভ ও রেস্পন্সিভ মডেড APK স্টোর — <b>শুধু @rashd12bot বট থেকে ওপেন করা যায়।</b>
</p>

---

## ✨ ফিচারসমূহ

- 🌌 **Aurora Glass ডিজাইন** — অ্যানিমেটেড ব্যাকগ্রাউন্ড, গ্লাস কার্ড, গ্রেডিয়েন্ট হিরো।
- 🔄 **রিয়েল-টাইম ডেটা** — প্রতি ৪৫ সেকেন্ডে অটো-রিফ্রেশ, ডাউনলোড ও ভিউ কাউন্ট লাইভ আপডেট।
- 📊 **রিয়েল ডাউনলোড কাউন্ট** — GitHub রিলিজের আসল `download_count` + ব্রাউজার ক্লিক কাউন্ট মিলে দেখায়।
- 💬 **প্রতি APK-এ কমেন্ট** — `💬 কমেন্ট` → লিখে `পাঠান` → সরাসরি আমাদের গ্রুপে যায় (বট অ্যাডমিন)।
- 🔍 **সার্চ ও ফিল্টার** — নাম দিয়ে খুঁজুন, এক্সটেনশন অনুযায়ী ফিল্টার করুন।
- 🏅 **টপ ডাউনলোড** — সবচেয়ে বেশি ডাউনলোড হওয়া অ্যাপ `#১` + 🔥 Trending।
- 🔒 **বট-এক্সক্লুসিভ** — সাইট একটা সিক্রেট কী দিয়ে গেটেড; ডাইরেক্ট লিংক কাজ করে না।
- 📲 **রেস্পন্সিভ** — মোবাইল/ডেস্কটপ + Telegram in-app ব্রাউজারে কাজ করে।
- 🤖 **Telegram WebApp** — "🛒 Open App Store" বাটনে টেলিগ্রামের ভিতরে ওপেন করা যায়।

---

## 🔗 লিংকসমূহ

| ধরণ | লিংক |
|------|------|
| 🤖 বট | [@rashd12bot](https://t.me/rashd12bot) |
| 👥 গ্রুপ | [আমাদের গ্রুপ](https://t.me/+T8FL1b_ELRNiMjk1) |
| 📢 চ্যানেল ১ | [@v4zrasehd](https://t.me/v4zrasehd) |
| 📢 চ্যানেল ২ | [@cybersohag121](https://t.me/cybersohag121) |
| 📢 চ্যানেল ৩ | [@rs_extra_info](https://t.me/rs_extra_info) |

---

## 🛡 ফোর্স-জয়েন (বট ব্যবহারের শর্ত)

বট ব্যবহার করতে হলে ইউজারকে অবশ্যই নিচের ৩ চ্যানেলে জয়েন থাকতে হবে, নাহলে বট কোনো কাজ করবে না:

1. [@v4zrasehd](https://t.me/v4zrasehd)
2. [@cybersohag121](https://t.me/cybersohag121)
3. [@rs_extra_info](https://t.me/rs_extra_info)

> ⚠️ ভেরিফিকেশন কাজ করার জন্য **@rashd12bot** বটটিকে ওই ৩ চ্যানেলে **অ্যাডমিন** করতে হবে।

---

## 🛠 কিভাবে কাজ করে

```text
Telegram Bot (@rashd12bot)
   │  "/start" → চ্যানেল ভেরিফাই → "🛒 Open App Store"
   ▼
Static Site (GitHub Pages)  ──▶  apps.json  (রিলিজ থেকে জেনারেটেড)
   │  💬 কমেন্ট → Image() রিকোয়েস্ট → আমাদের গ্রুপ গ্রুপে মেসেজ
```

- সাইট স্ট্যাটিক (`index.html`), GitHub Pages দিয়ে হোস্ট।
- ডেটা স্ট্যাটিক `apps.json` থেকে নেওয়া হয় → GitHub API রেট-লিমিট (403) নেই।
- নতুন রিলিজ → GitHub Actions (`.github/workflows/build-data.yml`) অটো `apps.json` রিফ্রেশ করে।

---

## ➕ নতুন APK যোগ করবেন

1. **Releases** → **Draft a new release**।
2. ট্যাগ দিন (যেমন `v1.1`) → APK/APKS/ZIP আপলোড করুন।
3. **Publish release** → ওয়ার্কফ্লো `apps.json` আপডেট করবে → সাইটে নতুন অ্যাপ চলে আসবে।

> ডাউনলোড কাউন্ট GitHub নিজে গুনে রাখে, তাই রিলিজ করলেই রিয়েল কাউন্ট দেখাবে।

---

## 💬 কমেন্ট সিস্টেম

প্রতিটি APK কার্ডের নিচে **💬 কমেন্ট** বাটন:

- বাটন → ইনপুট বক্স ওপেন (অটো-ফোকাস)।
- কমেন্ট লিখে **পাঠান** → ব্রাউজার থেকে সরাসরি `আমাদের গ্রুপ` গ্রুপে মেসেজ
  (বট `@rashd12bot` গ্রুপে অ্যাডমিন হতে হবে)।

---

## 📂 ফাইল স্ট্রাকচার

```text
rashd-app--store/
├── index.html              # মূল ওয়েবসাইট (কী-গেটেড)
├── apps.json               # রিলিজ থেকে জেনারেটেড অ্যাপ ডেটা
├── icons/                  # অ্যাপ আইকন + RASHD লোগো
├── .github/workflows/
│   └── build-data.yml      # রিলিজ হলে apps.json রিফ্রেশ
└── README.md
```

---

## ⚠️ নোট

- APK ডাউনলোড শুধু এই ওয়েবসাইট থেকে (বট ফাইল পাঠানো বন্ধ)।
- কোনো APK সম্পর্কে না জানলে সেটি ইনস্টল করবেন না।
- কমেন্ট/অভিযোগ আমাদের গ্রুপ গ্রুপে পাঠানো যায়।

---

<p align="center"><b>Made with ❤️ by RASHD / V4Z Team</b></p>
