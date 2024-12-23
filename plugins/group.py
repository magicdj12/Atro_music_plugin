import logging
from pyrogram import Client, enums, filters
from pyrogram.types import ChatPermissions

# فعال‌سازی لاگ برای اشکال‌زدایی
logging.basicConfig(level=logging.DEBUG)

# تابع بررسی دسترسی مدیر
def adminsOnly(permission: str):
    def decorator(func):
        async def wrapper(_, message):
            chat_id = message.chat.id
            user_id = message.from_user.id
            try:
                # دریافت اطلاعات کاربر
                admin_check = await app.get_chat_member(chat_id, user_id)
                if admin_check.privileges and getattr(admin_check.privileges, permission, False):
                    return await func(_, message)  # اگر دسترسی داشت، دستور اجرا می‌شود
                else:
                    await message.reply_text("شما دسترسی لازم برای اجرای این دستور را ندارید.")
            except Exception as e:
                await message.reply_text("خطا در بررسی دسترسی‌ها.")
        return wrapper
    return decorator

# دستور حذف عکس پروفایل گروه
@app.on_message(filters.command("removephoto"))
@adminsOnly("can_change_info")
async def deletechatphoto(_, message):
    try:
        logging.debug("دستور removephoto اجرا شد.")  # برای اشکال‌زدایی
        chat_id = message.chat.id
        user_id = message.from_user.id
        msg = await message.reply_text("در حال پردازش....")
        
        admin_check = await app.get_chat_member(chat_id, user_id)
        
        if message.chat.type == enums.ChatType.PRIVATE:
            await msg.edit("این دستور فقط در گروه‌ها کار می‌کند.")
            return
        
        if admin_check.privileges.can_change_info:
            await app.delete_chat_photo(chat_id)
            await msg.edit("عکس پروفایل گروه با موفقیت حذف شد!")
        else:
            await msg.edit("شما اجازه حذف عکس پروفایل گروه را ندارید.")
    except Exception as e:
        logging.error(f"خطا در اجرای دستور removephoto: {e}")
        await message.reply_text("خطا در اجرای دستور!")

# دستور تنظیم عکس پروفایل گروه
@app.on_message(filters.command("setphoto"))
@adminsOnly("can_change_info")
async def setchatphoto(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند.")
        return
    
    if not reply:
        await msg.edit("لطفاً به یک عکس یا سند پاسخ دهید.")
        return

    try:
        if admin_check.privileges.can_change_info:
            photo = await reply.download()
            await message.chat.set_photo(photo=photo)
            await msg.edit_text(f"عکس پروفایل گروه تغییر یافت!\nتوسط {message.from_user.mention}")
        else:
            await msg.edit("شما اجازه تغییر عکس پروفایل گروه را ندارید.")
    except Exception as e:
        logging.error(f"خطا در اجرای دستور setphoto: {e}")
        await msg.edit("خطا در اجرای دستور!")

# دستور تنظیم عنوان گروه
@app.on_message(filters.command("settitle"))
@adminsOnly("can_change_info")
async def setgrouptitle(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند.")
        return
    
    if reply:
        try:
            title = reply.text
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_title(title)
                await msg.edit(f"عنوان گروه تغییر یافت!\nتوسط {message.from_user.mention}")
            else:
                await msg.edit("شما اجازه تغییر عنوان گروه را ندارید.")
        except Exception as e:
            logging.error(f"خطا در اجرای دستور settitle: {e}")
            await msg.edit("خطا در اجرای دستور!")
    else:
        await msg.edit("لطفاً به یک پیام متنی پاسخ دهید تا عنوان گروه را تغییر دهید.")

# دستور تنظیم توضیحات گروه
@app.on_message(filters.command(["setdiscription", "setdesc"]))
@adminsOnly("can_change_info")
async def setg_discription(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند.")
        return
    
    if reply:
        try:
            discription = reply.text
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_description(discription)
                await msg.edit(f"توضیحات گروه تغییر یافت!\nتوسط {message.from_user.mention}")
            else:
                await msg.edit("شما اجازه تغییر توضیحات گروه را ندارید.")
        except Exception as e:
            logging.error(f"خطا در اجرای دستور setdiscription: {e}")
            await msg.edit("خطا در اجرای دستور!")
    else:
        await msg.edit("لطفاً به یک پیام متنی پاسخ دهید تا توضیحات گروه را تغییر دهید.")
