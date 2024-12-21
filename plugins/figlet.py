# import asyncio
# from pyrogram import Client, filters
# from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
# from pyrogram.errors import FloodWait
# import time

# from YukkiMusic import app

# # ذخیره پیام‌ها و اطلاعات آنها
# hidden_messages = {}

# @app.on_message(filters.command("نجوا") & filters.group)  # فقط در گروه‌ها اجرا شود
# async def secret_message(bot, message: Message):
#     try:
#         # استخراج اطلاعات
#         text = message.text.split(" ", 1)[1]
#         user_info = text.split(" ", 1)
#         user_id = int(user_info[0]) if user_info[0].isdigit() else user_info[0]
#         message_text = user_info[1] if len(user_info) > 1 else "لطفا پیامی برای ارسال وارد کنید."

#         # ارسال پیام به ربات (برای ذخیره و جلوگیری از ارسال در گروه)
#         user = await bot.get_users(user_id)
#         hidden_messages[user_id] = {
#             "message": message_text,
#             "sender": message.from_user.id,
#             "timestamp": time.time()
#         }

#         # دکمه‌ها برای مدیریت پیام
#         keyboard = InlineKeyboardMarkup(
#             [
#                 [InlineKeyboardButton("ویرایش پیام", callback_data=f"edit_{user_id}")],
#                 [InlineKeyboardButton("حذف پیام", callback_data=f"delete_{user_id}")],
#                 [InlineKeyboardButton("ارسال به پیوی", callback_data=f"send_private_{user_id}")],
#                 [InlineKeyboardButton("ارسال به صورت ناشناس", callback_data=f"send_anonymous_{user_id}")],
#                 [InlineKeyboardButton("ارسال از طرف من", callback_data=f"send_from_me_{user_id}")],
#                 [InlineKeyboardButton("بستن", callback_data="close")]
#             ]
#         )

#         # ارسال اعلان به ارسال‌کننده
#         await message.reply_text(f"پیام مخفی به {user.first_name} آماده ارسال است.", reply_markup=keyboard)

#         # ارسال پیام مخفی به پیوی دریافت‌کننده
#         await bot.send_message(user_id, f"شما یک پیام مخفی از {message.from_user.first_name} دارید. برای مدیریت آن از دکمه‌ها استفاده کنید.")

#         # ارسال پیام در گروه بدون نمایش متن
#         await message.delete()  # حذف پیام از گروه

#     except Exception as e:
#         await message.reply_text(f"خطا در ارسال پیام: {str(e)}")

# @app.on_callback_query(filters.regex(r"send_private_"))
# async def send_private(Client, query: CallbackQuery):
#     user_id = int(query.data.split("_")[2])

#     if user_id in hidden_messages:
#         hidden_message = hidden_messages[user_id]["message"]
#         sender_id = hidden_messages[user_id]["sender"]
#         sender = await query.bot.get_users(sender_id)

#         # ارسال پیام مخفی به پیوی
#         sent_message = await query.bot.send_message(user_id, f"پیام مخفی از {sender.first_name}:\n{hidden_message}")

#         # دکمه‌ها برای کاربر ارسال‌کننده
#         keyboard = InlineKeyboardMarkup(
#             [
#                 [InlineKeyboardButton("پاسخ به پیام", callback_data=f"reply_{user_id}_{sent_message.message_id}")],
#                 [InlineKeyboardButton("بستن", callback_data="close")]
#             ]
#         )
#         await query.message.edit_text("پیام مخفی به پیوی ارسال شد.", reply_markup=keyboard)

# @app.on_callback_query(filters.regex(r"send_anonymous_"))
# async def send_anonymous(Client, query: CallbackQuery):
#     user_id = int(query.data.split("_")[2])

#     if user_id in hidden_messages:
#         hidden_message = hidden_messages[user_id]["message"]

#         # ارسال پیام به صورت ناشناس (بدون مشخص شدن ارسال‌کننده)
#         await query.bot.send_message(user_id, f"پیام مخفی:\n{hidden_message}")

#         # دکمه‌ها برای کاربر ارسال‌کننده
#         keyboard = InlineKeyboardMarkup(
#             [
#                 [InlineKeyboardButton("پاسخ به پیام", callback_data=f"reply_{user_id}")],
#                 [InlineKeyboardButton("بستن", callback_data="close")]
#             ]
#         )
#         await query.message.edit_text("پیام به صورت ناشناس ارسال شد.", reply_markup=keyboard)

# @app.on_callback_query(filters.regex(r"send_from_me_"))
# async def send_from_me(Client, query: CallbackQuery):
#     user_id = int(query.data.split("_")[2])
#     if user_id in hidden_messages:
#         hidden_message = hidden_messages[user_id]["message"]
#         sender_id = hidden_messages[user_id]["sender"]
#         sender = await query.bot.get_users(sender_id)

#         # ارسال پیام از طرف ارسال‌کننده با اطلاعات کاربر
#         message_with_sender_info = f"پیام از {sender.first_name} ({sender.username}) [چت آیدی: {sender_id}]:\n{hidden_message}"
#         await query.bot.send_message(user_id, message_with_sender_info)

#         # دکمه‌ها برای کاربر ارسال‌کننده
#         keyboard = InlineKeyboardMarkup(
#             [
#                 [InlineKeyboardButton("پاسخ به پیام", callback_data=f"reply_{user_id}")],
#                 [InlineKeyboardButton("بستن", callback_data="close")]
#             ]
#         )
#         await query.message.edit_text("پیام از طرف شما ارسال شد.", reply_markup=keyboard)

# @app.on_callback_query(filters.regex(r"edit_"))
# async def edit_message(Client, query: CallbackQuery):
#     user_id = int(query.data.split("_")[1])
#     if user_id in hidden_messages:
#         # درخواست ویرایش پیام از ارسال‌کننده
#         await query.message.edit_text("لطفاً متن جدید پیام را وارد کنید.")

#         @app.on_message(filters.text & filters.private)
#         async def edit_reply(bot, message: Message):
#             if message.text.startswith("/"):
#                 return  # ignore commands

#             # ویرایش پیام و ذخیره آن
#             hidden_messages[user_id]["message"] = message.text
#             await bot.send_message(
#                 user_id,
#                 f"پیام ناشناس ویرایش شد:\n{message.text}"
#             )
#             await message.reply_text("پیام ویرایش شد.")
#             await query.message.edit_text("پیام مخفی ویرایش شد.", reply_markup=None)
#     else:
#         await query.answer("هیچ پیامی برای این کاربر پیدا نشد.", show_alert=True)

# @app.on_callback_query(filters.regex(r"delete_"))
# async def delete_message(Client, query: CallbackQuery):
#     user_id = int(query.data.split("_")[1])
#     if user_id in hidden_messages:
#         # حذف پیام مخفی
#         del hidden_messages[user_id]
#         await query.message.edit_text("پیام مخفی حذف شد.", reply_markup=None)
#     else:
#         await query.answer("هیچ پیامی برای این کاربر پیدا نشد.", show_alert=True)

# @app.on_callback_query(filters.regex(r"reply_"))
# async def reply_message(Client, query: CallbackQuery):
#     # ارسال پیام ناشناس به کاربر
#     data = query.data.split("_")
#     user_id = int(data[1])
#     message_id = int(data[2])

#     await query.message.edit_text("لطفاً پیامی برای پاسخ ارسال کنید.")

#     @app.on_message(filters.text & filters.private)
#     async def secret_reply(bot, message: Message):
#         if message.text.startswith("/"):
#             return  # ignore commands

#         # ارسال پیام به کاربر هدف به صورت ناشناس
#         await bot.send_message(
#             user_id,
#             f"پیام ناشناس به شما از {message.from_user.first_name}:\n{message.text}"
#         )
#         await message.reply_text("پاسخ ناشناس به کاربر ارسال شد.")
#         await query.message.edit_text("پیام مخفی ویرایش شد.", reply_markup=None)

# @app.on_callback_query(filters.regex(r"close"))
# async def close_message(Client, query: CallbackQuery):
#     await query.message.delete()
