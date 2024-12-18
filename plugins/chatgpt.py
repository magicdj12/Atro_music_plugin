# from config import BANNED_USERS
# from pyrogram import filters
# from pyrogram.enums import ChatAction
# from TheApi import api
# from YukkiMusic import app
# import requests
# from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
# from YukkiMusic import app



# @app.on_message(filters.command(["chatgpt", "ai", "ask"]) & ~BANNED_USERS)
# async def chatgpt_chat(bot, message):
#     if len(message.command) < 2 and not message.reply_to_message:
#         await message.reply_text(
#             "Example:\n\n`/ai write simple website code using html css, js?`"
#         )
#         return

#     if message.reply_to_message and message.reply_to_message.text:
#         user_input = message.reply_to_message.text
#     else:
#         user_input = " ".join(message.command[1:])

#     await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
#     results = await api.chatgpt(user_input)
#     await message.reply_text(results)


# __MODULE__ = "CʜᴀᴛGᴘᴛ"
# __HELP__ = """
# /advice - ɢᴇᴛ ʀᴀɴᴅᴏᴍ ᴀᴅᴠɪᴄᴇ ʙʏ ʙᴏᴛ
# /ai [ǫᴜᴇʀʏ] - ᴀsᴋ ʏᴏᴜʀ ǫᴜᴇsᴛɪᴏɴ ᴡɪᴛʜ ᴄʜᴀᴛɢᴘᴛ's ᴀɪ
# /gemini [ǫᴜᴇʀʏ] - ᴀsᴋ ʏᴏᴜʀ ǫᴜᴇsᴛɪᴏɴ ᴡɪᴛʜ ɢᴏᴏɢʟᴇ's ɢᴇᴍɪɴɪ ᴀɪ"""

from config import BANNED_USERS
from pyrogram import filters
from pyrogram.enums import ChatAction
from TheApi import api
from YukkiMusic import app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

# بررسی کاربر ممنوعه
BANNED_USERS = filters.user([])  # لیست کاربران ممنوعه را اینجا اضافه کنید.

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
        # فراخوانی ChatGPT API
        results = await api.chatgpt(user_input)
        if results:
            await message.reply_text(results)
        else:
            await message.reply_text("No response received from ChatGPT.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")


# MODULE = "CʜᴀᴛGᴘᴛ"
# HELP = """
# /advice - ɢᴇᴛ ʀᴀɴᴅᴏᴍ ᴀᴅᴠɪᴄᴇ ʙʏ ʙᴏᴛ
# /ai [ǫᴜᴇʀʏ] - ᴀsᴋ ʏᴏᴜʀ ǫᴜᴇsᴛɪᴏɴ ᴡɪᴛʜ ᴄʜᴀᴛɢᴘᴛ's ᴀɪ
# /gemini [ǫᴜᴇʀʏ] - ᴀsᴋ ʏᴏᴜʀ ǫᴜᴇsᴛɪᴏɴ ᴡɪᴛʜ ɢᴏᴏɢʟᴇ's ɢᴇᴍɪɴɪ ᴀɪ
# """
