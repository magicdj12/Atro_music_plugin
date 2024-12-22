import os

from pyrogram import enums, filters
from pyrogram.types import Message
from YukkiMusic import app
from YukkiMusic.misc import SUDOERS
from YukkiMusic.utils.database import is_gbanned_user

n = "\n"
w = " "

def bold(x):
    return f"{x}"

def bold_ul(x):
    return f"✨ {x} ✨"

def mono(x):
    return f"{x}{n}"

def section(title: str, body: dict, indent: int = 2, underline: bool = False) -> str:
    text = (bold_ul(title) + n) if underline else bold(title) + n
    for key, value in body.items():
        if value is not None:
            text += (
                indent * w
                + bold(key)
                + (
                    (value[0] + n)
                    if isinstance(value, list) and isinstance(value[0], str)
                    else mono(value)
                )
            )
    return text

async def userstatus(user_id):
    try:
        user = await app.get_users(user_id)
        x = user.status
        if x == enums.UserStatus.RECENTLY:
            return "🟢 وضعیت: به‌تازگی آنلاین شده است."
        elif x == enums.UserStatus.LAST_WEEK:
            return "🕒 آخرین بازدید: هفته گذشته."
        elif x == enums.UserStatus.LONG_AGO:
            return "📅 آخرین بازدید: مدت زمان طولانی پیش."
        elif x == enums.UserStatus.OFFLINE:
            return "🔘 وضعیت: آفلاین."
        elif x == enums.UserStatus.ONLINE:
            return "🟢 وضعیت: آنلاین."
    except Exception:
        return "⚠️ خطا: مشکلی رخ داده است. لطفاً دوباره تلاش کنید!"

async def get_user_info(user, already=False):
    if not already:
        user = await app.get_users(user)
    if not user.first_name:
        return ["❌ حساب کاربری حذف شده است.", None]
    user_id = user.id
    online = await userstatus(user_id)
    username = user.username
    first_name = user.first_name
    mention = user.mention("🌐 لینک به پروفایل")
    dc_id = user.dc_id
    photo_id = user.photo.big_file_id if user.photo else None
    is_gbanned = await is_gbanned_user(user_id)
    is_sudo = user_id in SUDOERS
    is_premium = "💎 بله" if user.is_premium else "❌ خیر"

    body = {
        "👤 نام:": [first_name],
        "🌐 نام کاربری:": [f"@{username}" if username else "🔸 مشخص نشده"],
        "🆔 شناسه کاربری:": user_id,
        "📍 شماره دیتاسنتر:": dc_id,
        "🔗 لینک:": [mention],
        "💎 حساب پریمیوم:": is_premium,
        "⏱ آخرین بازدید:": online,
    }
    caption = section("✨ اطلاعات کامل کاربر ✨", body)
    return [caption, photo_id]

async def get_chat_info(chat):
    chat = await app.get_chat(chat)
    username = chat.username
    link = f"🌐 لینک به گروه (https://t.me/{username})" if username else "🔸 مشخص نشده"
    photo_id = chat.photo.big_file_id if chat.photo else None

    info = f"""
✨ اطلاعات کامل گروه/چت ✨

🆔 شناسه چت: {chat.id}
👥 نام گروه/چت: {chat.title}
🌐 نام کاربری: {chat.username if chat.username else "🔸 مشخص نشده"}
📍 شماره دیتاسنتر: {chat.dc_id}
📝 توضیحات: {chat.description if chat.description else "🔸 ثبت نشده"}
📊 نوع چت: {chat.type}
✔️ تایید شده: {"✅ بله" if chat.is_verified else "❌ خیر"}
🚫 محدود شده: {"✅ بله" if chat.is_restricted else "❌ خیر"}
👑 سازنده گروه: {"✅ بله" if chat.is_creator else "❌ خیر"}
⚠️ کلاه‌برداری: {"✅ بله" if chat.is_scam else "❌ خیر"}
❌ جعلی: {"✅ بله" if chat.is_fake else "❌ خیر"}
👥 تعداد اعضا: {chat.members_count if chat.members_count else "🔸 **نامشخص**"}لینک:ک:** {link}

──────────────────────
"""
    return info, photo_id

@app.on_message(filters.command(["info", "$ایدی^"], prefixes=["", "/"]))
async def info_func(_, message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user.id
    elif not message.reply_to_message and len(message.command) == 1:
        user = message.from_user.id
    elif not message.reply_to_message and len(message.command) != 1:
        user_input = message.text.split(None, 1)[1]
        if user_input.isdigit():
            user = int(user_input)
        elif user_input.startswith("@"):
            user = user_input
        else:
            return await message.reply_text("⚠️ لطفاً شناسه یا نام کاربری را وارد کنید.")

    m = await message.reply_text("⏳ در حال پردازش...")

    try:
        info_caption, photo_id = await get_user_info(user)
    except Exception as e:
        return await m.edit(str(e))

    if not photo_id:
        return await m.edit(info_caption, disable_web_page_preview=True)
    photo = await app.download_media(photo_id)

    await message.reply_photo(photo, caption=info_caption, quote=False)
    await m.delete()
    os.remove(photo)

@app.on_message(filters.command(["chatinfo", "$چت ایدی^"], prefixes=["", "/"]))
async def chat_info_func(_, message: Message):
    splited = message.text.split()
    if len(splited) == 1:
        chat = message.chat.id
        if chat == message.from_user.id:
            return await message.reply_text("⚠️ دستور صحیح: /chatinfo [نام کاربری یا شناسه]")
    else:
        chat = splited[1]

    try:
        m = await message.reply_text("⏳ در حال پردازش...")

        info_caption, photo_id = await get_chat_info(chat)
        if not photo_id:
            return await m.edit(info_caption, disable_web_page_preview=True)

        photo = await app.download_media(photo_id)
        await message.reply_photo(photo, caption=info_caption, quote=False)

        await m.delete()
        os.remove(photo)
    except Exception as e:
        await m.edit(f"⚠️ خطا: {e}")
