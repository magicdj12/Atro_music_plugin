import os
import random
from datetime import datetime, timedelta
import pytz
import requests
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.enums import ChatType, UserStatus
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from deepface import DeepFace
from YukkiMusic import app

# 📅 تاریخ امروز
def get_today_date():
    timezone = pytz.timezone("Asia/Kolkata")
    now = datetime.now(timezone)
    return now.strftime("%d/%m/%Y")

# 📥 دانلود تصویر از URL
def download_image(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, "wb") as f:
            f.write(response.content)
    return path

# 📜 لیست شعرهای عاشقانه
LOVE_POEMS = [
    "عشق همان جایی است که قلب‌هایمان با هم می‌تپند 💕",
    "نگاهت، آغوشی است که آرامش می‌بخشد ❤️",
    "زندگی با تو رنگین‌کمان شادی‌هاست 🌈",
    "هر لحظه کنار تو، ابدیتی شیرین است 💞",
    "عشق در نگاهت بی‌پایان است، مثل آسمان شب ✨",
    "به قلبت سوگند، دنیا با تو بهشت من است 💘",
    "تو مثل ترانه‌ای هستی که هیچ‌وقت تمام نمی‌شود 🎶",
    "در آغوش تو، جهان زیباترین معنای زندگی است 🌹",
    "آرزوی من فقط یک لبخند توست 🌟",
    "قلبم فقط برای تو می‌تپد، همیشه و تا ابد 💖",
]

# 📅 تاریخ امروز
today = get_today_date()

# 🎨 آماده‌سازی تصویر زوج
def prepare_love_image(user1, user2, photo1, photo2, bg_path, result_path, custom_text=None):
    # آماده‌سازی تصاویر کاربران
    img1 = Image.open(photo1).resize((400, 400)).convert("RGBA")
    img2 = Image.open(photo2).resize((400, 400)).convert("RGBA")

    # پس‌زمینه
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
        font = ImageFont.truetype("Lobster-Regular.ttf", 50)  # فونت زیبا
    except IOError:
        font = ImageFont.load_default()

    # اگر کاربر متنی وارد نکرده باشد، یک شعر تصادفی انتخاب می‌شود
    if not custom_text:
        custom_text = random.choice(LOVE_POEMS)

    # نوشتن متن
    text = f"""
🌹 زوج عاشقانه امروز:

{user1.first_name} (tg://user?id={user1.id}) + {user2.first_name} (tg://user?id={user2.id})

💌 تاریخ: {today}
💖 {custom_text}
    """
    text_position = (background.width // 6, background.height - 300)
    draw.text(text_position, text, font=font, fill="white", align="center")

    # ذخیره تصویر
    background.save(result_path)
    return text

# 🌹 دستور زوج با ایدی
@app.on_message(filters.command("زوج") & ~filters.private)
async def couple_by_ids(_, message):
    args = message.text.split()
    if len(args) < 3:
        return await message.reply_text("❌ لطفاً دستور را به صورت /زوج [ایدی اول] [ایدی دوم] [متن دلخواه] وارد کنید.")

    # ایدی‌ها و متن دلخواه
    user1_id = args[1]
    user2_id = args[2]
    custom_text = " ".join(args[3:]) if len(args) > 3 else None

    try:
        # دریافت اطلاعات کاربران
        user1 = await app.get_users(user1_id)
        user2 = await app.get_users(user2_id)

        # دانلود تصاویر پروفایل
        p1_path = "downloads/p1.png"
        p2_path = "downloads/p2.png"
        bg_path = "downloads/background_love.png"
        result_path = "downloads/love_result.png"

        try:
            photo1 = await app.download_media(user1.photo.big_file_id, file_name=p1_path)
        except Exception:
            photo1 = download_image("https://telegra.ph/file/05aa686cf52fc666184bf.jpg", p1_path)

        try:
            photo2 = await app.download_media(user2.photo.big_file_id, file_name=p2_path)
        except Exception:
            photo2 = download_image("https://telegra.ph/file/05aa686cf52fc666184bf.jpg", p2_path)

        # دانلود پس‌زمینه
        bg_url = "https://telegra.ph/file/96f36504f149e5680741a.jpg"
        download_image(bg_url, bg_path)

# آماده‌سازی تصویر
        caption = prepare_love_image(user1, user2, photo1, photo2, bg_path, result_path, custom_text)

        # ارسال تصویر
        await message.reply_photo(
            photo=result_path,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("✨ اضافه کردن من به گروه", url=f"https://t.me/{app.username}?startgroup=true")]]
            ),
        )
    finally:
        # حذف فایل‌های موقت
        for path in [p1_path, p2_path, result_path, bg_path]:
            if os.path.exists(path):
                os.remove(path)

# 🌹 دستور زوج امروز
@app.on_message(filters.command("زوج_امروز") & ~filters.private)
async def random_couple(_, message):
    chat_id = message.chat.id

    # فقط در گروه‌ها فعال است
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("❌ این دستور فقط در گروه‌ها فعال است.")

    try:
        # انتخاب اعضای آنلاین
        members = []
        async for member in app.get_chat_members(chat_id, limit=100):
            if not member.user.is_bot and not member.user.is_deleted and member.status == UserStatus.RECENTLY:
                members.append(member.user)

        if len(members) < 2:
            return await message.reply_text("❌ کاربران آنلاین کافی وجود ندارد.")

        # تعیین جنسیت کاربران
        male_users, female_users = [], []
        for user in members:
            try:
                photo = await app.download_media(user.photo.big_file_id, file_name=f"downloads/temp_{user.id}.png")
                analysis = DeepFace.analyze(photo, actions=["gender"])
                if analysis["dominant_gender"] == "Male":
                    male_users.append(user)
                elif analysis["dominant_gender"] == "Female":
                    female_users.append(user)
                os.remove(photo)
            except Exception:
                pass

        # انتخاب کاربران
        if male_users and female_users:
            c1 = random.choice(male_users)
            c2 = random.choice(female_users)
        else:
            c1, c2 = random.sample(members, 2)

        # دانلود تصاویر پروفایل
        p1_path = "downloads/p1.png"
        p2_path = "downloads/p2.png"
        bg_path = "downloads/background_love.png"
        result_path = "downloads/love_result.png"

        try:
            photo1 = await app.download_media(c1.photo.big_file_id, file_name=p1_path)
        except Exception:
            photo1 = download_image("https://telegra.ph/file/05aa686cf52fc666184bf.jpg", p1_path)

        try:
            photo2 = await app.download_media(c2.photo.big_file_id, file_name=p2_path)
        except Exception:
            photo2 = download_image("https://telegra.ph/file/05aa686cf52fc666184bf.jpg", p2_path)

        # دانلود پس‌زمینه
        bg_url = "https://telegra.ph/file/96f36504f149e5680741a.jpg"
        download_image(bg_url, bg_path)

        # آماده‌سازی تصویر
        caption = prepare_love_image(c1, c2, photo1, photo2, bg_path, result_path)

        # ارسال تصویر
        await message.reply_photo(
            photo=result_path,
            caption=caption,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("✨ اضافه کردن من به گروه", url=f"https://t.me/{app.username}?startgroup=true")]]
            ),
        )
    finally:
        # حذف فایل‌های موقت
        for path in [p1_path, p2_path, result_path, bg_path]:
            if os.path.exists(path):
                os.remove(path)
