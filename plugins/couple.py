import os
import random
from datetime import datetime
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

# لیست شعرها
poems = [
    "هرگز نمی‌پنداشتم، از عشق هم زنجیر سازند...\nتا بر دست و پای دل، زنجیر کردند.",
    "عشق یعنی سکوت، نگاه\nو قلبی که برایت تپید...",
    "تو فقط باش، همین که تو را دارم کافی‌ست...\nجهان برایم زیباست.",
    "به تو سوگند که هیچ‌گاه کسی شبیه تو نخواهم یافت...",
    "دلتنگی یعنی به جای بوسیدنت، تنها نامت را صدا بزنم.",
    "کاش باران می‌بارید تا بفهمی چقدر دوستت دارم...",
    "تو دلیل زیبایی صبح‌های منی.",
    "یک لحظه کنارم باش\nو بگذار زمان متوقف شود...",
    "هر بار که تو را می‌بینم\nجهانم روشن‌تر می‌شود.",
    "اگر عشق تو گناه است، پس من گناهکارترینم.",
    "چشمان تو، رویای زندگی من است.",
    "لبخند تو دلیل شادی من است.",
    "تو برایم همه چیز هستی.",
    "زندگی من، با تو معنا دارد.",
    "تنها تو هستی که می‌توانی قلبم را لمس کنی.",
    "آغوشت خانه‌ی ابدی من است.",
    "تو دلیل بودنم هستی.",
    "تو را بیشتر از دیروز دوست دارم.",
    "برای تو می‌نویسم؛ هر آنچه از عشق می‌دانم.",
    "تو شعر زندگی منی.",
    "هر لحظه‌ام با یاد تو زیباست.",
    "خورشید صبحگاهی من، لبخند توست.",
    "تو را دیدم و دیگر هیچ ندیدم...",
    "تو شگفت‌انگیزترین هدیه‌ی زندگی‌ام هستی.",
    "هر جا که تو باشی، من خوشبختم.",
    "اگر بهشت این است، من آن را در چشمان تو یافتم.",
    "عشق من، برای تو می‌نویسم.",
    "تو خورشید قلب منی.",
    "با تو همه چیز ممکن است.",
    "در کنار تو، زندگی زیباتر است.",
]

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

{user1.first_name} (tg://user?id={user1.id}) ❤️ {user2.first_name} (tg://user?id={user2.id})

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
