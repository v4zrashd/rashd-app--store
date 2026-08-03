import asyncio
import json
import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# ==========================================
# 🤖 BOT CONFIGURATION
# ==========================================
BOT_TOKEN = "8803671280:AAFsUW9SDQubmsEioFW9lKtcUhVU4tmWSy4"
WEB_APP_URL = "https://v4zrashd.github.io/rashd-app--store/"
ADMIN_ID = 8100055552
USERS_FILE = "users.json"

# চ্যানেল তালিকা
CHANNELS = [
    {'user': '@cybersohag121', 'link': 'https://t.me/cybersohag121', 'name': 'Cybersohag121'},
    {'user': '@v4zrasehd', 'link': 'https://t.me/v4zrasehd', 'name': 'V4zRasehd'},
]

# লিংক চেনার জন্য ছোট হেল্পার
URL_PATTERN = re.compile(r'^(https?|ftp)://[^\s]+$', re.IGNORECASE)
SUPPORTED_HOSTS = ['instagram.com', 'youtube.com', 'youtu.be', 'tiktok.com',
                   'twitter.com', 'x.com', 'facebook.com', 'fb.com', 'reddit.com']

# Telegram ভাষা কোড -> আমাদের কোড
TELEGRAM_LANG_MAP = {
    'en': 'en', 'bn': 'bn', 'hi': 'hi', 'ar': 'ar', 'es': 'es',
    'pt': 'pt', 'ru': 'ru', 'fr': 'fr', 'id': 'id', 'zh': 'zh'
}

# ==========================================
# 🌐 10 LANGUAGES 🔤
# ==========================================
LANG_ORDER = ['en', 'bn', 'hi', 'ar', 'es', 'pt', 'ru', 'fr', 'id', 'zh']

LANGS = {
    'en': {'flag': '🇬🇧', 'name': 'English'},
    'bn': {'flag': '🇧🇩', 'name': 'বাংলা'},
    'hi': {'flag': '🇮🇳', 'name': 'हिन्दी'},
    'ar': {'flag': '🇸🇦', 'name': 'العربية'},
    'es': {'flag': '🇪🇸', 'name': 'Español'},
    'pt': {'flag': '🇧🇷', 'name': 'Português'},
    'ru': {'flag': '🇷🇺', 'name': 'Русский'},
    'fr': {'flag': '🇫🇷', 'name': 'Français'},
    'id': {'flag': '🇮🇩', 'name': 'Bahasa Indonesia'},
    'zh': {'flag': '🇨🇳', 'name': '中文'},
}

STRINGS = {
    'en': {
        'welcome': (
            "🤖 *RASHD APP STORE*\n"
            "━━━━━━━━━━━━━━━━━\n\n"
            "👋 *Welcome, {name}!*\n\n"
            "📱 *Premium Modded APKs* — unlocked, VIP, no ads\n"
            "⚡ *Fast updates* — latest versions instantly\n"
            "🆓 *100% Free* — every download costs nothing\n"
            "📥 *Smart downloader* — paste a link and watch it work\n\n"
            "👉 *Tap a button below to get started:*"
        ),
        'join_title': (
            "🚫 *Join Our Channels First!*\n\n"
            "You must join the following channels to unlock the App Store:\n\n"
        ),
        'join_prompt': "\n\n✅ *After joining all, tap verify:*",
        'verify_ok': "✅ *Verification Successful!*\n\nTap below to start exploring:",
        'not_joined': "❌ Still not joined: {names}",
        'choose_lang': "🗣️ *Select your language / আপনার ভাষা নির্বাচন করুন:*",
        'lang_set': "✅ *Language set to* {lang}!",
        'channel_menu': "📢 *Our Channels*\n\nJoin our channels for updates:",
        'dl_menu': (
            "📥 *Download Zone*\n\n"
            "Paste any supported link:\n"
            "`/download <url>`\n\n"
            "🔗 *Supported:* YouTube, Instagram, TikTok, Twitter/X, Facebook, Reddit."
        ),
        'dl_usage': (
            "📥 *Download Usage:*\n\n"
            "Send a supported link like:\n"
            "`/download https://youtube.com/watch?v=...`\n\n"
            "🔗 Supported: YouTube, Instagram, TikTok, Twitter/X, Facebook, Reddit."
        ),
        'dl_invalid': "❌ *Invalid link or unsupported platform. Please try again.*",
        'dl_notmember': "🚫 *Join first:* {names}\n\nUse /start to verify.",
        'dl_1': "⏳ *Downloading...* `[1/3]`",
        'dl_2': "⚙️ *Processing...* `[2/3]`",
        'dl_3': "📤 *Uploading...* `[3/3]`",
        'dl_done': (
            "✅ *Download Complete!*\n\n"
            "🔗 Link: `{link}`\n\n"
            "👨💻 Made with ❤️ by *RASHD ( @v4zrasehd )*"
        ),
        'about': (
            "💜 *Made with ❤️ by RASHD ( @v4zrasehd )*\n\n"
            "⚡ Premium APK Store & smart downloader bot.\n"
            "🆓 Free forever · Fast updates · No ads."
        ),
        'profile': (
            "👤 *Your Profile*\n\n"
            "Name: `{name}`\n"
            "User ID: `{uid}`\n"
            "Username: @{uname}\n"
            "Language: {lang}\n\n"
            "✅ Channel status: *Verified!*"
        ),
        'btn_download': "📥 Download",
        'btn_channel': "📢 Channel",
        'btn_about': "👨‍💻 About",
        'btn_language': "🌐 Language",
        'btn_openstore': "🛒 Open App Store",
        'btn_verify': "✅ Verify Membership",
        'btn_change': "🌐 Change Language",
    },
    'bn': {
        'welcome': (
            "🤖 *RASHD APP STORE*\n"
            "━━━━━━━━━━━━━━━━━\n\n"
            "👋 *স্বাগতম, {name}!*\n\n"
            "📱 *প্রিমিয়াম মোড APK* — আনলকড, VIP, বিজ্ঞাপনহীন\n"
            "⚡ *দ্রুত আপডেট* — সর্বশেষ ভার্সন সাথে সাথে\n"
            "🆓 *১০০% ফ্রি* — কোনো চার্জ ছাড়াই সব ডাউনলোড\n"
            "📥 *স্মার্ট ডাউনলোডার* — লিংক পেস্ট করলেই কাজ করবে\n\n"
            "👉 *নিচের বাটন চেপে শুরু করুন:*"
        ),
        'join_title': (
            "🚫 *প্রথমে আমাদের চ্যানেলে জয়েন করুন!*\n\n"
            "অ্যাপ স্টোর ব্যবহার করতে নিচের চ্যানেলগুলোতে জয়েন করতে হবে:\n\n"
        ),
        'join_prompt': "\n\n✅ *সব চ্যানেলে জয়েন করার পর verify চাপুন:*",
        'verify_ok': "✅ *ভেরিফিকেশন সফল!*\n\nনিচে চেপে শুরু করুন:",
        'choose_lang': "🗣️ *আপনার ভাষা নির্বাচন করুন:*",
        'not_joined': "❌ এখনও জয়েন করেননি: {names}",
        'lang_set': "✅ *ভাষা সেট করা হয়েছে* {lang}!",
        'channel_menu': "📢 *আমাদের চ্যানেল*\n\nআপডেটের জন্য জয়েন করুন:",
        'dl_menu': (
            "📥 *ডাউনলোড জোন*\n\n"
            "যেকোনো সাপোর্টেড লিংক দিন:\n"
            "`/download <url>`\n\n"
            "🔗 *সাপোর্টেড:* YouTube, TikTok, Instagram, Twitter/X, Facebook, Reddit."
        ),
        'dl_usage': (
            "📥 *ডাউনলোড ব্যবহার পদ্ধতি:*\n\n"
            "সাপোর্টেড লিংক দিন:\n"
            "`/download https://youtube.com/watch?v=...`\n\n"
            "🔗 সাপোর্টেড: YouTube, TikTok, Instagram, Twitter/X, Facebook, Reddit."
        ),
        'dl_invalid': "❌ *লিংকটি ভুল বা সাপোর্টেড প্ল্যাটফর্ম নয়। আবার চেষ্টা করুন।*",
        'dl_notmember': "🚫 *প্রথমে জয়েন করুন:* {names}\n\nযাচাই করতে /start দিন।",
        'dl_1': "⏳ *ডাউনলোড হচ্ছে...* `[1/3]`",
        'dl_2': "⚙️ *প্রসেস হচ্ছে...* `[2/3]`",
        'dl_3': "📤 *আপলোড হচ্ছে...* `[3/3]`",
        'dl_done': (
            "✅ *ডাউনলোড সম্পন্ন!*\n\n"
            "🔗 লিংক: `{link}`\n\n"
            "👨💻 ভালোবাসা দিয়ে বানানো *RASHD ( @v4zrasehd )*"
        ),
        'about': (
            "💜 *ভালোবাসা ❤️ দিয়ে বানানো RASHD ( @v4zrasehd )*\n\n"
            "⚡ প্রিমিয়াম APK স্টোর ও স্মার্ট ডাউনলোডার বট।\n"
            "🆓 চিরকাল ফ্রি · দ্রুত আপডেট · কোনো বিজ্ঞাপন নেই।"
        ),
        'profile': (
            "👤 *আপনার প্রোফাইল*\n\n"
            "নাম: `{name}`\n"
            "User ID: `{uid}`\n"
            "Username: @{uname}\n"
            "ভাষা: {lang}\n\n"
            "✅ চ্যানেল স্ট্যাটাস: *ভেরিফাইড!*"
        ),
        'btn_download': "📥 ডাউনলোড",
        'btn_channel': "📢 চ্যানেল",
        'btn_about': "👨‍💻 About",
        'btn_language': "🌐 ভাষা",
        'btn_openstore': "🛒 অ্যাপ স্টোর",
        'btn_verify': "✅ জয়েন চেক",
        'btn_profile': "🌐 ভাষা বদলান",
    },
    'hi': {
        'welcome': (
            "🤖 *RASSO APP STORE*\n"
            "━━━━━━━━━━━━━━━━━\n\n"
            "👋 *स्वागत है, {name}!*\n\n"
            "📱 *प्रीमियम मॉड APK* — अनलॉक, VIP, बिना विज्ञापन\n"
            "⚡ *फास्ट अपडेट* — नवीनतम वर्जन तुरंत\n"
            "🆓 *100% फ्री* — सभी डाउनलोड निःशुल्क\n"
            "📥 *स्मार्ट डाउनलोडर* — लिंक पेस्ट करें\n\n"
            "👉 *नीचे बटन दबाकर शुरू करें:*"
        ),
        'join_title': (
            "🚫 *पहले हमारे चैनल ज्वाइन करें!*\n\n"
            "ऐप स्टोर एक्सेस करने के लिए इन चैनलों को ज्वाइन करें:\n\n"
        ),
        'join_prompt': "\n\n✅ *सब ज्वाइन करने के बाद verify दबाएं:*",
        'verify_ok': "✅ *वेरिफिकेशन सफल!*\n\nशुरू करने के लिए नीचे दबाएं:",
        'choose_lang': "🗣️ *अपनी भाषा चुनें:*",
        'not_joined': "⚠️ अभी ज्वाइन नहीं किया: {names}",
        'channel_menu': "📢 *हमारे चैनल*\n\nअपडेट के लिए ज्वाइन करें:",
        'dl_menu': (
            "📥 *डाउनलोड ज़ोन*\n\n"
            "कोई समर्थित लिंक दें:\n"
            "`/download <url>`\n\n"
            "🔗 समर्थित: YouTube, TikTok, Instagram, Twitter/X, Facebook, Reddit."
        ),
        'dl_usage': (
            "📥 *डाउनलोड उपयोग:*\n\n"
            "समर्थित लिंक दें:\n"
            "`/download https://youtube.com/watch?v=...`"
        ),
        'dl_invalid': "❌ *अमान्य लिंक या असमर्थित प्लेटफ़ॉर्म। कृपया फिर से प्रयास करें।*",
        'dl_notmember': "🚫 *पहले ज्वाइन करें:* {names}\n\nसत्यापन के लिए /start दें।",
        'dl_1': "⏳ *डाउनलोड हो रहा है...* `[1/3]`",
        'dl_2': "⚙️ *प्रोसेस हो रहा है...* `[2/3]`",
        'dl_3': "📤 *अपलोड हो रहा है...* `[3/3]`",
        'dl_done': "✅ *डाउनलोड पूरा!*\n\n🔗 लिंक: `{link}`\n\n👨💻 ❤️ से बना *RASHD ( @v4zrasehd )*",
        'about': "💜 *RASHD ( @v4zrasehd ) द्वारा ❤️ से बनाया गया*\n\n⚡ प्रीमियम APK स्टोर व स्मार्ट डाउनलोडर बॉट।\n🆓 सदा फ्री · तेज़ · बिना विज्ञापन।",
        'profile': (
            "👤 *आपकी प्रोफाइल*\n\n"
            "नाm: `{name}`\n"
            "User ID: `{uid}`\n"
            "Username: @{uname}\n"
            "भाषा: {lang}\n\n"
            "✅ चैनल: *वेरिफाईड!*"
        ),
        'btn_download': "📥 डाउनलोड",
        'btn_channel': "📢 चैनल",
        'btn_about': "👨‍💻 About",
        'btn_language': "🌐 भाषा",
        'btn_openstore': "🛒 स्टोर",
        'btn_verify': "✅ वेरिफाई",
        'btn_profile': "🌐 भाषा बदलें",
    },
    'ar': {
        'welcome': (
            "🤖 *متجر راشد للتطبيقات*\n"
            "━━━━━━━━━━━━━━━━━\n\n"
            "👋 *أهلاً بك, {name}!*\n\n"
            "📱 *أبك معدلة متميزة* — مفتوح، VIP، بدون إعلانات\n"
            "⚡ *تحديثات سريعة* — أحدث الإصدارات فورًا\n"
            "🆓 *مجاني 100%* — كل التحميلات بدون مقابل\n"
            "📥 *محمل ذكي* — الصق الرابط\n\n"
            "👉 *اضغط الزر بالأسفل للبدء:*"
        ),
        'join_title': (
            "🚫 *انضم إلى قنواتنا أولاً!*\n\n"
            "يجب الانضمام إلى القنوات التالية لفتح المتجر:\n\n"
        ),
        'join_prompt': "\n\n✅ *بعد الانضمام، اضغط تحقق:*",
        'verify_ok': "✅ *تحقق ناجح!*\n\nاضغط بالأسفل للبدء:",
        'choose_lang': "🗣️ *اختر لغتك:*",
        'not_joined': "⚠️ لم تنضم بعد: {names}",
        'channel_menu': "📢 *قنواتنا*\n\nانضم للقنوات:",
        'dl_menu': (
            "📥 *منطقة التحميل*\n\n"
            "أرسل رابطًا مدعومًا:\n"
            "`/download <url>`\n\n"
            "🔗 *مدعوم:* يوتيوب، تيك توك، انستغرام، تويتر، فيسبوك، ريديت."
        ),
        'dl_usage': (
            "📥 *طريقة الاستخدام:*\n\n"
            "أرسل رابطًا مدعومًا:\n"
            "`/download https://youtube.com/watch?v=...`"
        ),
        'dl_invalid': "❌ *رابط غير صالح أو منصة غير مدعومة. حاول مرة أخرى.*",
        'dl_notmember': "🚫 *انضم أولاً:* {names}\n\nللتحقق استخدم /start.",
        'dl_1': "⏳ *جارٍ التحميل...* `[1/3]`",
        'dl_2': "⚙️ *جارٍ المعالجة...* `[2/3]`",
        'dl_3': "📤 *جارٍ الرفع...* `[3/3]`",
        'dl_done': "✅ *اكتمل التحميل!*\n\n🔗 الرابط: `{link}`\n\n👨‍💻 صنع بـ ❤️ بواسطة RASHD ( @v4zrasehd )",
        'about': "💜 *صنع ❤️ بواسطة RASHD ( @v4zrasehd )*\n\n⚡ متجر أبك متميز وبوت تحميل ذكي.\n🆓 مجاني · سريع · بدون إعلانات.",
        'profile': (
            "👤 *ملفك الشخصي*\n\n"
            "الاسم: `{name}`\n"
            "المعرف: `{uid}`\n"
            "اسم المستخدم: @{uname}\n"
            "اللغة: {lang}\n\n"
            "✅ حالة القناة: مؤكد!"
        ),
        'btn_download': "📥 تحميل",
        'btn_channel': "📢 القناة",
        'btn_about': "👨‍💻 عن",
        'btn_language': "🌐 اللغة",
        'btn_openstore': "🛒 المتجر",
        'btn_verify': "✅ تحقق",
        'btn_profile': "🌐 تغيير اللغة",
    },
    'es': {
        'welcome': (
            "🤖 *RASH APP STORE*\n"
            "━━━━━━━━━━━━━━━━━\n\n"
            "👋 *¡Bienvenido, {name}!*\n\n"
            "📱 *APK mod premium* — desbloqueados, VIP, sin anuncios\n"
            "⚡ *Actualizaciones rápidas* — las últimas versiones\n"
            "🆓 *100% gratis* — todas las descargas\n"
            "📥 *Descargador inteligente* — pega un enlace\n\n"
            "👉 *Pulsa un botón para empezar:*"
        ),
        'join_title': "🚫 *¡Primero únete a nuestros canales!*\n\nDebes unirte a estos canales para acceder:\n\n",
        'join_prompt': "\n\n✅ *Tras unirte, pulsa verificar:*",
        'verify_ok': "✅ *¡Verificación exitosa!*\n\nPulsa abajo para comenzar:",
        'choose_lang': "🗣️ *Elige tu idioma:*",
        'not_joined': "⚠️ Aún no te has unido: {names}",
        'channel_menu': "📢 *Nuestros canales*\n\nÚnete:",
        'dl_menu': "📥 *Zona de descarga*\n\nEnvía un enlace compatible:\n`/download <url>`\n\n🔗 *Compatible:* YouTube, TikTok, Instagram, X, Facebook, Reddit.",
        'dl_usage': "📥 *Uso:*\n\nEnvía un enlace válido:\n`/download https://youtube.com/watch?v=...`",
        'dl_invalid': "❌ *Enlace inválido o plataforma no compatible. Inténtalo de nuevo.*",
        'dl_notmember': "🚫 *Únete primero:* {names}\n\nUsa /start para verificar.",
        'dl_1': "⏳ *Descargando...* `[1/3]`",
        'dl_2': "⚙️ *Procesando...* `[2/3]`",
        'dl_3': "📤 *Subiendo...* `[3/3]`",
        'dl_done': "✅ *¡Descarga completa!*\n\n🔗 Enlace: `{link}`\n\n👨💻 Hecho ❤️ por *RASHD ( @v4zrasehd )*",
        'about': "💜 *Hecho ❤️ por RASHD ( @v4zrasehd )*\n\n⚡ Tienda de APK y bot descargador.\n🆓 Gratis · rápido · sin anuncios.",
        'profile': "👤 *Tu perfil*\n\nNombre: `{name}`\nID: `{uid}`\nUsuario: @{uname}\nIdioma: {lang}\n\n✅ ¡Verificado!",
        'btn_download': "📥 Descargar",
        'btn_channel': "📢 Canal",
        'btn_about': "👨‍💻 Acerca",
        'btn_language': "🌐 Idioma",
        'btn_openstore': "🛒 Tienda",
        'btn_verify': "✅ Verificar",
        'btn_profile': "🌐 Cambiar idioma",
    },
    'pt': {
        'welcome': (
            "🤖 *RASHD APP STORE*\n"
            "━━━━━━━━━━━━━━━━━\n\n"
            "👋 *Bem-vindo, {name}!*\n\n"
            "📱 *APKs mod toda rais* — desbloqueadas, VIP, sem anúncios\n"
            "⚡ *Atualizações rápidas*\n"
            "🆓 *100% grátis*\n"
            "📥 *Download inteligente* — cole um link\n\n"
            "👉 *Toque em um botão abaixo:*"
        ),
        'join_title': "🚫 *Entre em nossos canais primeiro!*\n\nÉ preciso entrar nestes canais:\n\n",
        'join_prompt': "\n\n✅ *Depois de entrar, toque em verificar:*",
        'verify_ok': "✅ *Verificação bem-sucedida!*\n\nToque abaixo para começar:",
        'choose_lang': "🗣️ *Escolha seu idioma:*",
        'not_joined': "⚠️ Você ainda não entrou: {names}",
        'channel_menu': "📢 *Nossos canais*\n\nEntre nos canais:",
        'dl_menu': "📥 *Zona de download*\n\nEnvie um link compatível:\n`/download <url>`\n\n🔗 *Suportado:* YouTube, TikTok, Instagram, X, Facebook, Reddit.",
        'dl_usage': "📥 *Como usar:*\n\nEnvie um link:\n`/download https://youtube.com/watch?v=...`",
        'dl_invalid': "❌ *Link inválido ou plataforma não suportada. Tente novamente.*",
        'dl_notmember': "🚫 *Entre primeiro:* {names}\n\nUse /start para verificar.",
        'dl_1': "⏳ *Baixando...* `[1/3]`",
        'dl_2': "⚙️ *Processando...* `[2/3]`",
        'dl_3': "📤 *Enviando...* `[3/3]`",
        'dl_done': "✅ *Download concluído!*\n\n🔗 Link: `{link}`\n\n👨💻 Feito ❤️ por RASHD ( @v4zrasehd )",
        'about': "💜 *Feito ❤️ por RASHD ( @v4zrasehd )*\n\n⚡ Loja de APK + bot downloader.\n🆓 Grátis · rápido · sem anúncios.",
        'profile': "👤 *Seu perfil*\n\nNome: `{name}`\nID: `{uid}`\nUsuário: @{uname}\nIdioma: {lang}\n\n✅ Verificado!",
        'btn_download': "📥 Baixar",
        'btn_channel': "📢 Canal",
        'btn_about': "👨‍💻 Sobre",
        'btn_language': "🌐 Idioma",
        'btn_openstore': "🛒 Loja",
        'btn_verify': "✅ Verificar",
        'btn_profile': "🌐 Trocar idioma",
    },
    'ru': {
        'welcome': (
            "🤖 *RASHD APP STORE*\n"
            "━━━━━━━━━━━━━━━━━\n\n"
            "👋 *Добро пожаловать, {name}!*\n\n"
            "📱 *Премиум моды APK* — без рекламы\n"
            "⚡ *Быстрые обновления*\n"
            "🆓 *100% бесплатно*\n"
            "📑 *Умный архив:* — вставьте ссылку\n\n"
            "👉 *Нажмите кнопку ниже:*"
        ),
        'join_title': "🚫 *Сначала вступите в наши каналы!*\n\nНеобходимо вступить в эти каналы:\n\n",
        'join_prompt': "\n\n✅ *После вступления нажмите проверить:*",
        'verify_ok': "✅ *Проверка пройдена!*\n\nНажмите ниже, чтобы начать:",
        'choose_lang': "🗣️ *Выберите язык:*",
        'not_joined': "⚠️ Вы ещё не вступили: {names}",
        'channel_menu': "📢 *Наши каналы*\n\nВступите:",
        'dl_menu': "📥 *Зона загрузки*\n\nОтправьте поддерживаемую ссылку:\n`/download <url>`\n\n🔗 *Поддерживается:* YouTube, TikTok, Instagram, X, Facebook, Reddit.",
        'dl_usage': "📥 *Как использовать:*\n\nОтправьте ссылку:\n`/download https://youtube.com/watch?v=...`",
        'dl_invalid': "❌ *Неверная ссылка или неподдерживаемая платформа. Попробуйте ещё раз.*",
        'dl_notmember': "🚫 *Вступайте:* {names}\n\nДля проверки: /start.",
        'dl_1': "⏳ *Загрузка...* `[1/3]`",
        'dl_2': "⚙️ *Обработка...* `[2/3]`",
        'dl_3': "📤 *Загрузка...* `[3/3]`",
        'dl_done': "✅ *Загрузка завершена!*\n\n🔗 Ссылка: `{link}`\n\n👨💻 С ❤️ от RASHD ( @v4zrasehd )",
        'about': "💜 *RASHD ( @v4zrasehd )*\n\n⚡ Магазин APK и умный качалка.\n🆓 Бесплатно · быстро · без рекламы.",
        'profile': "👤 *Ваш профиль*\n\nИмя: `{name}`\nID: `{uid}`\nЮзер: @{uname}\nЯзык: {lang}\n\n✅ Подтверждён!",
        'btn_download': "📥 Скачать",
        'btn_channel': "📢 Канал",
        'btn_about': "👨‍💻 О нас",
        'btn_language': "🌐 Язык",
        'btn_openstore': "🛒 Магазин",
        'btn_verify': "✅ Проверить",
        'btn_profile': "🌐 Язык",
    },
    'fr': {
        'welcome': (
            "🤖 *RASHD APP STORE*\n"
            "━━━━━━━━━━━━━━━━━\n\n"
            "👋 *Bienvenue, {name}!*\n\n"
            "📱 *APK mods premium* — débloqués, sans pub\n"
            "⚡ *Màj rapides*\n"
            "🆓 *100% gratuit*\n"
            "📥 *Téléchargeur intelligent*\n\n"
            "👉 *Appuyez sur un bouton:*"
        ),
        'join_title': "🚫 *Rejoignez vos chaînes d'abord!*\n\nRejoignez ces chaînes :\n\n",
        'join_prompt': "\n\n✅ *Une fois rejoint, appuyez sur vérifier:*",
        'verify_ok': "✅ *Vérification réussie!*\n\nAppuyez ci-dessous :",
        'choose_lang': "🗣️ *Choisissez votre langue :*",
        'not_joined': "⚠️ Pas encore rejoint : {names}",
        'channel_menu': "📢 *Nos chaînes*\n\nRejoindre :",
        'dl_menu': "📥 *Zone de téléchargement*\n\nEnvoyez un lien supporté :\n`/download <url>`\n\n🔗 *Supporté :* YouTube, TikTok, Instagram, X, Facebook, Reddit.",
        'dl_usage': "📺 *Utilisation :*\n\nEnvoyez un lien :\n`/download https://youtube.com/watch?v=...`",
        'dl_invalid': "❌ *Lien invive ou plateforme non supportée. Réessayez.*",
        'dl_notmember': "🚫 *Rejoignez d'abord :* {names}\n\nUtilisez /start pour vérifier.",
        'dl_1': "⏳ *Téléchargement...* `[1/3]`",
        'dl_2': "⚙️ *Traitement...* `[2/3]`",
        'dl_3': "📤 *Envoi...* `[3/3]`",
        'dl_done': "✅ *Téléchargement terminé!\n\n🔗 Lien : `{link}`\n\n👨💻 Fait ❤️ par RASHD ( @v4zrasehd )",
        'about': "💜 *RASHD ( @v4zrasehd )*\n\n⚡ Magasin d'APK et bot téléchargeur.\n🆓 Gratuit · rapide · sans pub.",
        'profile': "👤 *Votre profil*\n\nNom : `{name}`\nID : `{uid}`\nUtilisé par : @{uname}\nLangue : {lang}\n\n✅ Vérifié !",
        'btn_download': "📥 Télécharger",
        'btn_channel': "📢 Chaîne",
        'btn_about': "👨‍💻 À propos",
        'btn_language': "🌐 Langue",
        'btn_openstore': "🛒 Boutique",
        'btn_verify': "✅ Vérifier",
        'btn_profile': "🌐 Changer",
    },
    'id': {
        'welcome': (
            "🤖 *RASHD APP STORE*\n"
            "━━━━━━━━━━━━━━━━━\n\n"
            "👋 *Selamat datang, {name}!*\n\n"
            "📱 *APK mod premium* — tak terkunci, tanpa iklan\n"
            "⚡ *Update cepat*\n"
            "🆓 *100% gratis*\n"
            "📥 *Download cerdas*\n\n"
            "👉 *Tekan tombol di bawah:*"
        ),
        'join_title': "🚫 *Bergabung dulu ke channel!*\n\nGabung channel berikut:\n\n",
        'join_prompt': "\n\n✅ *Setelah gabung, tekan verifikasi:*",
        'verify_ok': "✅ *Verifikasi berhasil!*\n\nTekan untuk mulai:",
        'choose_lang': "🗣️ *Pilih bahasa Anda:*",
        'not_joined': "⚠️ Belum bergabung: {names}",
        'channel_menu': "📢 *Channel kami*\n\nGabung:",
        'dl_menu': "📥 *Zona download*\n\nKirim link yang didukung:\n`/download <url>`\n\n🔗 *Didukung:* YouTube, TikTok, Instagram, X, Facebook, Reddit.",
        'dl_usage': "📥 *Cara pakai:*\n\nKirim link:\n`/download https://youtube.com/watch?v=...`",
        'dl_invalid': "❌ *Link tidak valid atau platform tidak didukung. Coba lagi.*",
        'dl_notmember': "🔔 *Gabung dulu:* {names}\n\nGunakan /start untuk verifikasi.",
        'dl_1': "⏳ *Mengunduh...* `[1/3]`",
        'dl_2': "⚙️ *Memproses...* `[2/3]`",
        'dl_3': "📤 *Mengunggah...* `[3/3]`",
        'dl_done': "✅ *Download selesai!*\n\n🔗 Link: `{link}`\n\n👨💻 Dibuat ❤️ oleh RASHD ( @v4zrasehd )",
        'about': "💜 *Dibuat ❤️ oleh RASHD ( @v4zrasehd )*\n\n⚡ Toko APK + bot download.\n🆓 Gratis · cepat · tanpa iklan.",
        'profile': "👤 *Profil Anda*\n\nNama: `{name}`\nID: `{uid}`\nUsername: @{uname}\nBahasa: {lang}\n\n✅ Terverifikasi!",
        'btn_download': "📥 Download",
        'btn_channel': "📢 Channel",
        'btn_about': "👨‍💻 Tentang",
        'btn_language': "🌐 Bahasa",
        'btn_openstore': "🛒 Toko",
        'btn_verify': "✅ Verifikasi",
        'btn_profile': "🌐 Ganti bahasa",
    },
    'zh': {
        'welcome': (
            "🤖 *RASHD 应用商店*\n"
            "━━━━━━━━━━━━━━━━━\n\n"
            "👋 *欢迎，{name}!*\n\n"
            "📱 *魔法 Mod APK* — 已解锁、无广告\n"
            "⚡ *更新快速*\n"
            "🆓 *100% 免费*\n"
            "📥 *智能下载器*\n\n"
            "👉 *点击下方按钮开始:*"
        ),
        'join_title': "🚫 *请先加入我们的频道!*\n\n您需要加入以下频道:\n\n",
        'join_prompt': "\n\n✅ *加入后点击验证:*",
        'verify_ok': "✅ *验证成功!*\n\n点击下方开始:",
        'choose_lang': "🗣️ *请选择您的语言:*",
        'not_joined': "⚠️ 还未加入: {names}",
        'channel_menu': "📢 *我们的频道*\n\n加入频道:",
        'dl_menu': "📥 *下载专区*\n\n发送支持的链接:\n`/download <url>`\n\n🔗 *支持:* YouTube, TikTok, Instagram, X, Facebook, Reddit.",
        'dl_usage': "📥 *使用说明:*\n\n发送链接:\n`/download https://youtube.com/watch?v=...`",
        'dl_invalid': "❌ *链接无效或平台不支持。请重试。*",
        'dl_notmember': "🔔 *请先加入:* {names}\n\n使用 /start 验证。",
        'dl_1': "⏳ *正在下载...* `[1/3]`",
        'dl_2': "⚙️ *正在处理...* `[2/3]`",
        'dl_3': "📤 *正在上传...* `[3/3]`",
        'dl_done': "✅ *下载完成!*\n\n🔗 链接: `{link}`\n\n👨💻 由 RASHD ( @v4zrasehd ) ❤️ 制作",
        'about': "💜 *由 RASHD ( @v4zrasehd ) 制作*❤️\n\n⚡ Premium APK 商店和智能下载机器人。\n🆓 永远免费 · 更新快 · 无广告。",
        'profile': "👤 *您的个人资料*\n\n姓名: `{name}`\nID: `{uid}`\n用户名: @{uname}\n语言: {lang}\n\n✅ 已验证!",
        'btn_download': "📥 下载",
        'btn_channel': "📢 频道",
        'btn_about': "👨‍💻 关于",
        'btn_language': "🌐 语言",
        'btn_openstore': "🛒 商店",
        'btn_verify': "✅ 验证",
        'btn_profile': "🌐 更换语言",
    },
}

# একটি শব্দ হেল্পার: usuarios language অনুযায়ী string।
def T(lang, key, **kw):
    s = STRINGS.get(lang, STRINGS['en']).get(key, STRINGS['en'].get(key, key))
    try:
        return s.format(**kw)
    except Exception:
        return s

# ==========================================
# 🛠️ HELPER FUNCTIONS
# ==========================================

def get_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def get_lang(uid):
    return get_users().get(str(uid), {}).get('lang')

def set_lang(uid, code):
    users = get_users()
    key = str(uid)
    info = users.get(key, {'name': '', 'username': ''})
    info['lang'] = code
    users[key] = info
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def save_user(uid, user_info):
    users = get_users()
    key = str(uid)
    if key not in users:
        users[key] = user_info
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

def remove_user(uid):
    users = get_users()
    key = str(uid)
    if key in users:
        del users[key]
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
        return True
    return False

async def is_member(bot, uid, channel_username):
    try:
        member = await bot.get_chat_member(chat_id=channel_username, user_id=uid)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return False

async def check_all_channels(bot, uid):
    miss = []
    for c in CHANNELS:
        if not await is_member(bot, uid, c['user']):
            miss.append(c)
    return miss

async def notify_admin(bot, user):
    name = user.first_name or ''
    if user.last_name:
        name += f" {user.last_name}"
    uname = user.username or 'N/A'
    text = (
        "🚨 *New User Started/Verified Bot!*\n\n"
        f"👤 *Name:* `{name}`\n"
        f"🆔 *User ID:* `{user.id}`\n"
        f"🌐 *Username:* @{uname}"
    )
    try:
        await bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode='Markdown')
    except Exception as e:
        print(f"Error notifying admin: {e}")

def validate_url(text):
    if not text or not URL_PATTERN.match(text.strip()):
        return False
    host = re.sub(r'^(https?|ftp)://(www\.)?', '', text.strip()).split('/')[0].lower()
    return any(s in host for s in SUPPORTED_HOSTS)

def first_name(user):
    return user.first_name or 'User'

# ==========================================
# 📝 LANGUAGE SELECTOR
# ==========================================

def language_keyboard(prefer=None):
    rows = []
    for code in LANG_ORDER:
        info = LANGS[code]
        mark = ' ✅' if code == prefer else ''
        rows.append([InlineKeyboardButton(info['flag'] + ' ' + info['name'] + mark, callback_data='lang:' + code)])
    return InlineKeyboardMarkup(rows)

def welcome_keyboard(lang):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(T(lang, 'btn_download'), callback_data='dl'),
         InlineKeyboardButton(T(lang, 'btn_channel'), callback_data='channel')],
        [InlineKeyboardButton(T(lang, 'btn_about'), callback_data='about'),
         InlineKeyboardButton(T(lang, 'btn_language'), callback_data='change_lang')],
        [InlineKeyboardButton(T(lang, 'btn_openstore'), web_app=WebAppInfo(url=WEB_APP_URL))],
    ])

# Telegram ভাষা auto detect
def detect_lang(user):
    code = (user.language_code or 'en').lower().split('-')[0]
    return TELEGRAM_LANG_MAP.get(code, 'en')

# ==========================================
# 📩 HANDLERS
# ==========================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bot = context.bot

    miss = await check_all_channels(bot, user.id)
    if miss:
        lang = get_lang(user.id) or detect_lang(user)
        text = T(lang, 'join_title')
        keyboard = []
        for c in miss:
            text += f"▫️ *{c['name']}*\n"
            keyboard.append([InlineKeyboardButton(f"📢 Join {c['name']}", url=c['link'])])
        text += T(lang, 'join_prompt')
        keyboard.append([InlineKeyboardButton(T(lang, 'btn_verify'), callback_data='verify')])
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
        return

    save_user(user.id, {'name': first_name(user), 'username': user.username or ''})
    lang = get_lang(user.id)

    if not lang:
        # প্রথম বার → ভাষা বাছাই
        choose = T(detect_lang(user), 'choose_lang')
        await update.message.reply_text(
            choose,
            parse_mode='Markdown',
            reply_markup=language_keyboard(detect_lang(user))
        )
    else:
        await update.message.reply_text(
            T(lang, 'welcome', name=first_name(user)),
            parse_mode='Markdown',
            reply_markup=welcome_keyboard(lang)
        )
        await notify_admin(bot, user)

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = get_lang(user.id) or 'en'
    await update.message.reply_text(T(lang, 'about'), parse_mode='Markdown')

async def download_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bot = context.bot
    args = context.args
    lang = get_lang(user.id) or 'en'

    if not args:
        await update.message.reply_text(T(lang, 'dl_usage'), parse_mode='Markdown')
        return

    link = args[0]

    miss = await check_all_channels(bot, user.id)
    if miss:
        names = ", ".join([c['name'] for c in miss])
        await update.message.reply_text(
            T(lang, 'dl_notmember', names=names),
            parse_mode='Markdown'
        )
        return

    if not validate_url(link):
        await update.message.reply_text(T(lang, 'dl_invalid'), parse_mode='Markdown')
        return

    status = await update.message.reply_text(T(lang, 'dl_1'), parse_mode='Markdown')
    try:
        await asyncio.sleep(1.5)
        await status.edit_text(T(lang, 'dl_2'), parse_mode='Markdown')
        await asyncio.sleep(1.5)
        await status.edit_text(T(lang, 'dl_3'), parse_mode='Markdown')
        await asyncio.sleep(1)
        await status.edit_text(T(lang, 'dl_done', link=link), parse_mode='Markdown')
    except Exception as e:
        print(f"Download error: {e}")
        await status.edit_text(T(lang, 'dl_invalid'), parse_mode='Markdown')

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    users = get_users()
    total = len(users)
    text = (
        "👑 *Admin Control Panel*\n\n"
        f"📊 Total Users: *{total}*\n\n"
        "নিচের বাটন চেপে কার্যক্রম পরিচালনা করুন:"
    )
    keyboard = [
        [InlineKeyboardButton("👥 View Users", callback_data="adm_users")],
        [InlineKeyboardButton("📢 Broadcast Help", callback_data="adm_broadcast_help")],
        [InlineKeyboardButton("❌ Remove User Help", callback_data="adm_remove_help")],
        [InlineKeyboardButton("👥 Languages Used", callback_data="adm_langs")]
    ]
    await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    text_to_send = update.message.text[11:].strip()
    if not text_to_send:
        await update.message.reply_text("❌ পাঠানোর জন্য মেসেজ লিখুন। উদাহরণ: `/broadcast Hello`", parse_mode='Markdown')
        return

    users = get_users()
    sent = 0
    for uid in users:
        try:
            await context.bot.send_message(chat_id=int(uid), text=text_to_send)
            sent += 1
        except Exception:
            pass

    await update.message.reply_text(f"✅ Broadcast sent to {sent} users!")

async def remove_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    target_id = update.message.text[8:].strip()
    if remove_user(target_id):
        await update.message.reply_text(f"✅ User `{target_id}` removed from bot database!", parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ User ID not found.")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    chat_id = query.message.chat.id
    data = query.data
    bot = context.bot

    await query.answer()

    # 🌐 Language selection
    if data.startswith('lang:'):
        code = data.split(':')[1]
        if code not in LANGS:
            return
        set_lang(user.id, code)
        # auto save user record
        save_user(user.id, {'name': user.first_name or '', 'username': user.username or ''})
        await query.edit_message_text(
            T(code, 'welcome', name=first_name(user)),
            parse_mode='Markdown',
            reply_markup=welcome_keyboard(code)
        )
        await notify_admin(bot, user)
        return

    if data == 'change_lang':
        lang = get_lang(user.id) or detect_lang(user)
        await query.edit_message_text(
            T(lang, 'choose_lang'),
            parse_mode='Markdown',
            reply_markup=language_keyboard(detect_lang(user))
        )
        return

    lang = get_lang(user.id) or 'en'

    if data == "verify":
        miss = await check_all_channels(bot, user.id)
        if not miss:
            save_user(user.id, {'name': user.first_name or '', 'username': user.username or ''})
            if get_lang(user.id):
                await query.edit_message_text(
                    T(lang, 'welcome', name=first_name(user)),
                    parse_mode='Markdown',
                    reply_markup=welcome_keyboard(lang)
                )
                await notify_admin(bot, user)
            else:
                await query.edit_message_text(
                    T(detect_lang(user), 'choose_lang'),
                    parse_mode='Markdown',
                    reply_markup=language_keyboard(detect_lang(user))
                )
        else:
            names = ", ".join([c['name'] for c in miss])
            await query.answer(T(lang, 'not_joined', names=names), show_alert=True)
        return

    if data == "dl":
        await bot.send_message(
            chat_id=chat_id,
            text=T(lang, 'dl_menu'),
            parse_mode='Markdown',
            reply_markup=welcome_keyboard(lang)
        )
    elif data == "channel":
        text = T(lang, 'channel_menu')
        keyboard = [[InlineKeyboardButton(f"📢 Join {c['name']}", url=c['link'])] for c in CHANNELS]
        await bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "about":
        await bot.send_message(chat_id=chat_id, text=T(lang, 'about'), parse_mode='Markdown')
    elif data == "profile":
        name = user.first_name or ''
        if user.last_name:
            name += f" {user.last_name}"
        uname = user.username or 'N/A'
        langname = LANGS.get(lang, {}).get('flag', '') + ' ' + LANGS.get(lang, {}).get('name', lang)
        await bot.send_message(
            chat_id=chat_id,
            text=T(lang, 'profile', name=name, uid=user.id, uname=uname, lang=langname),
            parse_mode='Markdown'
        )
    elif user.id == ADMIN_ID:
        if data == "adm_users":
            users = get_users()
            list_text = "👥 *Registered Users:*\n\n"
            for uid, info in users.items():
                uname = f"@{info['username']}" if info.get('username') else "No Username"
                langcode = info.get('lang', '?')
                list_text += f"• `{uid}` | {uname} | 🌐 {langcode}\n"
            await bot.send_message(chat_id=chat_id, text=list_text, parse_mode='Markdown')

        elif data == "adm_langs":
            users = get_users()
            count = {}
            for info in users.values():
                c = info.get('lang', 'unknown')
                count[c] = count.get(c, 0) + 1
            text = "🌐 *Language Stats*\n\n"
            for k, v in sorted(count.items(), key=lambda x: -x[1]):
                text += f"• {LANGS.get(k,{}).get('name', k)} — *{v}*\n"
            await bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')

        elif data == "adm_broadcast_help":
            text = (
                "📢 *Broadcast Guide*\n\n"
                "সব ইউজারকে একসাথে মেসেজ পাঠাতে টাইপ করুন:\n"
                "`/broadcast আপনার কথা এখানে লিখুন`"
            )
            await bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')

        elif data == "adm_remove_help":
            text = (
                "❌ *Remove User Guide*\n\n"
                "কোনো ইউজার রিমুভ করতে টাইপ করুন:\n"
                "`/remove 123456789` (ইউজার আইডি)"
            )
            await bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')

# 📢 চ্যানেল পোস্ট ব্রডকাস্ট
async def channel_post_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post = update.channel_post
    if not post:
        return
    users = get_users()
    for uid in users:
        try:
            await context.bot.forward_message(
                chat_id=int(uid),
                from_chat_id=post.chat.id,
                message_id=post.message_id
            )
        except Exception:
            pass

# ==========================================
# 🚀 MAIN FUNCTION
# ==========================================

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("about", about_command))
    app.add_handler(CommandHandler("download", download_command))
    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("remove", remove_command))

    app.add_handler(CallbackQueryHandler(callback_handler))

    app.add_handler(MessageHandler(filters.ChatType.CHANNEL, channel_post_handler))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()