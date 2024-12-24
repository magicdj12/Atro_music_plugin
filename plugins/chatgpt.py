from config import BANNED_USERS
from pyrogram import filters
from pyrogram.enums import ChatAction
from TheApi import api  # فرض می‌کنیم این ماژول به‌درستی تنظیم شده
from YukkiMusic import app

@app.on_message(filters.command(["chatgpt", "ai", "ask"]) & ~BANNED_USERS)
async def chatgpt_chat(bot, message):
    try:
        # بررسی اینکه پیام حاوی دستور مناسب است
        if len(message.command) < 2 and not message.reply_to_message:
            await message.reply_text(
                "مثال استفاده:\n\n/ai توضیحی درباره هوش مصنوعی بده."
            )
            return

        # دریافت ورودی کاربر از پیام ریپلای یا دستور
        if message.reply_to_message and message.reply_to_message.text:
            user_input = message.reply_to_message.text
        else:
            user_input = " ".join(message.command[1:])

        # ارسال اکشن تایپینگ
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

        # فراخوانی API و دریافت پاسخ
        results = api.chatgpt(user_input)

        # بررسی و ارسال پاسخ
        if not results:
            await message.reply_text("پاسخی از هوش مصنوعی دریافت نشد.")
        else:
            await message.reply_text(results)

    except Exception as e:
        # گزارش خطا
        print(f"خطا رخ داد: {e}")
        await message.reply_text("یک خطا هنگام پردازش درخواست شما رخ داد.")

# # اطلاعات ماژول
# MODULE = "هوش مصنوعی"
# HELP = """
# هوش مصنوعی:
# - /ai سوال خود را از هوش مصنوعی بپرسید.
# - /advice دریافت مشاوره.
# """
