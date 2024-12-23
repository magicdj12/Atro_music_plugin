import logging
from googlesearch import search
from pyrogram import filters
from SafoneAPI import SafoneAPI
from YukkiMusic import app

# دستور جستجوی گوگل
@app.on_message(filters.text & filters.regex(r"^(?i)(گوگل|google|gle)"))
async def google(bot, message):
    # بررسی وجود ورودی
    if len(message.text.split()) < 2 and not message.reply_to_message:
        await message.reply_text("نمونه استفاده:\n\nگوگل برنامه نویسی")
        return

    # دریافت ورودی از پیام یا پیام پاسخ داده شده
    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        user_input = " ".join(message.text.split()[1:])
    b = await message.reply_text("در حال جستجو در گوگل...")
    
    try:
        # انجام جستجوی گوگل
        results = search(user_input, advanced=True)
        txt = f"نتایج جستجو برای: {user_input}\n\n"
        for result in results:
            txt += f"\n\n❍ {result.title}\n<b>{result.description}</b>"
        await b.edit(txt, disable_web_page_preview=True)
    except Exception as e:
        await b.edit(f"خطا رخ داد: {e}")
        logging.exception(e)

# دستور جستجوی برنامه در پلی‌استور
@app.on_message(filters.text & filters.regex(r"^(?i)(برنامه|app|apps)"))
async def app(bot, message):
    # بررسی وجود ورودی
    if len(message.text.split()) < 2 and not message.reply_to_message:
        await message.reply_text("نمونه استفاده:\n\nبرنامه اینستاگرام")
        return

    # دریافت ورودی از پیام یا پیام پاسخ داده شده
    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        user_input = " ".join(message.text.split()[1:])
    cbb = await message.reply_text("در حال جستجو در پلی‌استور...")
    
    try:
        # انجام جستجو در پلی‌استور
        result = await SafoneAPI().apps(user_input, 1)
        app_data = result["results"][0]
        icon = app_data["icon"]
        id = app_data["id"]
        link = app_data["link"]
        description = app_data["description"]
        title = app_data["title"]
        developer = app_data["developer"]

        # فرمت نمایش اطلاعات برنامه
        info = (
            f"<b>{title}</b>\n"
            f"<b>آی‌دی:</b> <code>{id}</code>\n"
            f"<b>توسعه‌دهنده:</b> {developer}\n"
            f"<b>توضیحات:</b> {description}"
        )
        await message.reply_photo(icon, caption=info)
        await cbb.delete()
    except Exception as e:
        await cbb.edit(f"خطا رخ داد: {e}")
        logging.exception(e)

# # اطلاعات راهنما
# HELP = """
# گوگل [متن جستجو] - برای جستجو در گوگل و دریافت نتایج
# برنامه [نام برنامه] - برای دریافت اطلاعات برنامه از پلی‌استور
# """
