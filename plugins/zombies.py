from pyrogram import filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from YukkiMusic import app

# متغیرهای اصلی
REQUIRED_CHANNELS = []  # لیست کانال‌های اجباری
JOIN_MANDATORY = False  # وضعیت فعال یا غیرفعال بودن جوین اجباری

# متغیر موقت برای ذخیره مراحل اضافه کردن یا حذف کردن کانال
TEMP_STATE = {}

# لیست کاربران مجاز
SUDOERS = [1924774929]  # شناسه عددی مالک یا مدیران ربات


@app.on_message(filters.user(SUDOERS) & filters.command(["جوین_اجباری", "حذف_جوین", "لیست_جوین", "جوین_روشن", "جوین_خاموش"]))
async def manage_join(client, message):
    global REQUIRED_CHANNELS, JOIN_MANDATORY, TEMP_STATE
    command = message.command

    if command[0] == "جوین_اجباری":
        await message.reply("لطفاً لینک یا آیدی عددی کانال را ارسال کنید:")
        TEMP_STATE[message.from_user.id] = "add"

    elif command[0] == "حذف_جوین":
        await message.reply("لطفاً لینک یا آیدی کانالی که می‌خواهید حذف کنید را ارسال کنید:")
        TEMP_STATE[message.from_user.id] = "remove"

    elif command[0] == "لیست_جوین":
        if REQUIRED_CHANNELS:
            channels = "\n".join(REQUIRED_CHANNELS)
            await message.reply(f"لیست کانال‌های اجباری:\n{channels}")
        else:
            await message.reply("هیچ کانالی در لیست جوین اجباری وجود ندارد.")

    elif command[0] == "جوین_روشن":
        JOIN_MANDATORY = True
        await message.reply("جوین اجباری روشن شد. کاربران باید عضو کانال‌های اجباری شوند.")

    elif command[0] == "جوین_خاموش":
        JOIN_MANDATORY = False
        await message.reply("جوین اجباری خاموش شد. کاربران نیازی به عضویت در کانال‌ها ندارند.")

@app.on_message(filters.user(SUDOERS) & filters.text)
async def handle_channel_entry(client, message):
    global TEMP_STATE, REQUIRED_CHANNELS

    user_id = message.from_user.id
    if user_id not in TEMP_STATE:
        return

    if TEMP_STATE[user_id] == "add":
        channel = message.text.strip()
        if channel not in REQUIRED_CHANNELS:
            REQUIRED_CHANNELS.append(channel)
            await message.reply(f"کانال {channel} به لیست جوین اجباری اضافه شد.")
        else:
            await message.reply(f"کانال {channel} قبلاً اضافه شده است.")
        TEMP_STATE.pop(user_id)

    elif TEMP_STATE[user_id] == "remove":
        channel = message.text.strip()
        if channel in REQUIRED_CHANNELS:
            REQUIRED_CHANNELS.remove(channel)
            await message.reply(f"کانال {channel} از لیست جوین اجباری حذف شد.")
        else:
            await message.reply(f"کانال {channel} در لیست وجود ندارد.")
        TEMP_STATE.pop(user_id)


@app.on_message(filters.private)
async def check_user_membership(client, message):
    global REQUIRED_CHANNELS, JOIN_MANDATORY

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
            [InlineKeyboardButton(f"عضویت در {channel}", url=f"https://t.me/{channel}")]
            for channel in missing_channels
        ]
        buttons.append([InlineKeyboardButton("عضو شدم", callback_data="check_membership")])

        reply_markup = InlineKeyboardMarkup(buttons)

        await message.reply(
            "برای ادامه استفاده از ربات، لطفاً ابتدا در کانال‌های زیر عضو شوید:",
            reply_markup=reply_markup
        )


@app.on_callback_query(filters.regex("check_membership"))
async def confirm_membership(client, callback_query):
    global REQUIRED_CHANNELS

    user_id = callback_query.from_user.id
    missing_channels = []

    for channel in REQUIRED_CHANNELS:
        try:
            await client.get_chat_member(channel, user_id)
        except UserNotParticipant:
            missing_channels.append(channel)

if missing_channels:
        await callback_query.answer("شما هنوز عضو تمام کانال‌های الزامی نشده‌اید.", show_alert=True)
    else:
        await callback_query.answer("عضویت شما تأیید شد! حالا می‌توانید از ربات استفاده کنید.", show_alert=True)
