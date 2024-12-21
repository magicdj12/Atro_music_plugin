import os
import random
from datetime import datetime, timedelta
import pytz
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app

# 📅 دریافت تاریخ و زمان
def get_datetime_info():
    timezone = pytz.timezone("Asia/Tehran")
    now = datetime.now(timezone)
    jalali_date = now.strftime("%Y/%m/%d")  # جایگزین با ماژول‌های تقویم شمسی (مثل khayyam) در صورت نیاز
    gregorian_date = now.strftime("%d %B %Y")
    time_now = now.strftime("%H:%M:%S")
    return jalali_date, gregorian_date, time_now

# 📥 دانلود تصویر از URL
def download_image(url, path):
    import requests
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, "wb") as f:
            f.write(response.content)
    return path

# 🎲 لیست اشعار عاشقانه
poems = [
    "✨ تو شعر زندگی منی.",
    "💞 عشق یعنی تو، یعنی ما.",
    "🌹 دنیای من با تو زیباست.",
    "❤️ قلبم تنها با تو می‌تپد.",
    "🎵 آهنگ زندگی منی.",
    "🌺 هر لحظه کنار تو بهشت است.",
    "🔥 گرمای عشق تو زندگی‌ام را روشن می‌کند.",
    "💖 تو در قلبم همیشه خواهی ماند.",
    "💎 با تو همه‌چیز زیباتر است.",
    "🌟 ستاره‌های شب تنها با نگاه تو معنا دارند.",
    "🌷 تو گل سرسبد عشق منی.",
    "💞 با تو دنیا زیباتر است.",
    "🌈 زندگی بدون تو رنگی ندارد.",
    "🌻 خورشید قلب من تویی.",
    "💌 نامه عشق من به تو هر روز نوشته می‌شود.",
    "🌙 تو ماه شب‌های تار منی.",
    "💓 تنها در آغوش تو آرام می‌گیرم.",
    "🦋 زندگی‌ام پر از پروانه‌های عشق است، به لطف تو.",
    "🌼 تو باغ آرزوهای منی.",
    "🎉 عشق تو جشن زندگی من است.",
    "✨ نگاهت جادوی لحظه‌های من است.",
    "💞 عشق یعنی تو در کنار من.",
    "🌹 تو گل عشقی که در قلبم شکوفا شده است.",
    "💖 زندگی بدون تو هیچ است.",
    "💎 تو ارزشمندترین دارایی منی.",
    "🔥 تو شعله عشقی که در قلبم می‌سوزد.",
    "🌺 هر لحظه با تو بهشت است.",
    "❤️ تو تنها دلیل لبخند منی.",
    "🌷 تو گل عشقی که در قلبم رشد کرده است.",
    "✨ ستاره‌های شب تنها با نگاه تو معنا دارند."
]

# 🎲 دستور انتخاب زوج
@app.on_message(filters.command("زوج") & ~filters.private)
async def random_couple(_, message):
    chat_id = message.chat.id

    if message.chat.type != ChatType.SUPERGROUP:
        return await message.reply_text("❌ این دستور فقط در گروه‌ها فعال است.")

    try:
        members = []
        async for member in app.get_chat_members(chat_id, limit=100):
            if not member.user.is_bot and not member.user.is_deleted:
                members.append(member.user)

        if len(members) < 2:
            return await message.reply_text("❌ تعداد کاربران کافی نیست.")

        user1 = random.choice(members)
        user2 = random.choice(members)
        while user1.id == user2.id:
            user2 = random.choice(members)

        # دانلود عکس پروفایل کاربران
        p1_path = f"downloads/{user1.id}.jpg"
        p2_path = f"downloads/{user2.id}.jpg"
        try:
            photo1 = await app.download_media(user1.photo.big_file_id, file_name=p1_path)
        except Exception:
            photo1 = download_image("https://telegra.ph/file/05aa686cf52fc666184bf.jpg", p1_path)

        try:
            photo2 = await app.download_media(user2.photo.big_file_id, file_name=p2_path)
        except Exception:
            photo2 = download_image("https://telegra.ph/file/05aa686cf52fc666184bf.jpg", p2_path)

        # پس‌زمینه عاشقانه
        bg_path = "downloads/background.jpg"
        bg_url = "https://telegra.ph/file/96f36504f149e5680741a.jpg"
        download_image(bg_url, bg_path)

        background = Image.open(bg_path).convert("RGBA")
        img1 = Image.open(photo1).resize((400, 400)).convert("RGBA")
        img2 = Image.open(photo2).resize((400, 400)).convert("RGBA")

        # ماسک دایره‌ای
        mask = Image.new("L", (400, 400), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 400, 400), fill=255)

        img1.putalpha(mask)
        img2.putalpha(mask)

# ترکیب تصاویر
        background.paste(img1, (100, 150), img1)
        background.paste(img2, (600, 150), img2)

        # اضافه کردن متن
        draw = ImageDraw.Draw(background)
        try:
            font = ImageFont.truetype("arial.ttf", 50)
        except IOError:
            font = ImageFont.load_default()

        jalali_date, gregorian_date, time_now = get_datetime_info()
        draw.text((50, 50), "🌸 زوج امروز 🌸", font=font, fill="white")
        draw.text((50, 600), f"📅 تاریخ شمسی: {jalali_date}", font=font, fill="white")
        draw.text((50, 650), f"📅 تاریخ میلادی: {gregorian_date}", font=font, fill="white")
        draw.text((50, 700), f"⏰ ساعت: {time_now}", font=font, fill="white")

        # ذخیره تصویر
        result_path = f"downloads/result_{chat_id}.png"
        background.save(result_path)

        # انتخاب شعر تصادفی
        random_poem = random.choice(poems)

        # ارسال پیام با تصویر
        caption = f"""
🌟 زوج امروز گروه:

《{user1.first_name}》 ❤️ 《{user2.first_name}》

📅 تاریخ شمسی: {jalali_date}
📅 تاریخ میلادی: {gregorian_date}
⏰ ساعت: {time_now}

✨ {random_poem}
"""
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
        for path in [p1_path, p2_path, bg_path, result_path]:
            if os.path.exists(path):
                os.remove(path)
