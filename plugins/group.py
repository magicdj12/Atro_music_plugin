from pyrogram import enums, filters
from YukkiMusic import app
from utils.permissions import adminsOnly

@app.on_message(filters.regex(r"^(removephoto|حذف پروف)$"))
@adminsOnly("can_change_info")
async def deletechatphoto(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش....")
    admin_check = await app.get_chat_member(chat_id, user_id)
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند!")
        return
    try:
        if admin_check.privileges.can_change_info:
            await app.delete_chat_photo(chat_id)
            await msg.edit(
                f"عکس پروفایل گروه حذف شد!\nتوسط {message.from_user.mention}"
            )
    except Exception:
        await msg.edit(
            "کاربر باید حقوق تغییر اطلاعات مدیر را داشته باشد تا بتواند عکس گروه را حذف کند!"
        )

@app.on_message(filters.regex(r"^(setphoto|تنظیم پروف)$"))
@adminsOnly("can_change_info")
async def setchatphoto(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    admin_check = await app.get_chat_member(chat_id, user_id)
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند!")
        return
    if not reply:
        await msg.edit("لطفاً به یک عکس یا سند پاسخ دهید.")
        return
    try:
        if admin_check.privileges.can_change_info:
            photo = await reply.download()
            await message.chat.set_photo(photo=photo)
            await msg.edit_text(
                f"عکس پروفایل گروه تغییر یافت!\nتوسط {message.from_user.mention}"
            )
        else:
            await msg.edit("چیزی اشتباه پیش آمده، لطفاً عکس دیگری امتحان کنید!")
    except Exception:
        await msg.edit(
            "کاربر باید حقوق تغییر اطلاعات مدیر را داشته باشد تا بتواند عکس گروه را تغییر دهد!"
        )

@app.on_message(filters.regex(r"^(settitle|تنظیم نام)$"))
@adminsOnly("can_change_info")
async def setgrouptitle(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند!")
        return
    if len(message.command) > 1:
        title = message.text.split(None, 1)[1]
    elif message.reply_to_message:
        title = message.reply_to_message.text
    else:
        await msg.edit("شما باید به یک متن پاسخ دهید یا متنی برای تغییر نام گروه وارد کنید.")
        return
    try:
        admin_check = await app.get_chat_member(chat_id, user_id)
        if admin_check.privileges.can_change_info:
            await message.chat.set_title(title)
            await msg.edit(
                f"نام جدید گروه تغییر یافت!\nتوسط {message.from_user.mention}"
            )
    except Exception:
        await msg.edit(
            "کاربر باید حقوق تغییر اطلاعات مدیر را داشته باشد تا بتواند نام گروه را تغییر دهد!"
        )

@app.on_message(filters.regex(r"^(setdiscription|setdesc|تنظیم بیو)$"))
@adminsOnly("can_change_info")
async def setg_discription(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند!")
        return
    if len(message.command) > 1:
        discription = message.text.split(None, 1)[1]
    elif message.reply_to_message:
        discription = message.reply_to_message.text
    else:
        await msg.edit("شما باید به یک متن پاسخ دهید یا متنی برای تغییر توضیحات گروه وارد کنید.")
        return
    try:
        admin_check = await app.get_chat_member(chat_id, user_id)
        if admin_check.privileges.can_change_info:
            await message.chat.set_description(discription)
            await msg.edit(
                f"توضیحات جدید گروه تغییر یافت!\nتوسط {message.from_user.mention}"
            )
    except Exception:
        await msg.edit(
            "کاربر باید حقوق تغییر اطلاعات مدیر را داشته باشد تا بتواند توضیحات گروه را تغییر دهد!"
        )
