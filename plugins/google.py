import logging
from pyrogram import Client, filters
from SafoneAPI import SafoneAPI
from YukkiMusic import app
from googlesearch import search
from youtubesearchpython import VideosSearch  # برای جستجوی یوتیوب

# تنظیم لاگینگ
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

@app.on_message(filters.command(["google", "gle", "گوگل"]))
async def google(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text("مثال:\n\n/google lord ram")
        return

    user_input = (
        message.reply_to_message.text if message.reply_to_message and message.reply_to_message.text 
        else " ".join(message.command[1:])
    )

    b = await message.reply_text("در حال جستجو در گوگل...")

    try:
        logging.debug(f"Searching for: {user_input}")
        results = search(user_input, num_results=5)  # استفاده از googlesearch
        if not results:
            await b.edit("هیچ نتیجه‌ای یافت نشد.")
            return
        
        txt = f"نتایج جستجو برای: {user_input}\n\n"
        for result in results:
            txt += f"{result.title}\n{result.description}\n\n"

        await b.edit(txt, disable_web_page_preview=True)
    except Exception as e:
        await b.edit("خطا در جستجو.")
        logging.exception(f"Google search error: {e}")

@app.on_message(filters.command(["app", "apps", "برنامه"], prefixes=["", "/"]))
async def app(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text("مثال:\n\n/app Free Fire")
        return

    user_input = (
        message.reply_to_message.text if message.reply_to_message and message.reply_to_message.text 
        else " ".join(message.command[1:])
    )

    cbb = await message.reply_text("در حال جستجو در Play Store...")

    try:
        logging.debug(f"Searching app: {user_input}")
        api = SafoneAPI()
        response = await api.apps(user_input, 1)
        if not response.get("results"):
            await cbb.edit("برنامه‌ای یافت نشد.")
            return

        app_data = response["results"][0]
        icon = app_data["icon"]
        app_id = app_data["id"]
        link = app_data["link"]
        description = app_data["description"]
        title = app_data["title"]
        developer = app_data["developer"]

        info = (
            f"<b>عنوان:</b> {title}\n"
            f"<b>شناسه:</b> <code>{app_id}</code>\n"
            f"<b>توسعه‌دهنده:</b> {developer}\n"
            f"<b>توضیحات:</b> {description}\n"
            f"<b>لینک دانلود:</b> {link}"
        )

        await message.reply_photo(icon, caption=info)
        await cbb.delete()
    except Exception as e:
        await cbb.edit("خطا در دریافت اطلاعات برنامه.")
        logging.exception(f"App search error: {e}")

@app.on_message(filters.command(["youtube", "yt", "یو تیوب"], prefixes=["", "/"]))
async def youtube(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text("مثال:\n\n/youtube python tutorial")
        return

    user_input = (
        message.reply_to_message.text if message.reply_to_message and message.reply_to_message.text 
        else " ".join(message.command[1:])
    )

    b = await message.reply_text("در حال جستجو در یوتیوب...")

    try:
        logging.debug(f"Searching YouTube for: {user_input}")
        searcher = VideosSearch(user_input, limit=5)
        results = await searcher.next()

        if not results["videos"]:
            await b.edit("هیچ نتیجه‌ای در یوتیوب یافت نشد.")
            return

        txt = f"نتایج جستجو در یوتیوب برای: {user_input}\n\n"
        for result in results["videos"]:
            video_title = result["title"]
            video_url = result["link"]
            video_duration = result["duration"]
            txt += f"{video_title} - مدت زمان: {video_duration}\n\n"
            await b.edit(txt, disable_web_page_preview=True)
    except Exception as e:
        await b.edit("خطا در جستجو.")
        logging.exception(f"YouTube search error: {e}")
