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

# 📅 دریافت تاریخ و زمان
def get_date_formats():
    now = datetime.now(pytz.timezone("Asia/Tehran"))
    jalali_date = JalaliDatetime.now().strftime("%Y/%m/%d")
    gregorian_date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    return jalali_date, gregorian_date, time

# 🌹 طراحی تصویر
def create_image(user1, user2, photo1_path, photo2_path, poem, custom_text=None):
    # ایجاد پس‌زمینه
    background = Image.new("RGB", (1200, 800), (50, 50, 100))
    draw = ImageDraw.Draw(background)
    gradient = Image.new("RGBA", background.size, (255, 0, 0, 0))
    for y in range(gradient.height):
        opacity = int(255 * (1 - y / gradient.height))
        draw.rectangle([(0, y), (gradient.width, y + 1)], fill=(255, 105, 180, opacity))
    background = Image.alpha_composite(background.convert("RGBA"), gradient).convert("RGB")

    # اضافه کردن تصاویر کاربران
    if photo1_path:
        img1 = Image.open(photo1_path).resize((400, 400)).convert("RGBA")
        mask1 = Image.new("L", (400, 400), 0)
        mask_draw = ImageDraw.Draw(mask1)
        mask_draw.ellipse((0, 0, 400, 400), fill=255)
        img1.putalpha(mask1)
        background.paste(img1, (100, 200), img1)

    if photo2_path:
        img2 = Image.open(photo2_path).resize((400, 400)).convert("RGBA")
        mask2 = Image.new("L", (400, 400), 0)
        mask_draw = ImageDraw.Draw(mask2)
        mask_draw.ellipse((0, 0, 400, 400), fill=255)
        img2.putalpha(mask2)
        background.paste(img2, (700, 200), img2)

    # اضافه کردن اسامی
    font_path = "arial.ttf"
    try:
        font = ImageFont.truetype(font_path, 30)
    except IOError:
        font = ImageFont.load_default()

    draw.text((200, 650), f"{user1.first_name}", fill="white", font=font)
    draw.text((800, 650), f"{user2.first_name}", fill="white", font=font)

    # اضافه کردن شعر
    draw.text((100, 750), poem, fill="white", font=font)

    # اضافه کردن متن سفارشی
    if custom_text:
        draw.text((300, 50), custom_text, fill="yellow", font=font)

    # ذخیره تصویر
    result_path = "downloads/result.png"
    background.save(result_path)
    return result_path

# 👫 دستور زوج (اتفاقی)
@app.on_message(filters.regex(r"^(زوج|Zoj|zoj)$") & ~filters.private)
async def random_couple(_, message):
    # کد انتخاب زوج اتفاقی...

# 👫 دستور زوج انتخابی
@app.on_message(filters.regex(r"^(زوج)\s+(\d+|\@[\w\d]+)\s+(\d+|\@[\w\d]+)(.*)?$") & ~filters.private)
async def chosen_couple(_, message):
    # کد انتخاب زوج بر اساس ایدی...
