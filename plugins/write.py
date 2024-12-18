from pyrogram import filters
from TheApi import api
from YukkiMusic import app
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

# ذخیره چت‌ها در یک دیکشنری
chats = {}

@app.on_message(filters.command("setchat") & filters.group)
async def set_chat(client, message: Message):
    # بررسی ادمین بودن کاربر
    chat = await message.chat
    admins = await client.get_chat_members(chat.id, filter="administrators")
    admin_ids = [admin.user.id for admin in admins]

    if message.from_user.id not in admin_ids:
        await message.reply_text("شما اجازه استفاده از این دستور را ندارید.")
        return

    # بررسی اینکه آیا پیامی به ریپلای شده
    if not message.reply_to_message:
        await message.reply_text("لطفاً یک پیام یا عکس/گیف را ریپلای کنید.")
        return

    # گرفتن نام چت از پیام
    if len(message.command) < 2:
        await message.reply_text("لطفاً نام چت را وارد کنید.")
        return

    chat_name = message.command[1]
    
    # ذخیره پیام/عکس/گیف
    chats[chat_name] = {
        'message': message.reply_to_message.text or message.reply_to_message.caption,
        'user_id': message.from_user.id
    }

    await message.reply_text(f"چت با نام '{chat_name}' با موفقیت ذخیره شد.")

@app.on_message(filters.text & filters.group)
async def respond_chat(client, message: Message):
    # بررسی اینکه آیا پیامی که ارسال شده معادل یک نام ذخیره‌شده است
    if message.text in chats:
        chat_info = chats[message.text]
        text_to_send = chat_info['message']
        user_id = chat_info['user_id']
        
        # تگ کردن کاربر
        user = await client.get_users(user_id)
        tagged_user = f"<a href='tg://user?id={user.id}'>{user.first_name}</a>"

        # ارسال پیام با تگ و چت
        await message.reply_text(f"{tagged_user} : {text_to_send}", disable_web_page_preview=True)

@app.on_message(filters.command("delchat") & filters.group)
async def del_chat(client, message: Message):
    # بررسی ادمین بودن کاربر
    chat = await message.chat
    admins = await client.get_chat_members(chat.id, filter="administrators")
    admin_ids = [admin.user.id for admin in admins]

    if message.from_user.id not in admin_ids:
        await message.reply_text("شما اجازه استفاده از این دستور را ندارید.")
        return

    if len(message.command) < 2:
        await message.reply_text("لطفاً نام چت را وارد کنید.")
        return

    chat_name = message.command[1]

    # حذف چت
    if chat_name in chats:
        del chats[chat_name]
        await message.reply_text(f"چت با نام '{chat_name}' حذف شد.")
    else:
        await message.reply_text(f"چت با نام '{chat_name}' پیدا نشد.")
