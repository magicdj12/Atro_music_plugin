import traceback
from config import BANNED_USERS
from pyrogram import filters
from pyrogram.enums import ChatAction
from TheApi import api
from YukkiMusic import app

@app.on_message(filters.command(["chatgpt", "ai", "ask"]) & ~BANNED_USERS)
async def chatgpt_chat(bot, message):
    try:
        print("دستور دریافت شد.")  # دیباگ: تایید دریافت پیام

        # بررسی ورودی
        if len(message.command) < 2 and not message.reply_to_message:
            await message.reply_text(
                "مثال استفاده:\n\n/ai توضیحی درباره هوش مصنوعی بده."
            )
            print("ورودی کافی نبود.")  # دیباگ: ورودی خالی
            return

        # گرفتن ورودی
        if message.reply_to_message and message.reply_to_message.text:
            user_input = message.reply_to_message.text
        else:
            user_input = " ".join(message.command[1:])
        print(f"ورودی کاربر: {user_input}")  # دیباگ: نمایش ورودی کاربر

        # نشان دادن حالت تایپینگ
        await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
        print("حالت تایپینگ ارسال شد.")  # دیباگ: تایید ارسال تایپینگ

        # فراخوانی API
        results = api.chatgpt(user_input)
        print(f"پاسخ API: {results}")  # دیباگ: نمایش پاسخ API

        # بررسی و ارسال پاسخ
        if not results:
            await message.reply_text("پاسخی از هوش مصنوعی دریافت نشد.")
            print("پاسخی از API دریافت نشد.")  # دیباگ: پاسخ خالی
        else:
            await message.reply_text(results)
            print("پاسخ به کاربر ارسال شد.")  # دیباگ: تایید ارسال پاسخ

    except Exception as e:
        # چاپ جزئیات خطا
        error_details = traceback.format_exc()
        print(f"خطای کامل:\n{error_details}")
        await message.reply_text("یک خطا هنگام پردازش درخواست شما رخ داد.")
