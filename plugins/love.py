from pyrogram import filters
from pyrogram.types import Message
from YukkiMusic import app

def bold(x):
    return f"**{x}:** "


def bold_ul(x):
    return f"**--{x}:**-- "


def mono(x):
    return f"`{x}`\n"

@app.on_message(filters.command(["عشق",'love'],prefixes=["", "/"]))
async def chat_info_func(_, message: Message):
    chat = message.chat.id
    user_input = message.text.split(' ')
    if len(user_input) == 3:
        app.send_message(chat,user_input)

# __MODULE__ = "عشق"
__HELP__ = """
• عشق نام کاربر نام کاربری دوم
• عشق سلیم فواد
"""
