import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.enums import ChatType
from YukkiMusic import app

# لیست اشعار عاشقانه
LOVE_QUOTES = [
    "عشق همین است، در نگاه تو گم شدن...",
    "تو تمام دلیل زندگی منی...",
    "✨تو شعر زندگی منی.",
    "💞عشق یعنی تو، یعنی ما.",
    "🌹دنیای من با تو زیباست.",
    "❤️قلبم تنها با تو می‌تپد.",
    "🎵آهنگ زندگی منی.",
    "🌺هر لحظه کنار تو بهشت است.",
    "🔥گرمای عشق تو زندگی‌ام را روشن می‌کند.",
    "💖تو در قلبم همیشه خواهی ماند.",
    "💎با تو همه‌چیز زیباتر است.",
    "🌟ستاره‌های شب تنها با نگاه تو معنا دارند.",
    "🌷تو گل سرسبد عشق منی.",
    "💞با تو دنیا زیباتر است.",
    "🌈زندگی بدون تو رنگی ندارد.",
    "🌻خورشید قلب من تویی.",
    "💌نامه عشق من به تو هر روز نوشته می‌شود.",
    "🌙تو ماه شب‌های تار منی.",
    "💓تنها در آغوش تو آرام می‌گیرم.",
    "🦋زندگی‌ام پر از پروانه‌های عشق است، به لطف تو.",
    "🌼تو باغ آرزوهای منی.",
    "🎉عشق تو جشن زندگی من است.",
    "✨نگاهت جادوی لحظه‌های من است.",
    "💞عشق یعنی تو در کنار من.",
    "🌹تو گل عشقی که در قلبم شکوفا شده است.",
    "💖زندگی بدون تو هیچ است.",
    "💎تو ارزشمندترین دارایی منی.",
    "🔥تو شعله عشقی که در قلبم می‌سوزد.",
    "🌺هر لحظه با تو بهشت است.",
    "❤️تو تنها دلیل لبخند منی.",
    "🌷تو گل عشقی که در قلبم رشد کرده است.",
    "✨ستاره‌های شب تنها با نگاه تو معنا دارند."
    "با تو تمام جهان زیباست...",
    "هر لحظه که با توام، زندگی عاشقانه‌تر است...",
    "💞عشق یعنی تو، یعنی ما."
]

# دانلود تصویر پیش‌فرض
def download_default_image():
    url = "https://telegra.ph/file/05aa686cf52fc666184bf.jpg"
    path = "default_pfp.png"
    if not os.path.exists(path):
        response = requests.get(url)
        if response.status_code == 200:
            with open(path, "wb") as f:
                f.write(response.content)
    return path

# برش دایره‌ای عکس
def circle_crop(image_path):
    img = Image.open(image_path).resize((256, 256))
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + img.size, fill=255)
    img.putalpha(mask)
    return img

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
    default_image = download_default_image()

    try:
        p1 = await app.download_media(user1.photo.big_file_id, p1_path) if user1.photo else default_image
        p2 = await app.download_media(user2.photo.big_file_id, p2_path) if user2.photo else default_image
    except:
        p1, p2 = default_image, default_image

    # تنظیم عکس‌ها
    background = Image.new("RGB", (1024, 512), "black")
    draw = ImageDraw.Draw(background)

    img1 = circle_crop(p1)
    img2 = circle_crop(p2)

    background.paste(img1, (128, 128), img1)
    background.paste(img2, (640, 128), img2)

    # اضافه کردن نام‌ها و شعر
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", 40)
    except:
        return await message.reply_text("فونت پشتیبانی نمی‌شود. لطفاً فونت مناسب نصب کنید.")

    draw.text((128, 400), name1, fill="white", font=font)
    draw.text((640, 400), name2, fill="white", font=font)

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
