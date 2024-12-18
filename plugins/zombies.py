from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config

# Initialize Pyrogram Client
app = Client("my_bot", api_id=config.api_id, api_hash=config.api_hash, bot_token=config.bot_token)

REQUIRED_CHANNELS = []
JOIN_MANDATORY = False
OWNER_ID = 1924774929

# Helper function to check membership and send response
async def check_user_membership(client, user_id):
    missing_channels = [
        channel for channel in REQUIRED_CHANNELS if not await is_member(client, user_id, channel)
    ]
    return missing_channels

# Check if a user is a member of a channel
async def is_member(client, user_id, channel):
    try:
        await client.get_chat_member(channel, user_id)
        return True
    except UserNotParticipant:
        return False

# Command handler for the owner to manage mandatory join
@app.on_message(filters.text & filters.user(OWNER_ID))
async def manage_mandatory_join(client, message):
    global REQUIRED_CHANNELS, JOIN_MANDATORY
    text = message.text.strip()

    if text == "جوین اجباری":
        await message.reply("لطفاً لینک یا شناسه عددی کانالی که می‌خواهید به لیست جوین اجباری اضافه کنید را ارسال کنید.")
    elif text.startswith("https://") or text.isdigit():
        channel = text
        if text.startswith("https://"):
            channel = text.split('/')[-1]
        if channel not in REQUIRED_CHANNELS:
            REQUIRED_CHANNELS.append(channel)
            await message.reply(f"کانال @{channel} به لیست جوین اجباری اضافه شد.")
        else:
            await message.reply(f"کانال @{channel} از قبل در لیست موجود است.")
    elif text == "لیست جوین اجباری":
        channels_list = "\n".join(REQUIRED_CHANNELS) if REQUIRED_CHANNELS else "هیچ کانالی به لیست اضافه نشده است."
        await message.reply(f"کانال‌های جوین اجباری:\n{channels_list}")
    elif text == "حذف جوین":
        await message.reply("لطفاً لینک یا شناسه عددی کانالی که می‌خواهید از لیست حذف کنید را ارسال کنید.")
    elif text == "جوین روشن":
        JOIN_MANDATORY = True
        await message.reply("قابلیت جوین اجباری فعال شد.")
    elif text == "جوین خاموش":
        JOIN_MANDATORY = False
        await message.reply("قابلیت جوین اجباری غیرفعال شد.")

# Middleware to check user membership
@app.on_message(filters.command)
async def check_membership(client, message):
    if not JOIN_MANDATORY or not REQUIRED_CHANNELS:
        return  # Skip check if feature is disabled

    missing_channels = await check_user_membership(client, message.from_user.id)
    if missing_channels:
        buttons = [
            [InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{channel}") for channel in missing_channels],
            [InlineKeyboardButton("عضو شدم", callback_data="check_membership")]
        ]
        await message.reply(
            "برای استفاده از ربات، ابتدا در کانال‌های زیر عضو شوید:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

# Callback handler for "عضو شدم"
@app.on_callback_query(filters.regex("check_membership"))
async def confirm_membership(client, callback_query):
    missing_channels = await check_user_membership(client, callback_query.from_user.id)
    message = "شما هنوز عضو نشده‌اید." if missing_channels else "شما می‌توانید از ربات استفاده کنید."
    await callback_query.answer(message, show_alert=True)
