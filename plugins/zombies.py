from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app

# Database or in-memory dictionary to store required channels and settings
REQUIRED_CHANNELS = []
JOIN_MANDATORY = False  # Toggle to enable or disable the feature
OWNER_ID = 1924774929  # Replace with the owner's user ID

# Command to add a channel to mandatory join list or toggle feature
@app.on_message(filters.text & filters.user(OWNER_ID))
async def manage_mandatory_join(client, message):
    global REQUIRED_CHANNELS, JOIN_MANDATORY
    text = message.text.strip()

    # Add channel to the list
    if text == "جوین اجباری":
        await message.reply("لطفاً لینک یا شناسه عددی کانالی که می‌خواهید به لیست جوین اجباری اضافه کنید را ارسال کنید.")

    elif text.startswith("https://") or text.isdigit():
        # Channel ID or link has been provided
        channel = text
        if channel not in REQUIRED_CHANNELS:
            REQUIRED_CHANNELS.append(channel)
            await message.reply(f"کانال @{channel} به لیست جوین اجباری اضافه شد.")
        else:
            await message.reply(f"کانال @{channel} از قبل در لیست جوین اجباری موجود است.")

    # List all required channels
    elif text == "لیست جوین اجباری":
        if REQUIRED_CHANNELS:
            channels_list = "\n".join(REQUIRED_CHANNELS)
            await message.reply(f"کانال‌های جوین اجباری:\n{channels_list}")
        else:
            await message.reply("هیچ کانالی به لیست جوین اجباری اضافه نشده است.")

    # Remove channel from the list
    elif text == "حذف جوین":
        await message.reply("لطفاً لینک یا شناسه عددی کانالی که می‌خواهید از لیست جوین اجباری حذف کنید را ارسال کنید.")

    elif text.startswith("https://") or text.isdigit():
        # Channel ID or link has been provided to remove
        channel = text
        if channel in REQUIRED_CHANNELS:
            REQUIRED_CHANNELS.remove(channel)
            await message.reply(f"کانال @{channel} از لیست جوین اجباری حذف شد.")
        else:
            await message.reply(f"کانال @{channel} در لیست جوین اجباری وجود ندارد.")

    # Enable mandatory join feature
    elif text == "جوین روشن":
        JOIN_MANDATORY = True
        await message.reply("قابلیت جوین اجباری فعال شد. کاربران باید عضو کانال‌ها شوند تا بتوانند از ربات استفاده کنند.")

    # Disable mandatory join feature
    elif text == "جوین خاموش":
        JOIN_MANDATORY = False
        await message.reply("قابلیت جوین اجباری غیرفعال شد. کاربران نیازی به عضویت در کانال‌ها ندارند.")

# Middleware to check user membership
@app.on_message(filters.command)
async def check_membership(client, message):
    if not JOIN_MANDATORY or not REQUIRED_CHANNELS:
        return  # Skip check if the feature is disabled or no channels are set

    user_id = message.from_user.id
    missing_channels = []

    for channel in REQUIRED_CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            missing_channels.append(channel)

    if missing_channels:
        # Generate inline keyboard buttons for missing channels
        buttons = [
            [InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{channel}") for channel in missing_channels],
            [InlineKeyboardButton("عضو شدم", callback_data="check_membership")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        await message.reply(
            "برای استفاده از ربات، ابتدا در کانال‌های زیر عضو شوید:",
            reply_markup=reply_markup
        )
        return  # Stop further processing if not a member

# Callback handler for "عضو شدم" button
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
    await callback_query.answer("شما هنوز عضو نشده‌اید.", show_alert=True)
else:
    await callback_query.answer("شما می‌توانید از ربات استفاده کنید.", show_alert=True)
