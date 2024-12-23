from pyrogram import Client, enums, filters
from YukkiMusic import app
from utils.permissions import adminsOnly

@app.on_message(filters.regex(r"^(removephoto|حذف پروف)$"))
@adminsOnly("can_change_info")
async def deletechatphoto(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند!")
        return
    try:
        admin_check = await app.get_chat_member(chat_id, user_id)
        if admin_check.privileges.can_change_info:
            await app.delete_chat_photo(chat_id)
            await msg.edit(f"عکس پروفایل گروه حذف شد!\nتوسط {message.from_user.mention}")
        else:
            await msg.edit("شما دسترسی لازم برای تغییر عکس گروه را ندارید!")
    except Exception as e:
        await msg.edit(f"خطایی رخ داد: {e}")

@app.on_message(filters.regex(r"^(setphoto|تنظیم پروف)$"))
@adminsOnly("can_change_info")
async def setchatphoto(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند!")
        return
    if not reply or not (reply.photo or reply.document):
        await msg.edit("لطفاً به یک عکس یا سند پاسخ دهید.")
        return
    try:
        admin_check = await app.get_chat_member(chat_id, user_id)
        if admin_check.privileges.can_change_info:
            photo = await reply.download()
            await app.set_chat_photo(chat_id, photo)
            await msg.edit(f"عکس پروفایل گروه تغییر یافت!\nتوسط {message.from_user.mention}")
        else:
            await msg.edit("شما دسترسی لازم برای تغییر عکس گروه را ندارید!")
    except Exception as e:
        await msg.edit(f"خطایی رخ داد: {e}")

@app.on_message(filters.regex(r"^(settitle|تنظیم نام)$"))
@adminsOnly("can_change_info")
async def setgrouptitle(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند!")
        return
    title = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else None
    if not title and message.reply_to_message:
        title = message.reply_to_message.text
    if not title:
        await msg.edit("لطفاً متنی برای نام گروه وارد کنید.")
        return
    try:
        admin_check = await app.get_chat_member(chat_id, user_id)
        if admin_check.privileges.can_change_info:
            await app.set_chat_title(chat_id, title)
            await msg.edit(f"نام جدید گروه تغییر یافت!\nتوسط {message.from_user.mention}")
        else:
            await msg.edit("شما دسترسی لازم برای تغییر نام گروه را ندارید!")
    except Exception as e:
        await msg.edit(f"خطایی رخ داد: {e}")

@app.on_message(filters.regex(r"^(setdiscription|setdesc|تنظیم بیو)$"))
@adminsOnly("can_change_info")
async def setg_discription(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند!")
        return
    description = message.text.split(None, 1)[1] if len(message.text.split()) > 1 else None
    if not description and message.reply_to_message:
        description = message.reply_to_message.text
    if not description:
        await msg.edit("لطفاً متنی برای توضیحات گروه وارد کنید.")
        return
    try:
        admin_check = await app.get_chat_member(chat_id, user_id)

        if admin_check.privileges.can_change_info:
            await app.set_chat_description(chat_id, description)
            await msg.edit(f"توضیحات جدید گروه تغییر یافت!\nتوسط {message.from_user.mention}")
        else:
            await msg.edit("شما دسترسی لازم برای تغییر توضیحات گروه را ندارید!")
    except Exception as e:
        await msg.edit(f"خطایی رخ داد: {e}")
