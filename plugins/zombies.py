from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from YukkiMusic import app


# لیست کانال‌های جوین اجباری
mandatory_channels = {}  # {channel_id: "نام کانال"}
OWNER_ID = [1924774929]  # شناسه عددی مالک (عدد)

# بررسی عضویت کاربران
@Client.on_message(filters.private & ~filters.command(["start", "add_channel", "remove_channel"]))
async def check_mandatory_join(client, message):
    user_id = message.from_user.id

    # بررسی عضویت در کانال‌ها
    not_joined = []
    for channel_id, channel_name in mandatory_channels.items():
        try:
            member = await client.get_chat_member(channel_id, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append((channel_id, channel_name))
        except Exception:
            not_joined.append((channel_id, channel_name))

    # اگر کاربر عضو همه کانال‌ها نباشد
    if not_joined:
        buttons = [
            [InlineKeyboardButton(f"عضویت در {name}", url=f"https://t.me/{channel_id}")]
            for channel_id, name in not_joined
        ]
        buttons.append([InlineKeyboardButton("تأیید عضویت", callback_data="check_join")])
        reply_markup = InlineKeyboardMarkup(buttons)

        await message.reply(
            "❌ برای استفاده از ربات، ابتدا در کانال‌های زیر عضو شوید:",
            reply_markup=reply_markup,
        )
        return

    # اگر کاربر عضو همه کانال‌ها باشد
    await message.reply("✅ شما عضو همه کانال‌های الزامی هستید! حالا می‌توانید از ربات استفاده کنید.")


# اضافه کردن کانال جدید به لیست جوین اجباری
@Client.on_message(filters.command("add_channel") & filters.user(OWNER_ID))
async def add_channel(client, message):
    if len(message.command) < 3:
        await message.reply("❌ استفاده صحیح: /add_channel <آیدی کانال> <نام کانال>")
        return

    channel_id = message.command[1]
    channel_name = message.command[2]
    mandatory_channels[channel_id] = channel_name

    await message.reply(f"✅ کانال {channel_name} با موفقیت به لیست جوین اجباری اضافه شد.")


# حذف کانال از لیست جوین اجباری
@Client.on_message(filters.command("remove_channel") & filters.user(OWNER_ID))
async def remove_channel(client, message):
    if len(message.command) < 2:
        await message.reply("❌ استفاده صحیح: /remove_channel <آیدی کانال>")
        return

    channel_id = message.command[1]
    if channel_id in mandatory_channels:
        del mandatory_channels[channel_id]
        await message.reply("✅ کانال از لیست جوین اجباری حذف شد.")
    else:
        await message.reply("❌ کانالی با این آیدی در لیست وجود ندارد.")


# بررسی عضویت پس از کلیک روی دکمه "تأیید عضویت"
@Client.on_callback_query(filters.regex("check_join"))
async def handle_join_check(client, callback_query):
    user_id = callback_query.from_user.id

    # بررسی عضویت مجدد
    not_joined = []
    for channel_id, channel_name in mandatory_channels.items():
        try:
            member = await client.get_chat_member(channel_id, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append(channel_name)
        except Exception:
            not_joined.append(channel_name)

    # پیام مناسب بر اساس عضویت
    if not_joined:
        await callback_query.answer(
            f"هنوز در کانال‌های زیر عضو نیستید: {', '.join(not_joined)} 🤨",
            show_alert=True,
        )
    else:
        await callback_query.answer("شما عضو همه کانال‌ها هستید! 😎", show_alert=True)
        await callback_query.message.reply(
            "🎉 حالا می‌توانید از ربات استفاده کنید. امیدوارم خوش بگذره!"
        )
