from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

REQUIRED_CHANNELS = []  # کانال‌های اجباری
JOIN_MANDATORY = False  # وضعیت جوین اجباری

@app.on_message(filters.text & filters.user(OWNER_ID))
async def manage_join_settings(client, message):
    global REQUIRED_CHANNELS, JOIN_MANDATORY
    text = message.text.strip()

    if text == "جوین اجباری":
        await message.reply("لینک کانال را ارسال کنید.")

    elif text.startswith("https://") or text.isdigit():
        channel = text
        if channel not in REQUIRED_CHANNELS:
            REQUIRED_CHANNELS.append(channel)
            await message.reply(f"کانال {channel} اضافه شد.")
        else:
            await message.reply(f"کانال {channel} قبلاً اضافه شده است.")

    elif text == "لیست کانال‌ها":
        if REQUIRED_CHANNELS:
            await message.reply("\n".join(REQUIRED_CHANNELS))
        else:
            await message.reply("هیچ کانالی اضافه نشده است.")

    elif text == "جوین روشن":
        JOIN_MANDATORY = True
        await message.reply("جوین اجباری فعال شد.")

    elif text == "جوین خاموش":
        JOIN_MANDATORY = False
        await message.reply("جوین اجباری غیرفعال شد.")

    elif text.startswith("حذف "):
        channel = text.replace("حذف ", "")
        if channel in REQUIRED_CHANNELS:
            REQUIRED_CHANNELS.remove(channel)
            await message.reply(f"کانال {channel} حذف شد.")
        else:
            await message.reply(f"کانال {channel} وجود ندارد.")

@app.on_message(filters.text & ~filters.user(OWNER_ID))
async def check_user_membership(client, message):
    if not JOIN_MANDATORY or not REQUIRED_CHANNELS:
        return

    user_id = message.from_user.id
    missing_channels = []

    for channel in REQUIRED_CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            missing_channels.append(channel)

    if missing_channels:
        buttons = [
            [InlineKeyboardButton(f"عضویت در {channel}", url=f"https://t.me/{channel}") for channel in missing_channels],
            [InlineKeyboardButton("عضو شدم", callback_data="check_membership")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        await message.reply(
            "ابتدا در کانال‌های زیر عضو شوید:",
            reply_markup=reply_markup
        )

@app.on_callback_query(filters.regex("check_membership"))
async def confirm_membership(client, callback_query):
    user_id = callback_query.from_user.id
    missing_channels = []

    for channel in REQUIRED_CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            missing_channels.append(channel)

    if missing_channels:
        await callback_query.answer("عضویت شما کامل نیست.", show_alert=True)
    else:
        await callback_query.answer("عضویت تأیید شد. اکنون می‌توانید از ربات استفاده کنید.", show_alert=True)

