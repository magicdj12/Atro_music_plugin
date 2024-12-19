from YukkiMusic import app
from pyrogram import Client, filters
from pyrogram.types import Message

# ذخیره‌سازی کانال‌های اجباری و وضعیت جوین
forced_channels = []
join_required = False
ADMIN_ID = [1924774929]

@app.on_message(filters.command("add_join") & filters.user(ADMIN_ID))
async def add_join_channel(client: Client, message: Message):
    await message.reply("لینک یا آیدی عددی کانال مورد نظر را ارسال کنید:")
    reply = await client.listen(message.chat.id)  # دریافت پاسخ کاربر
    channel_id = reply.text.strip()

    if channel_id not in forced_channels:
        forced_channels.append(channel_id)
        await message.reply(f"کانال {channel_id} به لیست جوین اجباری اضافه شد.")
    else:
        await message.reply("این کانال قبلاً در لیست وجود دارد!")


@app.on_message(filters.command("list_join") & filters.user(ADMIN_ID))
async def list_join_channels(client: Client, message: Message):
    if forced_channels:
        channels = "\n".join(forced_channels)
        await message.reply(f"لیست کانال‌های جوین اجباری:\n{channels}")
    else:
        await message.reply("هیچ کانالی در لیست جوین اجباری وجود ندارد.")


@app.on_message(filters.command("remove_join") & filters.user(ADMIN_ID))
async def remove_join_channel(client: Client, message: Message):
    await message.reply("لینک یا آیدی عددی کانالی که می‌خواهید حذف کنید را ارسال کنید:")
    reply = await client.listen(message.chat.id)  # دریافت پاسخ کاربر
    channel_id = reply.text.strip()

    if channel_id in forced_channels:
        forced_channels.remove(channel_id)
        await message.reply(f"کانال {channel_id} از لیست جوین اجباری حذف شد.")
    else:
        await message.reply("این کانال در لیست جوین اجباری یافت نشد!")


@app.on_message(filters.command("join_on") & filters.user(ADMIN_ID))
async def enable_join(client: Client, message: Message):
    global join_required
    join_required = True
    await message.reply("جوین اجباری فعال شد. کاربران باید عضو کانال‌های مشخص‌شده شوند.")


@app.on_message(filters.command("join_off") & filters.user(ADMIN_ID))
async def disable_join(client: Client, message: Message):
    global join_required
    join_required = False
    await message.reply("جوین اجباری غیرفعال شد. نیازی به عضویت کاربران نیست.")


@app.on_message(filters.private, group=-1)
async def check_user_join(client: Client, message: Message):
    if join_required and forced_channels:
        for channel in forced_channels:
            try:
                await client.get_chat_member(channel, message.from_user.id)
            except:
                await message.reply(
                    f"برای استفاده از ربات، ابتدا عضو کانال زیر شوید:\n{channel}"
                )
                return
