from pyrogram import filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from YukkiMusic import app  
# کانال‌های اجباری و وضعیت جوین اجباری
REQUIRED_CHANNELS = []
JOIN_MANDATORY = False

# مدیریت کانال‌های اجباری
@app.on_message(filters.user(SUDOERS) & filters.command(["جوین_اجباری", "لیست_جوین", "حذف_جوین", "جوین_روشن", "جوین_خاموش"]))
async def manage_join(client, message):
    global REQUIRED_CHANNELS, JOIN_MANDATORY
    command = message.command

    if command[0] == "جوین_اجباری":
        await message.reply("لطفاً لینک یا آیدی عددی کانال را ارسال کنید.")
        return

    elif command[0] == "لیست_جوین":
        if REQUIRED_CHANNELS:
            channels_list = "\n".join(REQUIRED_CHANNELS)
            await message.reply(f"کانال‌های اجباری:\n{channels_list}")
        else:
            await message.reply("هیچ کانالی در لیست جوین اجباری وجود ندارد.")

    elif command[0] == "حذف_جوین":
        await message.reply("لطفاً لینک یا آیدی کانال موردنظر برای حذف را ارسال کنید.")
        return

    elif command[0] == "جوین_روشن":
        JOIN_MANDATORY = True
        await message.reply("جوین اجباری فعال شد.")

    elif command[0] == "جوین_خاموش":
        JOIN_MANDATORY = False
        await message.reply("جوین اجباری غیرفعال شد.")

# بررسی پیام و عضویت کاربر در کانال‌های اجباری
@app.on_message(filters.private)
async def check_mandatory_join(client, message):
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
            "لطفاً ابتدا در کانال‌های زیر عضو شوید:",
            reply_markup=reply_markup
        )
        return

# دکمه "عضو شدم"
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


# حذف کاربران غیرفعال (زامبی‌ها)
@app.on_message(filters.command("پاکسازی_زامبی‌ها") & filters.user(SUDOERS))
async def remove_zombies(_, message: Message):
    chat_id = message.chat.id

    total_kicked = 0
    async for member in app.get_chat_members(chat_id):
        user = member.user
        if user.is_deleted:
            try:
                await app.kick_chat_member(chat_id, user.id)
                total_kicked += 1
            except Exception as e:
                print(f"خطا در حذف کاربر: {e}")

    if total_kicked > 0:
        await message.reply(f"{total_kicked} کاربر غیرفعال از گروه پاک شدند.")
    else:
        await message.reply("هیچ کاربر غیرفعالی یافت نشد.")
