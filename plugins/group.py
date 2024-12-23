import logging
from pyrogram import enums, filters
from YukkiMusic import app
from utils.permissions import adminsOnly

# تنظیمات logging برای اشکال‌زدایی
logging.basicConfig(level=logging.DEBUG)

# دستور تست برای بررسی عملکرد ربات
@app.on_message(filters.command("test"))
async def test_command(_, message):
    await message.reply_text("دستور test با موفقیت اجرا شد!")

# دستور حذف عکس پروفایل گروه
@app.on_message(filters.command("removephoto"))
@adminsOnly("can_change_info")
async def deletechatphoto(_, message):
    logging.debug("دستور removephoto اجرا شد!")  # برای اشکال‌زدایی
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش....")
    
    admin_check = await app.get_chat_member(chat_id, user_id)
    
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند.")
    
    elif admin_check.privileges.can_change_info:
        try:
            await app.delete_chat_photo(chat_id)
            await msg.edit("عکس پروفایل گروه با موفقیت حذف شد!")
        except Exception as e:
            logging.error(f"خطا در حذف عکس پروفایل: {e}")
            await msg.edit("خطا در حذف عکس پروفایل.")
    else:
        await msg.edit("شما اجازه حذف عکس پروفایل گروه را ندارید.")

# دستور تنظیم عکس پروفایل گروه
@app.on_message(filters.command("setphoto"))
@adminsOnly("can_change_info")
async def setchatphoto(_, message):
    logging.debug("دستور setphoto اجرا شد!")  # برای اشکال‌زدایی
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    
    admin_check = await app.get_chat_member(chat_id, user_id)
    
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند.")
    
    elif not reply:
        await msg.edit("لطفاً به یک عکس یا فایل پاسخ دهید.")
    
    else:
        try:
            if admin_check.privileges.can_change_info:
                photo = await reply.download()
                await message.chat.set_photo(photo=photo)
                await msg.edit("عکس پروفایل گروه با موفقیت تغییر کرد!")
            else:
                await msg.edit("شما اجازه تغییر عکس پروفایل گروه را ندارید.")
        except Exception as e:
            logging.error(f"خطا در تنظیم عکس پروفایل: {e}")
            await msg.edit("خطا در تغییر عکس پروفایل.")

# دستور تنظیم نام گروه
@app.on_message(filters.command("settitle"))
@adminsOnly("can_change_info")
async def setgrouptitle(_, message):
    logging.debug("دستور settitle اجرا شد!")  # برای اشکال‌زدایی
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند.")
    
    elif reply:
        try:
            title = message.reply_to_message.text
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_title(title)
                await msg.edit("نام گروه با موفقیت تغییر کرد!")
        except Exception as e:
            logging.error(f"خطا در تنظیم نام گروه: {e}")
            await msg.edit("خطا در تغییر نام گروه.")
    
    elif len(message.command) > 1:
        try:
            title = message.text.split(None, 1)[1]
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_title(title)
                await msg.edit("نام گروه با موفقیت تغییر کرد!")
        except Exception as e:
            logging.error(f"خطا در تنظیم نام گروه: {e}")
            await msg.edit("خطا در تغییر نام گروه.")
    
    else:
        await msg.edit("لطفاً به متن پاسخ دهید یا متنی برای تغییر نام گروه وارد کنید.")

# دستور تنظیم توضیحات گروه
@app.on_message(filters.command(["setdiscription", "setdesc"]))
@adminsOnly("can_change_info")
async def setg_discription(_, message):
    logging.debug("دستور setdiscription اجرا شد!")  # برای اشکال‌زدایی
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("در حال پردازش...")
    
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("این دستور فقط در گروه‌ها کار می‌کند.")
    
    elif reply:
        try:
            discription = message.reply_to_message.text
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_description(discription)
                await msg.edit("توضیحات گروه با موفقیت تغییر کرد!")
        except Exception as e:
            logging.error(f"خطا در تنظیم توضیحات گروه: {e}")
            await msg.edit("خطا در تغییر توضیحات گروه.")
    
    elif len(message.command) > 1:
        try:
            discription = message.text.split(None, 1)[1]
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_description(discription)
                await msg.edit("توضیحات گروه با موفقیت تغییر کرد!")
        except Exception as e:
            logging.error(f"خطا در تنظیم توضیحات گروه: {e}")
            await msg.edit("خطا در تغییر توضیحات گروه.")
    
    else:
        await msg.edit("لطفاً به متن پاسخ دهید یا متنی برای تغییر توضیحات گروه وارد کنید.")
