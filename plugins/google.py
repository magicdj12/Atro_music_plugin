import logging
from googlesearch import search
from pyrogram import Client, filters
from SafoneAPI import SafoneAPI
from YukkiMusic import app

# فعال‌سازی لاگینگ برای ردیابی خطاها و اطلاعات
logging.basicConfig(
    level=logging.DEBUG,  # تنظیم سطح لاگ به DEBUG برای گرفتن تمام جزئیات
    format='%(asctime)s - %(levelname)s - %(message)s',  # فرمت نمایش لاگ
    handlers=[
        logging.StreamHandler()  # نمایش لاگ‌ها در کنسول
    ]
)

@app.on_message(filters.command(["google", "gle", "گوگل"]))
async def google(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text("Example:\n\n/google lord ram")
        return

    # دریافت ورودی از پیام
    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        user_input = " ".join(message.command[1:])

    # نمایش پیام اولیه
    b = await message.reply_text("Sᴇᴀʀᴄʜɪɴɢ ᴏɴ Gᴏᴏɢʟᴇ....")
    
    try:
        # انجام جستجو در گوگل
        logging.debug(f"Searching for: {user_input}")
        a = search(user_input, num_results=5)
        
        txt = f"Search Query: {user_input}\n\nresults:"
        for result in a:
            txt += f"\n\n❍ {result.title}\n<b>{result.description}</b>"
        
        await b.edit(txt, disable_web_page_preview=True)
    except Exception as e:
        await b.edit("An error occurred while searching.")
        logging.exception(f"Error while searching Google: {e}")


@app.on_message(filters.command(["app", "apps", "برنامه"], prefixes=["", "/"]))
async def app(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text("Example:\n\n/app Free Fire")
        return

    # دریافت ورودی از پیام
    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        user_input = " ".join(message.command[1:])
    
    # نمایش پیام اولیه
    cbb = await message.reply_text("Sᴇᴀʀᴄʜɪɴɢ ᴏɴ Pʟᴀʏ Sᴛᴏʀᴇ....")
    
    try:
        logging.debug(f"Searching app: {user_input}")
        # انجام جستجو در Play Store با استفاده از SafoneAPI
        a = await SafoneAPI().apps(user_input, 1)
        
        if not a["results"]:
            await cbb.edit("No results found for the app.")
            return
        
        b = a["results"][0]
        icon = b["icon"]
        app_id = b["id"]
        link = b["link"]
        description = b["description"]
        title = b["title"]
        developer = b["developer"]

        # ساخت اطلاعات برای نمایش
        info = f"<b>ᴛɪᴛʟᴇ : {title}</b>\n<b>ɪᴅ</b>: <code>{app_id}</code>\n<b>ᴅᴇᴠᴇʟᴏᴘᴇʀ</b>: {developer}\n<b>ᴅᴇsᴄʀɪᴘᴛɪᴏɴ</b>: {description}"
        
        await message.reply_photo(icon, caption=info)
        await cbb.delete()
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
        logging.exception(f"Error while fetching app information: {e}")
