import os
import random
from datetime import datetime, timedelta
from khayyam import JalaliDatetime
import pytz
import requests
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.enums import ChatType, UserStatus
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app

# 📅 دریافت تاریخ امروز
def get_date_formats():
    now = datetime.now(pytz.timezone("Asia/Tehran"))
    jalali_date = JalaliDatetime.now().strftime("%Y/%m/%d")
    gregorian_date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    return jalali_date, gregorian_date, time

# 📥 دانلود تصویر از URL
def download_image(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, "wb") as f:
            f.write(response.content)
    return path

# 🌹 دستور زوج
@app.on_message(filters.command(["زوج"]) & ~filters.private)
async def select_couple(_, message):
    chat_id = message.chat.id
    args = message.text.split()

    # فقط در گروه‌ها فعال است
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("❌ این دستور فقط در گروه‌ها فعال است.")

    # مسیر ذخیره تصاویر
    p1_path = "downloads/p1.png"
    p2_path = "downloads/p2.png"
    result_path = f"downloads/love_result_{chat_id}.png"
    bg_path = "downloads/background_love.png"

    # تاریخ
    jalali_date, gregorian_date, current_time = get_date_formats()

    try:
        # بررسی آرگومان‌ها (با یا بدون آیدی)
        if len(args) >= 3:
            user1_id = int(args[1].replace("@", ""))
            user2_id = int(args[2].replace("@", ""))
            custom_text = " ".join(args[3:]) if len(args) > 3 else None
            user1 = await app.get_users(user1_id)
            user2 = await app.get_users(user2_id)
        else:
            # انتخاب کاربران آنلاین
            members = []
            async for member in app.get_chat_members(chat_id, limit=100):
                if (
                    not member.user.is_bot
                    and not member.user.is_deleted
                    and member.status == UserStatus.ONLINE
                ):
                    members.append(member.user)

            if len(members) < 2:
                return await message.reply_text("❌ کاربران کافی برای انتخاب وجود ندارد.")

            user1, user2 = random.sample(members, 2)
            custom_text = None

        # دانلود تصاویر پروفایل
        try:
            photo1 = await app.download_media(user1.photo.big_file_id, file_name=p1_path)
        except Exception:
            photo1 = download_image("https://telegra.ph/file/05aa686cf52fc666184bf.jpg", p1_path)

        try:
            photo2 = await app.download_media(user2.photo.big_file_id, file_name=p2_path)
        except Exception:
            photo2 = download_image("https://telegra.ph/file/05aa686cf52fc666184bf.jpg", p2_path)

        # آماده‌سازی تصویر زوج
        img1 = Image.open(photo1).resize((400, 400)).convert("RGBA")
        img2 = Image.open(photo2).resize((400, 400)).convert("RGBA")

        # پس‌زمینه
        bg_url = "https://telegra.ph/file/96f36504f149e5680741a.jpg"
        bg_path = download_image(bg_url, bg_path)
        background = Image.open(bg_path).convert("RGBA")

        # ترکیب تصاویر
        mask = Image.new("L", (400, 400), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 400, 400), fill=255)

        img1.putalpha(mask)
        img2.putalpha(mask)

        background.paste(img1, (150, 150), img1)
        background.paste(img2, (600, 150), img2)

        # اضافه کردن متن عاشقانه
        draw = ImageDraw.Draw(background)
        try:
            font = ImageFont.truetype("arial.ttf", 50)
        except IOError:
            font = ImageFont.load_default()

        # متن عاشقانه
        love_text = custom_text or f"""
💖 زوج عاشقانه امروز:

{user1.first_name} (tg://user?id={user1.id}) + {user2.first_name} (tg://user?id={user2.id})

📅 تاریخ شروع عشق:
🕰 ساعت: {current_time}
📆 شمسی: {jalali_date}
📅 میلادی: {gregorian_date}

✨ عشق همیشگی 💘
        """

        # نوشتن متن روی تصویر
        text_position = (background.width // 4, background.height - 200)
        draw.text(text_position, love_text, font=font, fill="white")

        # ذخیره تصویر نتیجه
        background.save(result_path)

        # ارسال تصویر و پیام
        await message.reply_photo(
            photo=result_path,
            caption=love_text,
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
