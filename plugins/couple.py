import os
import random
from datetime import datetime, timedelta
import pytz
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app

# دریافت تاریخ میلادی و شمسی
def get_datetime_info():
    timezone = pytz.timezone("Asia/Tehran")
    now = datetime.now(timezone)
    jalali_date = now.strftime("%Y/%m/%d")
    gregorian_date = now.strftime("%d %B %Y")
    time_now = now.strftime("%H:%M:%S")
    return jalali_date, gregorian_date, time_now

# ذخیره عکس پروفایل به صورت موقت
def download_image(url, path):
    import requests
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, "wb") as f:
            f.write(response.content)
    return path

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

        # متن‌های عاشقانه
        draw = ImageDraw.Draw(background)
        try:
            font = ImageFont.truetype("arial.ttf", 50)
        except IOError:
            font = ImageFont.load_default()

        text = "🌸 زوج خوشبخت امروز 🌸"
        draw.text((200, 50), text, font=font, fill="white")

        jalali_date, gregorian_date, time_now = get_datetime_info()
        draw.text((50, 600), f"📅 تاریخ شمسی: {jalali_date}", font=font, fill="white")
        draw.text((50, 650), f"📅 تاریخ میلادی: {gregorian_date}", font=font, fill="white")
        draw.text((50, 700), f"⏰ ساعت: {time_now}", font=font, fill="white")

        # ذخیره تصویر
        result_path = f"downloads/result_{chat_id}.png"
        background.save(result_path)

        # ارسال پیام با تصویر
        caption = f"""
        🌟 زوج امروز گروه:

        {user1.first_name} (tg://user?id={user1.id}) ❤️ {user2.first_name} (tg://user?id={user2.id})

            🌸 برای روزهای خوشبختی!
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
