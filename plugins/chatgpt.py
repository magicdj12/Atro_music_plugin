import traceback
from config import BANNED_USERS
from pyrogram import filters
from pyrogram.enums import ChatAction
from TheApi import api  # فرض می‌کنیم این ماژول درست پیکربندی شده
from YukkiMusic import app

@app.on_message(filters.command(["chatgpt", "ai", "ask"]) & ~BANNED_USERS)
async def chatgpt_chat(bot, message):
    try:
        # بررسی ورودی
        if len(message.command) < 2 and not message.reply_to_message:
            await message.reply_text(
                "مثال استفاده:\n\n/ai توضیحی درباره هوش مصنوعی بده."
            )
            return

        # گرفتن ورودی از پیام یا متن ریپلای شده
        if message.reply_to_message and message.reply_to_message.text:
            user_input = message.reply_to_message.text
        else:
            user_input = " ".join(message.command[1:])

        # نشان دادن حالت تایپینگ
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        # فراخوانی API
        results = api.chatgpt(user_input)

        # ارسال پاسخ یا پیغام خطا
        if not results:
            await message.reply_text("پاسخی از هوش مصنوعی دریافت نشد.")
        else:
            await message.reply_text(results)

    except Exception as e:
        # مدیریت خطا و چاپ جزئیات کامل
        error_details = traceback.format_exc()
        print(f"خطای کامل:\n{error_details}")  # چاپ خطا در کنسول
        await message.reply_text("یک خطا هنگام پردازش درخواست شما رخ داد.")

# # اطلاعات ماژول
# MODULE = "هوش مصنوعی"
# HELP = """
# هوش مصنوعی:
# - /ai سوال خود را از هوش مصنوعی بپرسید.
# - /advice دریافت مشاوره.
# """
