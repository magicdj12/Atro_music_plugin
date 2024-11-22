from pyrogram import filters
from pyrogram.enums import ChatAction
from TheApi import api

from YukkiMusic import app
from config import BANNED_USERS


@app.on_message(filters.command(["جی پی تی", "هوش مشصنوعی", "سوال",'bard','بارد','chatgpt'],prefixes=['','/']) & ~BANNED_USERS)
async def chatgpt_chat(bot, message):
    if len(message.command) < 2 and not message.reply_to_message:
        await message.reply_text(
            "نمونه:\n\n`/سوال چگونه از حساب خود حفاظت کنیم?`"
        )
        return

    if message.reply_to_message and message.reply_to_message.text:
        user_input = message.reply_to_message.text
    else:
        user_input = " ".join(message.command[1:])

    await bot.send_chat_action(message.chat.id, ChatAction.TYPING)
    results = api.chatgpt(user_input)
    await message.reply_text(results)



__MODULE__ = "هوش مصنوعی◉"
__HELP__ = """
◉هوش مصنوعی
 
با استفاده از دستور زیر خبرها و...هرچیزی که بخواین دریافت کنید 🔻
𝄞 گوگل
/google [آب و هو]

با استفاده از دستور زیر هر نوع برنامه ای که میخواین دانلود کنید🔻
𝄞برنامه
/app [فیلتیر شکن]


با استفاده از دستور زیر سوال خودرا چت جی پی تی بپرسید 🔻
𝄞بارد 
/bard [ ترامپ چه کسیست]
با استفاده از دستور زیر سوال خودرا از هوش مصنوعی بپرسید🔻
𝄞هوشم
/ai

"""
