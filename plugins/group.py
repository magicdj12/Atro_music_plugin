from pyrogram import enums, filters
from YukkiMusic import app

from utils.permissions import adminsOnly


@app.on_message(filters.command(["removephoto","حذف پروف"]))
@adminsOnly("can_change_info")
async def deletechatphoto(_, message):

    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش....")
    admin_check = await app.get_chat_member(chat_id, user_id)
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند!")
    try:
        if admin_check.privileges.can_change_info:
            await app.delete_chat_photo(chat_id)
            await msg.edit(
                "عکس پروفایل گروه حذف شد!\nتوسط {}".format(
                    message.from_user.mention
                )
            )
    except BaseException:
        await msg.edit(
            "کاربر باید حقوق تغییر اطلاعات مدیر را داشته باشد تا بتواند عکس گروه را حذف کند!"
        )


@app.on_message(filters.command(["setphoto","تنظیم پروف"]))
@adminsOnly("can_change_info")
async def setchatphoto(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    admin_check = await app.get_chat_member(chat_id, user_id)
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند!")
    elif not reply:
        await msg.edit("لطفاً به یک عکس یا سند پاسخ دهید.")
    elif reply:
        try:
            if admin_check.privileges.can_change_info:
                photo = await reply.download()
                await message.chat.set_photo(photo=photo)
                await msg.edit_text(
                    "عکس پروفایل گروه تغییر یافت!\nتوسط {}".format(
                        message.from_user.mention
                    )
                )
            else:
                await msg.edit("چیزی اشتباه پیش آمده، لطفاً عکس دیگری امتحان کنید!")

        except BaseException:
            await msg.edit(
                "کاربر باید حقوق تغییر اطلاعات مدیر را داشته باشد تا بتواند عکس گروه را تغییر دهد!"
            )


@app.on_message(filters.command(["settitle","تنظیم نام"]))
@adminsOnly("can_change_info")
async def setgrouptitle(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند!")
    elif reply:
        try:
            title = message.reply_to_message.text
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_title(title)
                await msg.edit(
                    "نام جدید گروه تغییر یافت!\nتوسط {}".format(
                        message.from_user.mention
                    )
                )
        except AttributeError:
            await msg.edit(
                "کاربر باید حقوق تغییر اطلاعات مدیر را داشته باشد تا بتواند نام گروه را تغییر دهد!"
            )
    elif len(message.command) > 1:
        try:
            title = message.text.split(None, 1)[1]
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_title(title)
                await msg.edit(
                    "نام جدید گروه تغییر یافت!\nتوسط {}".format(
                        message.from_user.mention
                    )
                )
        except AttributeError:
            await msg.edit(
                "کاربر باید حقوق تغییر اطلاعات مدیر را داشته باشد تا بتواند نام گروه را تغییر دهد!"
            )

    else:
        await msg.edit(
            "شما باید به یک متن پاسخ دهید یا متنی برای تغییر نام گروه وارد کنید."
        )

@app.on_message(filters.command(["setdiscription", "setdesc","تنظیم بیو"]))
@adminsOnly("can_change_info")
async def setg_discription(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند!")
    elif reply:
        try:
            discription = message.reply_to_message.text
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_description(discription)
                await msg.edit(
                    "توضیحات جدید گروه تغییر یافت!\nتوسط {}".format(
                        message.from_user.mention
                    )
                )
        except AttributeError:
            await msg.edit(
                "کاربر باید حقوق تغییر اطلاعات مدیر را داشته باشد تا بتواند توضیحات گروه را تغییر دهد!"
            )
    elif len(message.command) > 1:
        try:
            discription = message.text.split(None, 1)[1]
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_description(discription)
                await msg.edit(
                    "توضیحات جدید گروه تغییر یافت!\nتوسط {}".format(
                        message.from_user.mention
                    )
                )
        except AttributeError:
            await msg.edit(
                "کاربر باید حقوق تغییر اطلاعات مدیر را داشته باشد تا بتواند توضیحات گروه را تغییر دهد!"
            )
    else:
        await msg.edit(
            "شما باید به یک متن پاسخ دهید یا متنی برای تغییر توضیحات گروه وارد کنید."
        )
