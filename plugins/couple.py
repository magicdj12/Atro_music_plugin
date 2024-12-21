import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app

# لیست اشعار عاشقانه
LOVE_QUOTES = [
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
    "عشق همین است، در نگاه تو گم شدن...",
    "تو تمام دلیل زندگی منی...",
    "با تو تمام جهان زیباست...",
    "هر لحظه که با توام، زندگی عاشقانه‌تر است...",
    "در نگاهت هزار راز عشق نهفته است..."
]

def download_image(url, path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(path, "wb") as f:
            f.write(response.content)
    return path

# دستورات اصلی
@app.on_message(filters.command("زوج"))
async def select_couple(_, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("این دستور فقط در گروه‌ها کار می‌کند.")

    # حالت انتخابی
    args = message.text.split()
    if len(args) > 1:
        try:
            user1 = await app.get_users(args[1])
            user2 = await app.get_users(args[2])
        except Exception:
            return await message.reply_text("لطفاً آی‌دی یا یوزرنیم معتبر وارد کنید.")
        c1, c2 = user1.id, user2.id
    else:  # حالت تصادفی
        members = [
            m.user
            async for m in app.get_chat_members(chat_id, filter="recently")
            if not m.user.is_bot
        ]
        if len(members) < 2:
            return await message.reply_text("اعضای کافی برای انتخاب وجود ندارد.")
        random.shuffle(members)
        c1, c2 = members[0].id, members[1].id

    # دریافت عکس و نام‌ها
    user1 = await app.get_users(c1)
    user2 = await app.get_users(c2)
    name1, name2 = user1.first_name, user2.first_name

    p1_path, p2_path = "pfp1.png", "pfp2.png"
    try:
        p1 = await app.download_media(user1.photo.big_file_id, p1_path) if user1.photo else None
        p2 = await app.download_media(user2.photo.big_file_id, p2_path) if user2.photo else None
    except:
        p1, p2 = None, None

    # تنظیم عکس‌ها
    background = Image.new("RGB", (1024, 512), "black")
    draw = ImageDraw.Draw(background)

    def circle_crop(image_path):
        img = Image.open(image_path).resize((256, 256))
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + img.size, fill=255)
        img.putalpha(mask)
        return img

    if p1:
        img1 = circle_crop(p1_path)
        background.paste(img1, (128, 128), img1)
    if p2:
        img2 = circle_crop(p2_path)
        background.paste(img2, (640, 128), img2)

    # اضافه کردن نام‌ها
    font = ImageFont.truetype("arial.ttf", 40)
    draw.text((128, 400), name1, fill="white", font=font)
    draw.text((640, 400), name2, fill="white", font=font)

    # افزودن شعر
    quote = random.choice(LOVE_QUOTES)
    draw.text((256, 450), quote, fill="white", font=font)

    # ذخیره و ارسال
    result_path = "couple_result.png"
    background.save(result_path)

    await message.reply_photo(result_path, caption=f"{name1} ❤️ {name2}\n{quote}")

    # پاک کردن فایل‌ها
    for path in [p1_path, p2_path, result_path]:
        if os.path.exists(path):
            os.remove(path)
