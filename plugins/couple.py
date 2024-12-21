import os
import random
from datetime import datetime
import pytz
import requests
from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# 📅 دریافت تاریخ و ساعت
def get_dates():
    timezone = pytz.timezone("Asia/Tehran")
    now = datetime.now(timezone)
    jalali_date = now.strftime("%Y/%m/%d")  # تاریخ شمسی
    gregorian_date = now.strftime("%d %B %Y")
    time = now.strftime("%H:%M:%S")
    return jalali_date, gregorian_date, time

# 📥 دانلود تصویر از آدرس اینترنتی
def download_image(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, "wb") as f:
            f.write(response.content)
    return path

# 📜 لیست ۳۰ شعر عاشقانه
poems = [
    "✨ تو شعر زندگی منی.", "🌹 عشق تو دلیل تپش قلبم است.", "💫 با تو زندگی رنگ دیگری دارد.",
    "❤️ تو آفتاب روزهای بارانی منی.", "✨ بدون تو، دنیا تاریک است.", "💖 هر لحظه با تو، یک عمر خوشبختی است.",
    "🌷 تو بهار قلب منی.", "💎 تو گنج بی‌همتای منی.", "🌙 تو ماه شب‌های تاریک منی.",
    "🌟 دنیایم با لبخند تو روشن می‌شود.", "🌸 عشق تو چون گلی در باغ دلم شکفته است.",
    "✨ هر روز با تو یک رؤیای تازه است.", "❤️ قلبم تنها برای تو می‌تپد.",
    "💐 تو زیباترین هدیه زندگی منی.", "🕊️ عشق تو آزادی روح من است.", "💛 با تو جهان من کامل است.",
    "🌈 تو رنگین‌کمان روزهای بارانی منی.", "🎵 صدای قلبت، زیباترین موسیقی دنیا است.",
    "🌺 زندگی بدون تو مانند باغی بدون گل است.", "❤️ تو دلیل خوشبختی منی.",
    "✨ هر لحظه با تو ارزش یک دنیا را دارد.", "💫 تو خورشید گرمابخش زمستان منی.",
    "🌷 قلبم برای همیشه مال تو است.", "💖 عشق تو آتشی است که خاموش نمی‌شود.",
    "🌟 تو تنها دلیل زنده بودنم هستی.", "💐 هر نگاهت، یک شعر عاشقانه است.",
    "🌹 عشق تو زندگی‌ام را معنا می‌بخشد.", "🕊️ با تو، زندگی یک سفر زیبا است.",
    "💛 هر لبخند تو، طلوعی جدید است.", "🌈 تو رؤیای شب‌های منی."
]

# 🎲 دستور زوج تصادفی
@app.on_message(filters.command(["زوج", "couple"]) & ~filters.private)
async def select_couple(_, message):
    chat_id = message.chat.id

    # دستور فقط در گروه‌ها فعال باشد
    if message.chat.type == "private":
        return await message.reply_text("❌ این دستور فقط در گروه‌ها فعال است.")

    # مسیر ذخیره تصاویر
    p1_path = "downloads/p1.png"
    p2_path = "downloads/p2.png"
    result_path = f"downloads/result_{chat_id}.png"
    bg_path = "downloads/background.png"

    try:
        # انتخاب اعضای گروه
        members = []
        async for member in app.get_chat_members(chat_id):
            if not member.user.is_bot and not member.user.is_deleted:
                members.append(member.user)

        if len(members) < 2:
            return await message.reply_text("❌ اعضای کافی برای انتخاب وجود ندارد.")  # پیام فقط در صورتی که کمتر از ۲ نفر وجود دارد

        # انتخاب دو کاربر تصادفی
        user1 = random.choice(members)
        user2 = random.choice(members)
        while user1.id == user2.id:
            user2 = random.choice(members)

        # دانلود تصاویر کاربران
        try:
            photo1 = await app.download_media(user1.photo.big_file_id, file_name=p1_path)
        except:
            photo1 = download_image("https://telegra.ph/file/05aa686cf52fc666184bf.jpg", p1_path)

        try:
            photo2 = await app.download_media(user2.photo.big_file_id, file_name=p2_path)
        except:
            photo2 = download_image("https://telegra.ph/file/05aa686cf52fc666184bf.jpg", p2_path)

        # پس‌زمینه
        bg_url = "https://telegra.ph/file/96f36504f149e5680741a.jpg"
        bg_path = download_image(bg_url, bg_path)
        background = Image.open(bg_path).convert("RGBA")

        # آماده‌سازی تصاویر
        img1 = Image.open(photo1).resize((400, 400)).convert("RGBA")
        img2 = Image.open(photo2).resize((400, 400)).convert("RGBA")

        # ماسک دایره‌ای برای تصاویر
        mask = Image.new("L", (400, 400), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 400, 400), fill=255)

        img1.putalpha(mask)
        img2.putalpha(mask)

# قرار دادن تصاویر روی پس‌زمینه
        background.paste(img1, (150, 150), img1)
        background.paste(img2, (600, 150), img2)

        # اضافه کردن نام کاربران دور تصاویر
        draw = ImageDraw.Draw(background)
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            font = ImageFont.load_default()

        draw.text((200, 570), f"@{user1.username}" if user1.username else user1.first_name, font=font, fill="white")
        draw.text((650, 570), f"@{user2.username}" if user2.username else user2.first_name, font=font, fill="white")

        # ذخیره تصویر نهایی
        background.save(result_path)

        # تاریخ و زمان
        jalali_date, gregorian_date, time = get_dates()

        # انتخاب شعر تصادفی
        poem = random.choice(poems)

        # کپشن نهایی
        caption = f"""
🌟 زوج امروز گروه:

@{user1.username} ❤️ @{user2.username}

📅 تاریخ شمسی: {jalali_date}
📅 تاریخ میلادی: {gregorian_date}
⏰ ساعت: {time}

✨ {poem}
        """

        # ارسال تصویر
        await message.reply_photo(
            photo=result_path,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("✨ اضافه کردن من به گروه", url=f"https://t.me/{app.username}?startgroup=true")]]
            ),
        )
    except Exception as e:
        await message.reply_text(f"⚠️ خطا: {e}")
    finally:
        # حذف فایل‌های موقت
        for path in [p1_path, p2_path, result_path, bg_path]:
            if os.path.exists(path):
                os.remove(path)
