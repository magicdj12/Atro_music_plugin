import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
import time
from datetime import datetime, timedelta

from YukkiMusic import app

# ذخیره پیام‌های مخفی و اطلاعات مرتبط با آن‌ها
hidden_messages = {}
expiration_time = 60 * 60  # مدت زمان انقضا (یک ساعت)

@app.on_message(filters.command("نجوا") & filters.group)  # فقط در گروه‌ها اجرا شود
async def secret_message(bot, message: Message):
    try:
        # استخراج متن پیام و id یا username کاربر
        text = message.text.split(" ", 1)[1]
        user_info = text.split(" ", 1)
        user_id = int(user_info[0]) if user_info[0].isdigit() else user_info[0]
        message_text = user_info[1] if len(user_info) > 1 else "لطفا پیامی برای ارسال وارد کنید."

        # ارسال پیام مخفی به کاربر
        user = await bot.get_users(user_id)
        reply_text = f"پیام مخفی ارسال شد به {user.first_name}:\n{message_text}"

        # ذخیره پیام در hidden_messages به همراه زمان ارسال
        hidden_messages[user_id] = {
            "message": message_text,
            "sender": message.from_user.id,
            "timestamp": time.time()
        }

        # ایجاد کلیدهای شیشه‌ای برای نمایش، حذف، و پاسخ
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("نمایش پیام", callback_data=f"show_{user_id}")],
                [InlineKeyboardButton("حذف پیام", callback_data=f"delete_{user_id}")],
                [InlineKeyboardButton("پاسخ پیام", callback_data=f"reply_{user_id}")],
                [InlineKeyboardButton("ویرایش پیام", callback_data=f"edit_{user_id}")],  # ویرایش پیام
            ]
        )

        # ارسال پیام به گروه
        await message.reply_text(
            f"پیام مخفی به {user.first_name} ارسال شد.",
            reply_markup=keyboard
        )

        # ارسال اعلان برای دریافت‌کننده
        await bot.send_message(user_id, f"شما یک پیام مخفی از {message.from_user.first_name} دارید. برای نمایش یا حذف آن از دکمه‌ها استفاده کنید.")

    except Exception as e:
        await message.reply_text(f"خطا در ارسال پیام: {str(e)}")

@app.on_callback_query(filters.regex(r"show_"))
async def show_message(Client, query: CallbackQuery):
    user_id = int(query.data.split("_")[1])
    if user_id in hidden_messages:
        # ارسال پیام مخفی به کاربر
        hidden_message = hidden_messages[user_id]["message"]
        sender_id = hidden_messages[user_id]["sender"]
        sender = await query.bot.get_users(sender_id)

        # بررسی زمان انقضا پیام
        if time.time() - hidden_messages[user_id]["timestamp"] > expiration_time:
            del hidden_messages[user_id]
            await query.answer("این پیام منقضی شده است.", show_alert=True)
            return

        await query.message.edit_text(
            f"پیام مخفی از {sender.first_name}:\n<pre>{hidden_message}</pre>",
            reply_markup=query.message.reply_markup
        )
    else:
        await query.answer("هیچ پیامی برای این کاربر پیدا نشد.", show_alert=True)

@app.on_callback_query(filters.regex(r"delete_"))
async def delete_message(Client, query: CallbackQuery):
    user_id = int(query.data.split("_")[1])
    if user_id in hidden_messages:
        # حذف پیام مخفی
        del hidden_messages[user_id]
        await query.message.edit_text("پیام مخفی حذف شد.", reply_markup=None)
    else:
        await query.answer("هیچ پیامی برای این کاربر پیدا نشد.", show_alert=True)

@app.on_callback_query(filters.regex(r"reply_"))
async def reply_message(Client, query: CallbackQuery):
    user_id = int(query.data.split("_")[1])
    # ارسال پیام ناشناس به کاربر
    await query.message.edit_text("لطفاً پیامی برای پاسخ ارسال کنید.")

    @app.on_message(filters.text & filters.private)
    async def secret_reply(bot, message: Message):
        if message.text.startswith("/"):
            return  # ignore commands

# ارسال پیام به کاربر هدف به صورت ناشناس
        await bot.send_message(
            user_id,
            f"پیام ناشناس به شما از {message.from_user.first_name}:\n{message.text}"
        )
        await message.reply_text("پاسخ ناشناس به کاربر ارسال شد.")

@app.on_callback_query(filters.regex(r"edit_"))
async def edit_message(Client, query: CallbackQuery):
    user_id = int(query.data.split("_")[1])
    if user_id in hidden_messages:
        # درخواست ویرایش پیام از ارسال‌کننده
        await query.message.edit_text("لطفاً متن جدید پیام را وارد کنید.")

        @app.on_message(filters.text & filters.private)
        async def edit_reply(bot, message: Message):
            if message.text.startswith("/"):
                return  # ignore commands

            # ویرایش پیام و ذخیره آن
            hidden_messages[user_id]["message"] = message.text
            await bot.send_message(
                user_id,
                f"پیام ناشناس ویرایش شد:\n{message.text}"
            )
            await message.reply_text("پیام ویرایش شد.")
            await query.message.edit_text("پیام مخفی ویرایش شد.", reply_markup=None)
    else:
        await query.answer("هیچ پیامی برای این کاربر پیدا نشد.", show_alert=True)
