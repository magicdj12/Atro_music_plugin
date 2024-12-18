import random
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app

# لیست بیوگرافی‌ها
BIOGRAPHIES = [
    "زندگی کوتاه است، اما خاطرات آن طولانی.",
    "تنهایی را دوست دارم، چون کسی نیست که دلم را بشکند.",
    "غم‌هایم را می‌نویسم، شاید کسی بخواند و بفهمد.",
    "تو فقط خاطره‌ای هستی که هنوز زنده است.",
    "عشق، گاهی شروعی است برای پایان.",
    "هر روزی که بی تو می‌گذرد، یک قرن است.",
    "کاش دلی بود که به اندازه من تنگ تو می‌شد.",
    "زندگی‌ام را با خنده‌های مصنوعی پر کرده‌ام.",
    "گاهی دلتنگی برای کسی که نیست، عجیب زیباست.",
    "تو همان کسی هستی که نبودنت هم درد می‌آورد.",
    "اگر عشق جنون است، من دیوانه‌ترینم.",
    "تنهایی یعنی هزار نفر دور و برت باشند و تو باز دلتنگ باشی.",
    "هر زخم داستانی دارد، اما همه داستان‌ها شنیدنی نیستند.",
    "تو برای من تمام دنیا بودی، اما من برای تو فقط یک لحظه.",
    "زندگی چیزی نیست جز بازی احساسات و خاطرات.",
    "دلم برای روزهایی که هنوز ندیدمت تنگ است.",
    "غم و شادی هر دو می‌گذرند، اما زخم‌های عشق ماندنی‌اند.",
    "زندگی‌ام را در سکوت سپری می‌کنم، چون کسی صدایم را نمی‌شنود.",
    "تو رفتی و من هنوز منتظر بازگشتت هستم.",
    "خاطراتت مثل یک فیلم تکراری، هر شب در ذهنم پخش می‌شود.",
    "عشق یعنی تو، حتی اگر من نباشم.",
    "کاش می‌توانستم فقط یک بار دیگر نگاهت کنم.",
    "هرگز به کسی که دوستش داری نگو خداحافظ، شاید آخرین خداحافظی باشد.",
    "من همان عاشقی هستم که هیچ‌کس عشقش را باور نکرد.",
    "غمگینم، اما هنوز به امید دیدنت زنده‌ام.",
    "هر دل شکسته‌ای داستانی دارد که هیچ‌کس آن را نمی‌داند.",
    "گاهی درد، تنها دوای زخم‌های قدیمی است.",
    "تو رفته‌ای، اما خاطراتت هنوز با من زندگی می‌کنند.",
    "عشق واقعی هرگز نمی‌میرد، حتی اگر فراموش شود.",
]

@app.on_message(filters.text & filters.private)
async def get_bio(_, message):
    if message.text.strip() in ["بیو", "بیوگرافی"]:  # بررسی دستورات فارسی
        random_bio = random.choice(BIOGRAPHIES)
        refresh_button = InlineKeyboardButton("تازه‌سازی", callback_data="refresh_bio")
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[refresh_button]])
        await message.reply_text(
            random_bio, reply_markup=keyboard, parse_mode=ParseMode.HTML
        )


@app.on_callback_query(filters.regex(r"refresh_bio"))
async def refresh_bio(_, query):
    await query.answer()
    new_bio = random.choice(BIOGRAPHIES)
    await query.message.edit_text(
        new_bio,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("تازه‌سازی", callback_data="refresh_bio")]]
        ),
        parse_mode=ParseMode.HTML,
    )
