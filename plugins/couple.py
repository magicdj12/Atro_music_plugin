import os
import random
from datetime import datetime
import pytz
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app

# لیست اشعار عاشقانه
poems = [
    "تو شعر زندگی منی.",
    "زندگی با تو یعنی بهشت.",
    "تو آرامش دل منی.",
    "با تو دنیا زیباتره.",
    "تو نبض قلب منی.",
    "عشق یعنی نام تو.",
    "تو خورشید زندگی منی.",
    "زندگی بدون تو بی‌رنگ است.",
    "قلبم برای تو می‌تپد.",
    "تو آرزوی هر شب منی.",
    "در نگاه تو زندگی را یافتم.",
    "تو دریای آرامش منی.",
    "زندگی با عشق تو زیباست.",
    "با تو هر لحظه‌ام خوشبختی است.",
    "تو صدای قلب منی.",
    "با تو بودن، رویای من است.",
    "عشق تو دلیل تپش قلبم است.",
    "با تو، همه چیز کامل است.",
    "هر لحظه با تو، بهشت است.",
    "تو نور زندگی منی.",
    "با تو، دنیا زیباتر می‌شود.",
    "قلبم تنها برای تو می‌تپد.",
    "عشق تو، زندگی‌ام را روشن کرده.",
    "با تو، زندگی معنای دیگری دارد.",
    "تو امید هر روز منی.",
    "قلب من برای تو می‌تپد.",
    "تو شاهکار زندگی منی.",
    "با تو، همه چیز زیباست.",
    "تو دلیل خوشبختی منی.",
]

# دریافت تاریخ و زمان فعلی
def get_datetime_info():
    now = datetime.now(pytz.timezone("Asia/Tehran"))
    jalali_date = now.strftime("%Y/%m/%d")
    gregorian_date = now.strftime("%d %B %Y")
    time_now = now.strftime("%H:%M:%S")
    return jalali_date, gregorian_date, time_now

# دایره‌ای کردن تصاویر
def circle_image(image_path, size):
    image = Image.open(image_path).resize(size).convert("RGBA")
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    output = ImageOps.fit(image, size, centering=(0.5, 0.5))
    output.putalpha(mask)
    return output

# دستور زوج
@app.on_message(filters.command("زوج") & ~filters.private)
async def select_couple(_, message):
    chat_id = message.chat.id

    if message.chat.type != ChatType.SUPERGROUP:
        return await message.reply_text("❌ این دستور فقط در گروه‌ها فعال است.")

    members = []
    async for member in app.get_chat_members(chat_id, limit=50):
        if not member.user.is_bot and not member.user.is_deleted:
            members.append(member.user)

    if len(members) < 2:
        return await message.reply_text("❌ اعضای کافی برای انتخاب زوج وجود ندارند.")

    # انتخاب تصادفی کاربران
    user1 = random.choice(members)
    user2 = random.choice(members)
    while user1.id == user2.id:
        user2 = random.choice(members)

    # دانلود تصاویر پروفایل کاربران
    p1_path = f"downloads/{user1.id}.png"
    p2_path = f"downloads/{user2.id}.png"
    try:
        photo1 = await app.download_media(user1.photo.big_file_id, file_name=p1_path)
    except:
        photo1 = "default_profile.png"

    try:
        photo2 = await app.download_media(user2.photo.big_file_id, file_name=p2_path)
    except:
        photo2 = "default_profile.png"

    # ایجاد پس‌زمینه
    bg_url = "https://telegra.ph/file/96f36504f149e5680741a.jpg"
    bg_path = "downloads/background.jpg"
    background = Image.open(bg_url).convert("RGBA")

    # تصاویر پروفایل کاربران به‌صورت دایره‌ای
    img1 = circle_image(photo1, (200, 200))
    img2 = circle_image(photo2, (200, 200))

    # اضافه کردن تصاویر به پس‌زمینه
    background.paste(img1, (150, 200), img1)
    background.paste(img2, (600, 200), img2)

    # اضافه کردن نام کاربران
    draw = ImageDraw.Draw(background)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    # نام کاربران دور عکس پروفایل
    draw.text((150, 420), user1.first_name, font=font, fill="white")
    draw.text((600, 420), user2.first_name, font=font, fill="white")

    # تاریخ و ساعت
    jalali_date, gregorian_date, time_now = get_datetime_info()
    draw.text((50, 600), f"📅 تاریخ شمسی: {jalali_date}", font=font, fill="white")
    draw.text((50, 650), f"📅 تاریخ میلادی: {gregorian_date}", font=font, fill="white")
    draw.text((50, 700), f"⏰ ساعت: {time_now}", font=font, fill="white")

# ذخیره تصویر نهایی
    result_path = f"downloads/result_{chat_id}.png"
    background.save(result_path)

    # انتخاب شعر تصادفی
    random_poem = random.choice(poems)

    # کپشن نهایی
    caption = f"""
🌟 زوج امروز گروه:

{user1.first_name} (tg://user?id={user1.id}) ❤️ {user2.first_name} (tg://user?id={user2.id})

📅 تاریخ شمسی: {jalali_date}
📅 تاریخ میلادی: {gregorian_date}
⏰ ساعت: {time_now}

✨ {random_poem}
"""

    # ارسال تصویر
    await message.reply_photo(
        photo=result_path,
        caption=caption,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✨ اضافه کردن من به گروه", url=f"https://t.me/{app.username}?startgroup=true")]]
        ),
    )

    # حذف فایل‌های موقت
    for path in [p1_path, p2_path, result_path]:
        if os.path.exists(path):
            os.remove(path)
