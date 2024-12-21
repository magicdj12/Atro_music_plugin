import os
import random
from datetime import datetime
from khayyam import JalaliDatetime
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.enums import ChatType, UserStatus
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app

# لیست اشعار عاشقانه
love_poems = [
    "تو با قلب ویرانه‌ی من چه کردی؟\nببین عشق دیوانه‌ی من چه کردی؟",
    "بهترین لحظه‌ام، همین حالاست\nکه تو باشی کنار من، جانم.",
    "عشق یعنی نگاه تو، یعنی آرامش وجودم.",
    # سایر اشعار...
]

# دریافت تاریخ و زمان
def get_date_formats():
    now = datetime.now()
    jalali_date = JalaliDatetime.now().strftime("%Y/%m/%d")
    gregorian_date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    return jalali_date, gregorian_date, time

# ایجاد پس‌زمینه و ترکیب تصویر
def create_couple_image(user1_name, user2_name, photo1_path, photo2_path, custom_text=None):
    background = Image.new("RGB", (1200, 800), (30, 30, 50))
    draw = ImageDraw.Draw(background)

    # اضافه کردن تصاویر کاربران
    if photo1_path:
        img1 = Image.open(photo1_path).resize((300, 300)).convert("RGBA")
        mask = Image.new("L", (300, 300), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, 300, 300), fill=255)
        img1.putalpha(mask)
        background.paste(img1, (200, 250), img1)

    if photo2_path:
        img2 = Image.open(photo2_path).resize((300, 300)).convert("RGBA")
        mask = Image.new("L", (300, 300), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, 300, 300), fill=255)
        img2.putalpha(mask)
        background.paste(img2, (700, 250), img2)

    # اضافه کردن اسم کاربران
    font = ImageFont.truetype("arial.ttf", 40)
    draw.text((250, 580), user1_name, fill="white", font=font)
    draw.text((750, 580), user2_name, fill="white", font=font)

    # اضافه کردن متن انتخابی یا شعر عاشقانه
    if custom_text:
        draw.text((150, 700), custom_text, fill="white", font=font)
    else:
        poem = random.choice(love_poems)
        draw.text((150, 700), poem, fill="white", font=font)

    # ذخیره تصویر
    result_path = f"downloads/couple_result.png"
    background.save(result_path)
    return result_path

# دستور زوج تصادفی
@app.on_message(filters.regex(r"^(زوج|Zoj|zoj)$") & ~filters.private)
async def random_couple(_, message):
    chat_id = message.chat.id
    try:
        members = []
        async for member in app.get_chat_members(chat_id, limit=100):
            if not member.user.is_bot and member.status in [UserStatus.ONLINE, UserStatus.RECENTLY]:
                members.append(member.user)

        if len(members) < 2:
            return await message.reply_text("❌ تعداد کاربران کافی نیست.")

        user1, user2 = random.sample(members, 2)
        photo1_path = await app.download_media(user1.photo.big_file_id) if user1.photo else None
        photo2_path = await app.download_media(user2.photo.big_file_id) if user2.photo else None

        result_image = create_couple_image(user1.first_name, user2.first_name, photo1_path, photo2_path)
        jalali_date, gregorian_date, current_time = get_date_formats()

        await message.reply_photo(
            photo=result_image,
            caption=(
                f"💞 زوج امروز:\n👩 {user1.mention} + 👦 {user2.mention}\n\n"
                f"📅 تاریخ شمسی: {jalali_date}\n"
                f"📆 تاریخ میلادی: {gregorian_date}\n"
                f"🕒 ساعت: {current_time}\n\n"
                f"🌹 یک شعر عاشقانه:\n{random.choice(love_poems)}"
            ),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("✨ منو به گروهت اضافه کن", url=f"https://t.me/{app.username}?startgroup=true")]]
            ),
        )
        except Exception as e:
            pass
# دستور زوج انتخابی
@app.on_message(filters.regex(r"^(زوج)\s+(\d+|\@[\w\d]+)\s+(\d+|\@[\w\d]+)(.*)?$") & ~filters.private)
async def chosen_couple(_, message):
    try:
        args = message.text.split()
        user1 = await app.get_users(args[1])
        user2 = await app.get_users(args[2])
        custom_text = args[3] if len(args) > 3 else None

        photo1_path = await app.download_media(user1.photo.big_file_id) if user1.photo else None
        photo2_path = await app.download_media(user2.photo.big_file_id) if user2.photo else None

        result_image = create_couple_image(user1.first_name, user2.first_name, photo1_path, photo2_path, custom_text)
        jalali_date, gregorian_date, current_time = get_date_formats()

        await message.reply_photo(
            photo=result_image,
            caption=(
                f"💞 زوج انتخابی:\n👩 {user1.mention} + 👦 {user2.mention}\n\n"
                f"📅 تاریخ شمسی: {jalali_date}\n"
                f"📆 تاریخ میلادی: {gregorian_date}\n"
                f"🕒 ساعت: {current_time}\n\n"
                f"🌹 یک شعر عاشقانه:\n{custom_text if custom_text else random.choice(love_poems)}"
            ),
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("✨ منو به گروهت اضافه کن", url=f"https://t.me/{app.username}?startgroup=true")]]
            ),
        )
    except Exception as e:
        await message.reply_text(f"⚠️ خطا: {e}")
