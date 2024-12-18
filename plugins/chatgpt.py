from config import BANNED_USERS
from pyrogram import filters
from pyrogram.enums import ChatAction
from YukkiMusic import app
import openai  # نصب کتابخانه openai ضروری است: pip install openai

# کلید API از OpenAI
OPENAI_API_KEY = ""
openai.api_key = OPENAI_API_KEY

@app.on_message(filters.command(["chatgpt", "ai", "ask"]) & ~BANNED_USERS)
async def chatgpt_chat(bot, message):
    # بررسی خالی بودن ورودی
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text(
            "Example:\n\n/ai write simple website code using html, css, js?"
        )
        return

    # گرفتن ورودی از پاسخ یا دستور
    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        user_input = " ".join(message.command[1:])

    # ارسال وضعیت تایپ کردن
    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)

    try:
        # ارسال درخواست به OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # یا gpt-4 برای استفاده از مدل جدیدتر
            messages=[{"role": "user", "content": user_input}],
        )
        # گرفتن پاسخ از ChatGPT
        reply = response.choices[0].message["content"]
        await message.reply_text(reply)
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")


MODULE = "CʜᴀᴛGᴘᴛ"
HELP = """
/advice - ɢᴇᴛ ʀᴀɴᴅᴏᴍ ᴀᴅᴠɪᴄᴇ ʙʏ ʙᴏᴛ
/ai [ǫᴜᴇʀʏ] - ᴀsᴋ ʏᴏᴜʀ ǫᴜᴇsᴛɪᴏɴ ᴡɪᴛʜ ᴄʜᴀᴛɢᴘᴛ's ᴀɪ
/gemini [ǫᴜᴇʀʏ] - ᴀsᴋ ʏᴏᴜʀ ǫᴜᴇsᴛɪᴏɴ ᴡɪᴛʜ ɢᴏᴏɢʟᴇ's ɢᴇᴍɪɴɪ ᴀɪ
"""
