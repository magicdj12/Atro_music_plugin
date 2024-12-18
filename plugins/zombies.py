from pyrogram import filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app  # استفاده از اپلیکیشن اصلی
from config import OWNER_ID  # شناسه مالک از فایل config

# لیست کانال‌های اجباری و وضعیت جوین
REQUIRED_CHANNELS = []
JOIN_MANDATORY = False


@app.on_message(filters.user(OWNER_ID) & filters.command(["جوین_اجباری", "حذف_جوین", "لیست_جوین", "جوین_روشن", "جوین_خاموش"], prefixes=["/"]))
async def manage_join(client, message):
    global REQUIRED_CHANNELS, JOIN_MANDATORY
    command = message.command[0]

    if command == "جوین_اجباری":
        await message.reply("لینک یا آیدی کانال را ارسال کنید.")
        reply = await app.listen(message.chat.id)
        channel = reply.text
        if channel not in REQUIRED_CHANNELS:
            REQUIRED_CHANNELS.append(channel)
            await message.reply(f"کانال {channel} به لیست جوین اجباری اضافه شد.")
        else:
            await message.reply(f"کانال {channel} قبلاً در لیست وجود دارد.")

    elif command == "حذف_جوین":
        await message.reply("لینک یا آیدی کانال موردنظر برای حذف را ارسال کنید.")
        reply = await app.listen(message.chat.id)
        channel = reply.text
        if channel in REQUIRED_CHANNELS:
            REQUIRED_CHANNELS.remove(channel)
            await message.reply(f"کانال {channel} از لیست جوین اجباری حذف شد.")
        else:
            await message.reply(f"کانال {channel} در لیست وجود ندارد.")

    elif command == "لیست_جوین":
        if REQUIRED_CHANNELS:
            channels_list = "\n".join(REQUIRED_CHANNELS)
            await message.reply(f"لیست کانال‌های اجباری:\n{channels_list}")
        else:
            await message.reply("هیچ کانالی در لیست وجود ندارد.")

    elif command == "جوین_روشن":
        JOIN_MANDATORY = True
        await message.reply("جوین اجباری فعال شد.")

    elif command == "جوین_خاموش":
        JOIN_MANDATORY = False
        await message.reply("جوین اجباری غیرفعال شد.")


@app.on_message(filters.command & filters.group)
async def check_membership(client, message):
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
