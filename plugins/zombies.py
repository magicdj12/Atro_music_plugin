from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID

# تعریف اپلیکیشن
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# لیست کانال‌های اجباری و وضعیت جوین اجباری
REQUIRED_CHANNELS = []  # کانال‌های اجباری
JOIN_MANDATORY = False  # وضعیت جوین اجباری

# دستورات مدیریت جوین اجباری توسط مالک ربات
@app.on_message(filters.text & filters.user(OWNER_ID))
async def manage_mandatory_join(client, message):
    global REQUIRED_CHANNELS, JOIN_MANDATORY
    text = message.text.strip()

    if text == "جوین اجباری":
        await message.reply("لطفاً لینک یا شناسه عددی کانال مورد نظر را ارسال کنید.")

    elif text.startswith("https://") or text.isdigit():
        channel = text
        if channel not in REQUIRED_CHANNELS:
            REQUIRED_CHANNELS.append(channel)
            await message.reply(f"کانال {channel} به لیست جوین اجباری اضافه شد.")
        else:
            await message.reply(f"کانال {channel} قبلاً اضافه شده است.")

    elif text == "لیست جوین اجباری":
        if REQUIRED_CHANNELS:
            channels_list = "\n".join(REQUIRED_CHANNELS)
            await message.reply(f"کانال‌های اجباری:\n{channels_list}")
        else:
            await message.reply("هیچ کانالی در لیست وجود ندارد.")

    elif text == "حذف جوین":
        await message.reply("لطفاً لینک یا شناسه عددی کانال مورد نظر را ارسال کنید.")

    elif text.startswith("حذف https://") or text.isdigit():
        channel = text.replace("حذف ", "")
        if channel in REQUIRED_CHANNELS:
            REQUIRED_CHANNELS.remove(channel)
            await message.reply(f"کانال {channel} از لیست جوین اجباری حذف شد.")
        else:
            await message.reply(f"کانال {channel} در لیست وجود ندارد.")

    elif text == "جوین روشن":
        JOIN_MANDATORY = True
        await message.reply("جوین اجباری فعال شد.")

    elif text == "جوین خاموش":
        JOIN_MANDATORY = False
        await message.reply("جوین اجباری غیرفعال شد.")

# بررسی عضویت کاربران
@app.on_message(filters.command)
async def check_user_membership(client, message):
    if not JOIN_MANDATORY or not REQUIRED_CHANNELS:
        return  # اگر جوین اجباری غیرفعال باشد، چک نکن

    user_id = message.from_user.id
    missing_channels = []

    for channel in REQUIRED_CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            missing_channels.append(channel)

    if missing_channels:
        buttons = [
            [InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{channel}")]
            for channel in missing_channels
        ]
        buttons.append([InlineKeyboardButton("عضو شدم", callback_data="check_membership")])

        reply_markup = InlineKeyboardMarkup(buttons)

        await message.reply(
            "برای استفاده از ربات، ابتدا در کانال‌های زیر عضو شوید:",
            reply_markup=reply_markup
        )
        return

# بررسی دوباره عضویت کاربر هنگام زدن دکمه "عضو شدم"
@app.on_callback_query(filters.regex("check_membership"))
async def confirm_user_membership(client, callback_query):
    user_id = callback_query.from_user.id
    missing_channels = []

    for channel in REQUIRED_CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            missing_channels.append(channel)

    if missing_channels:
        await callback_query.answer("شما هنوز عضو نشده‌اید.", show_alert=True)
    else:
        await callback_query.answer("شما می‌توانید از ربات استفاده کنید.", show_alert=True)

# اجرای ربات
if name == "main":
    app.run()
