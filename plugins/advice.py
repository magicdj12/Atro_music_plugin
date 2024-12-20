from config import LOG_GROUP_ID
from pyrogram import filters
from SafoneAPI import SafoneAPI
from TheApi import api
from YukkiMusic import app


@app.on_message(filters.command(["advice","^ربات$"],prefixes=["", "/"]))
async def advice(_, message):
    A = await message.reply_text("ربات هم اکنون آنلاین میباشد !")
    res = api.get_advice()
    await A.edit(res)


@app.on_message(filters.command("astronomical"))
async def advice(_, message):
    a = await SafoneAPI().astronomy()
    if a["success"]:
        c = a["date"]
        url = a["imageUrl"]
        b = a["explanation"]
        caption = f"Tᴏᴅᴀʏ's [{c}] ᴀsᴛʀᴏɴᴏᴍɪᴄᴀʟ ᴇᴠᴇɴᴛ:\n\n{b}"
        await message.reply_photo(url, caption=caption)
    else:
        await message.reply_photo("ᴛʀʏ ᴀғᴛᴇʀ sᴏᴍᴇ ᴛɪᴍᴇ")
        await app.send_message(LOG_GROUP_ID, "/astronomical not working")


# __MODULE__ = "بیوگرافی"
__HELP__ = """
با این دستور میتوانید بیوگرافی دریافت کنید
  𝄞 بیو
/advice"""
