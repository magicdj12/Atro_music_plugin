import re
import requests
from config import LOG_GROUP_ID
from pyrogram import filters
from YukkiMusic import app


@app.on_message(filters.command(["دان", "اینستا", "ویدیو", "ریلز"], prefixes=["", "/"]))
async def download_instagram_video(client, message):
    if len(message.command) < 2:
        await message.reply_text("لطفاً لینک ویدئو یا ریلز اینستاگرام را بعد از دستور وارد کنید.")
        return
    url = message.text.split()[1]
    if not re.match(re.compile(r"^(https?://)?(www\.)?(instagram\.com|instagr\.am)/.*$"), url):
        return await message.reply_text("لینک وارد شده معتبر نیست. لطفاً یک لینک اینستاگرام معتبر وارد کنید.")
    processing_message = await message.reply_text("در حال پردازش، لطفاً صبر کنید...")
    api_url = f"https://insta-dl.hazex.workers.dev/?url={url}"

    response = requests.get(api_url)
    try:
        result = response.json()
        data = result["result"]
    except Exception as e:
        error_message = f"خطا رخ داد:\n{e}"
        try:
            await processing_message.edit(error_message)
        except Exception:
            await message.reply_text(error_message)
            return await app.send_message(LOG_GROUP_ID, error_message)
        return await app.send_message(LOG_GROUP_ID, error_message)
    
    if not result["error"]:
        video_url = data["url"]
        duration = data["duration"]
        quality = data["quality"]
        file_type = data["extension"]
        size = data["formattedSize"]
        caption = f"مدت زمان: {duration}\nکیفیت: {quality}\nنوع فایل: {file_type}\nحجم فایل: {size}"
        await processing_message.delete()
        await message.reply_video(video_url, caption=caption)
    else:
        try:
            return await processing_message.edit("دانلود ویدئو یا ریلز ناموفق بود.")
        except Exception:
            return await message.reply_text("دانلود ویدئو یا ریلز ناموفق بود.")


# # MODULE = "دانلود اینستا"
# HELP = """
# دانلود ویدئو و ریلز اینستاگرام:

# • دانلود [لینک]: دانلود ویدئو یا ریلز اینستاگرام. لینک ویدئو را بعد از دستور وارد کنید.
# • اینستا [لینک]: دانلود ویدئو یا ریلز اینستاگرام. لینک ویدئو را بعد از دستور وارد کنید.
# • ویدئو [لینک]: دانلود ویدئو یا ریلز اینستاگرام. لینک ویدئو را بعد از دستور وارد کنید.
# • ریلز [لینک]: دانلود ویدئو یا ریلز اینستاگرام. لینک ویدئو را بعد از دستور وارد کنید.
# """
