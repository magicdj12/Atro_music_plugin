from pyrogram import enums, filters
from YukkiMusic import app
from utils.permissions import adminsOnly


@app.on_message(filters.command(["removephoto","حذف بروف"]))
@adminsOnly("can_change_info")
async def deletechatphoto(_, message):

    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش....")
    admin_check = await app.get_chat_member(chat_id, user_id)
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها قابل استفاده است!")  # This command works only in groups
    try:
        if admin_check.privileges.can_change_info:
            await app.delete_chat_photo(chat_id)
            await msg.edit(
                "عکس پروفایل گروه حذف شد !\nتوسط {}".format(
                    message.from_user.mention
                )
            )
    except BaseException:
        await msg.edit(
            "برای حذف عکس پروفایل گروه، کاربر باید دسترسی ادمین تغییر اطلاعات گروه را داشته باشد!"  # User must have admin rights to change group info
        )


@app.on_message(filters.command("setphoto"))
@adminsOnly("can_change_info")
async def setchatphoto(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    admin_check = await app.get_chat_member(chat_id, user_id)
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها قابل استفاده است!")  # This command works only in groups
    elif not reply:
        await msg.edit("لطفاً به یک عکس یا سند پاسخ دهید.")  # Please reply to a photo or document
    elif reply:
        try:
            if admin_check.privileges.can_change_info:
                photo = await reply.download()
                await message.chat.set_photo(photo=photo)
                await msg.edit_text(
                    "عکس پروفایل گروه تغییر یافت !\nتوسط {}".format(
                        message.from_user.mention
                    )
                )
            else:
                await msg.edit("مشکلی پیش آمده، لطفاً عکس دیگری امتحان کنید!")  # Something went wrong, try another photo
        except BaseException:
            await msg.edit(
                "برای تغییر عکس پروفایل گروه، کاربر باید دسترسی ادمین تغییر اطلاعات گروه را داشته باشد!"  # User must have admin rights to change group photo
            )


@app.on_message(filters.command("settitle"))
@adminsOnly("can_change_info")
async def setgrouptitle(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها قابل استفاده است!")  # This command works only in groups
    elif reply:
        try:
            title = message.reply_to_message.text
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_title(title)
                await msg.edit(
                    "عنوان جدید گروه تنظیم شد !\nتوسط {}".format(
                        message.from_user.mention
                    )
                )
        except AttributeError:
            await msg.edit(
                "برای تغییر عنوان گروه، کاربر باید دسترسی ادمین تغییر اطلاعات گروه را داشته باشد!"  # User must have admin rights to change group title
            )
    elif len(message.command) > 1:
        try:
            title = message.text.split(None, 1)[1]
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_title(title)
                await msg.edit(

            "عنوان جدید گروه تنظیم شد !\nتوسط {}".format(
                        message.from_user.mention
                    )
                )
        except AttributeError:
            await msg.edit(
                "برای تغییر عنوان گروه، کاربر باید دسترسی ادمین تغییر اطلاعات گروه را داشته باشد!"  # User must have admin rights to change group title
            )

    else:
        await msg.edit(
            "لطفاً به یک متن پاسخ دهید یا عنوان جدیدی برای گروه وارد کنید."  # Please reply with a text or provide a new title for the group
        )


@app.on_message(filters.command(["setdiscription", "setdesc"]))
@adminsOnly("can_change_info")
async def setg_discription(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها قابل استفاده است!")  # This command works only in groups
    elif reply:
        try:
            discription = message.reply_to_message.text
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_description(discription)
                await msg.edit(
                    "توضیحات جدید گروه تغییر یافت !\nتوسط {}".format(
                        message.from_user.mention
                    )
                )
        except AttributeError:
            await msg.edit(
                "برای تغییر توضیحات گروه، کاربر باید دسترسی ادمین تغییر اطلاعات گروه را داشته باشد!"  # User must have admin rights to change group description
            )
    elif len(message.command) > 1:
        try:
            discription = message.text.split(None, 1)[1]
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_description(discription)
                await msg.edit(
                    "توضیحات جدید گروه تغییر یافت !\nتوسط {}".format(
                        message.from_user.mention
                    )
                )
        except AttributeError:
            await msg.edit(
                "برای تغییر توضیحات گروه، کاربر باید دسترسی ادمین تغییر اطلاعات گروه را داشته باشد!"  # User must have admin rights to change group description
            )
    else:
        await msg.edit(
            "لطفاً به یک متن پاسخ دهید یا توضیحات جدیدی برای گروه وارد کنید."  # Please reply with a text or provide new description for the group
        )
