import os
import random
from datetime import datetime
from khayyam import JalaliDatetime
import pytz
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pyrogram import filters
from pyrogram.enums import ChatType, UserStatus
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app

# 📜 لیست اشعار عاشقانه
love_poems = [
    "تو با قلب ویرانه‌ی من چه کردی؟\nببین عشق دیوانه‌ی من چه کردی؟",
    "بهترین لحظه‌ام، همین حالاست\nکه تو باشی کنار من، جانم.",
    "عشق یعنی نگاه تو، یعنی آرامش وجودم.",
    "چشمانت شعر می‌گوید و من عاشقانه می‌نویسم.",
    "بی‌تو من هیچم، با تو همه‌چیزم.",
    "تا همیشه با تو خواهم بود، مثل نفس.",
    "زندگی‌ام در نگاهت خلاصه می‌شود.",
    "تو همان شعری که در قلبم حک شده‌ای.",
    "عشق یعنی تو، یعنی ما، یعنی همیشه.",
    "قلبم تنها برای تو می‌تپد.",
    "عاشق تو بودن، زیباترین حس دنیاست.",
    "هر لحظه که تو را می‌بینم، قلبم دوباره می‌تپد.",
    "می‌خواهم همیشه در کنار تو بمانم، بی‌هیچ دلیل.",
    "لبخندت دلیل زندگی من است.",
    "عشق تو، زیباترین اتفاق زندگی من است.",
    "قلبم تنها برای تو می‌زند، حتی در خواب.",
    "تو همان رویای شیرینی که هرگز تمام نمی‌شود.",
    "تو تنها دلیل خوشبختی‌ام هستی.",
    "با تو، دنیا زیباتر است.",
    "عشق یعنی دیدن لبخندت در هر صبح.",
    "تو تمام آرامش دنیا هستی.",
    "تو مثل شعری که هرگز کهنه نمی‌شود.",
    "من برای تو، تو برای من، ما برای همیشه.",
    "بی‌تو دنیا چیزی کم دارد.",
    "عشق یعنی زندگی‌ام با حضور تو کامل است.",
    "با تو بودن، بزرگ‌ترین نعمت خداوند است.",
    "تو دلیل لبخندهای بی‌اختیار منی.",
    "زندگی در کنار تو معنای عشق را کامل می‌کند.",
    "تو همان گمشده‌ای که همیشه می‌خواستم.",
    "هر لحظه با تو مثل یک شعر عاشقانه است.",
]

# 📅 دریافت تاریخ امروز
def get_date_formats():
    now = datetime.now(pytz.timezone("Asia/Tehran"))
    jalali_date = JalaliDatetime.now().strftime("%Y/%m/%d")
    gregorian_date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    return jalali_date, gregorian_date, time

# 🌹 دستور زوج
@app.on_message(filters.regex(r"^(زوج|زدوج|Zoj|zoj)$") & ~filters.private)
async def select_couple(_, message):
    chat_id = message.chat.id

    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("❌ این دستور فقط در گروه‌ها فعال است.")

    p1_path = "downloads/p1.png"
    p2_path = "downloads/p2.png"
    result_path = f"downloads/love_result_{chat_id}.png"

    jalali_date, gregorian_date, current_time = get_date_formats()

    try:
        members = []
        async for member in app.get_chat_members(chat_id, limit=100):
            if (
                not member.user.is_bot
                and not member.user.is_deleted
                and member.status in [UserStatus.ONLINE, UserStatus.RECENTLY]
            ):
                members.append(member.user)

        if len(members) < 2:
            return await message.reply_text("❌ کاربران کافی برای انتخاب وجود ندارد.")

        # تلاش برای انتخاب یک دختر و یک پسر
        females = [m for m in members if "خانم" in (m.first_name or "") or "خانم" in (m.last_name or "")]
        males = [m for m in members if "آقا" in (m.first_name or "") or "آقا" in (m.last_name or "")]

        if females and males:
            user1 = random.choice(females)
            user2 = random.choice(males)
        else:
            user1, user2 = random.sample(members, 2)

        # دانلود عکس کاربران
        try:
            photo1 = await app.download_media(user1.photo.big_file_id, file_name=p1_path)
        except Exception:
            photo1 = None

        try:
            photo2 = await app.download_media(user2.photo.big_file_id, file_name=p2_path)
        except Exception:
            photo2 = None

        # ایجاد تصویر پس‌زمینه با نورپردازی
        background = Image.new("RGB", (1000, 800), (30, 30, 50))
        draw = ImageDraw.Draw(background)
        gradient = Image.new("RGBA", background.size, (255, 0, 0, 0))
        for y in range(gradient.height):
            opacity = int(255 * (1 - y / gradient.height))
            draw.rectangle([(0, y), (gradient.width, y + 1)], fill=(255, 182, 193, opacity))
        background = Image.alpha_composite(background.convert("RGBA"), gradient).convert("RGB")

        if photo1:
            img1 = Image.open(photo1).resize((400, 400)).convert("RGBA")
            mask = Image.new("L", (400, 400), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, 400, 400), fill=255)
            img1.putalpha(mask)
            background.paste(img1, (100, 200), img1)

        if photo2:
            img2 = Image.open(photo2).resize((400, 400)).convert("RGBA")
            mask = Image.new("L", (400, 400), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, 400, 400), fill=255)
            img2.putalpha(mask)
            background.paste(img2, (500, 200), img2)

        # اضافه کردن شعر عاشقانه
        random_poem = random.choice(love_poems)
        font_path = "arial.ttf"
        try:
            font = ImageFont.truetype(font_path, 40)
        except IOError:
            font = ImageFont.load_default()

        text_position = (150, 650)
        draw.text(text_position, random_poem, fill="white", font=font)

        background.save(result_path)

        # ارسال تصویر همراه با کپشن و کلید شیشه‌ای
        await message.reply_photo(
            photo=result_path,
            caption=(
                f"💞 زوج امروز:\n👩 {user1.first_name} + 👦 {user2.first_name}\n\n"
                f"📅 تاریخ شمسی: {jalali_date}\n"
                f"📆 تاریخ میلادی: {gregorian_date}\n"
                f"🕒 ساعت: {current_time}\n\n"
                f"🌹 شعر عاشقانه:\n{random_poem}"
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "✨ منو ببر گروهت",
                            url=f"https://t.me/{app.username}?startgroup=true",
                        )
                    ]
                ]
            ),
        )

    except Exception as e:
        await message.reply_text(f"⚠️ خطا: {e}")
    finally:
        for path in [p1_path, p2_path, result_path]:
            if os.path.exists(path):
                os.remove(path)
