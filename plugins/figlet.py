from pyrogram import Client, InlineKeyboardButton, InlineKeyboardMarkup, filters
from pyrogram.types import CallbackQuery
import asyncio
from YukkiMusic import app  # اطلاعات ربات از اینجا وارد می‌شود

# ذخیره پیام‌های مخفی
hidden_messages = {}

@app.on_message(filters.command("نجوا"))
async def send_hidden_message(bot, message):
    # گرفتن متن پیام و دریافت گیرنده
    try:
        text = message.text.split(" ", 1)[1]
        user_id = int(message.reply_to_message.text.split(" ")[0])  # دریافت ID کاربر برای ارسال پیام
    except IndexError:
        return await message.reply_text("مثال:\n\n/نجوا 123456789 متن پیام")

    # ذخیره پیام مخفی
    hidden_messages[user_id] = {"message": text, "sender": message.from_user.id}

    # ارسال پیام به ربات و درخواست تأیید
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("ارسال به پیوی", callback_data=f"send_to_pv_{user_id}")],
            [InlineKeyboardButton("ارسال در گروه", callback_data=f"send_in_group_{user_id}")],
            [InlineKeyboardButton("بستن", callback_data="close")]
        ]
    )
    await message.reply_text("پیام به طور ناشناس آماده ارسال است. لطفاً گزینه مورد نظر خود را انتخاب کنید.", reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"send_to_pv_"))
async def send_to_pv(Client, query: CallbackQuery):
    user_id = int(query.data.split("_")[3])
    
    # دریافت پیام مخفی
    if user_id in hidden_messages:
        hidden_message = hidden_messages[user_id]["message"]
        sender_id = hidden_messages[user_id]["sender"]
        
        # ارسال پیام به پیوی دریافت‌کننده
        try:
            await query.bot.send_message(user_id, f"پیام از طرف {sender_id}:\n{hidden_message}")
            await query.message.edit_text("پیام به پیوی ارسال شد.", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("پاسخ به پیام", callback_data=f"reply_{user_id}")]]
            ))
        except Exception as e:
            await query.answer(f"خطا در ارسال پیام به پیوی: {e}", show_alert=True)


@app.on_callback_query(filters.regex(r"send_in_group_"))
async def send_in_group(Client, query: CallbackQuery):
    user_id = int(query.data.split("_")[3])
    
    # دریافت پیام مخفی
    if user_id in hidden_messages:
        hidden_message = hidden_messages[user_id]["message"]
        
        # ارسال پیام در گروه
        try:
            await query.message.reply_text(f"پیام ناشناس از {user_id}:\n{hidden_message}")
            await query.message.edit_text("پیام به گروه ارسال شد.", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("پاسخ به پیام", callback_data=f"reply_{user_id}")]]
            ))
        except Exception as e:
            await query.answer(f"خطا در ارسال پیام به گروه: {e}", show_alert=True)


@app.on_callback_query(filters.regex(r"reply_"))
async def reply_to_hidden_message(Client, query: CallbackQuery):
    user_id = int(query.data.split("_")[1])
    
    # بررسی اینکه پیام پاسخ داده شده است
    if user_id in hidden_messages:
        hidden_message = hidden_messages[user_id]["message"]
        
        # ارسال پیام پاسخ به کاربر به طور ناشناس
        try:
            await query.bot.send_message(user_id, f"پاسخ به پیام ناشناس:\n{hidden_message}")
            await query.message.edit_text("پیام شما به طور ناشناس ارسال شد.", reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("پاسخ به پیام", callback_data=f"reply_{user_id}")]]
            ))
        except Exception as e:
            await query.answer(f"خطا در ارسال پیام: {e}", show_alert=True)


@app.on_callback_query(filters.regex("close"))
async def close_handler(Client, query: CallbackQuery):
    # بستن پیام
    await query.message.delete()
