import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
from os import getenv

# بارگذاری متغیرهای .env
load_dotenv()

# متغیرهای پیکربندی از فایل .env
API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
OWNER_ID = int(getenv("OWNER_ID", ""))
LOG_GROUP_ID = getenv("LOG_GROUP_ID", "")
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "")

# ابتدای ساخت ربات
app = Client("YukkiMusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# لیست کانال‌های جوین اجباری
required_channels = []

# حالت جوین اجباری
join_active = False

# دستور برای اضافه کردن کانال به لیست جوین اجباری
@app.on_message(filters.text & filters.user(OWNER_ID) & filters.regex("^جوین اجباری$"))
async def add_join_channel(client, message: Message):
    await message.reply("لطفا لینک یا آیدی عددی کانال مورد نظر را ارسال کنید.")

# پردازش لینک یا آیدی کانال که توسط صاحب ربات ارسال می‌شود
@app.on_message(filters.text & filters.user(OWNER_ID) & filters.regex("^(https?://|[0-9]+)$"))
async def process_join_channel(client, message: Message):
    channel = message.text.strip()
    
    # بررسی اگر کانال قبلاً اضافه نشده باشد
    if channel not in required_channels:
        required_channels.append(channel)
        # ساخت دکمه لینک به کانال
        button = InlineKeyboardButton(f"عضویت در کانال {channel}", url=channel)
        # دکمه تایید عضویت
        confirm_button = InlineKeyboardButton("عضو شدم", callback_data=f"confirm_{channel}")
        
        # ارسال پیام تایید با دکمه‌ها
        keyboard = InlineKeyboardMarkup([[button], [confirm_button]])
        await message.reply(f"کانال {channel} به لیست جوین اجباری اضافه شد.", reply_markup=keyboard)
    else:
        await message.reply("این کانال قبلاً به لیست اضافه شده است.")

# دستور برای حذف کانال از لیست جوین اجباری
@app.on_message(filters.text & filters.user(OWNER_ID) & filters.regex("^حذف جوین اجباری$"))
async def remove_join_channel(client, message: Message):
    await message.reply("لطفا لینک یا آیدی عددی کانال مورد نظر که می‌خواهید حذف کنید را ارسال کنید.")

# پردازش حذف کانال از لیست جوین اجباری
@app.on_message(filters.text & filters.user(OWNER_ID) & filters.regex("^(https?://|[0-9]+)$"))
async def process_remove_channel(client, message: Message):
    channel = message.text.strip()
    
    if channel in required_channels:
        required_channels.remove(channel)
        await message.reply(f"کانال {channel} از لیست جوین اجباری حذف شد.")
    else:
        await message.reply("این کانال در لیست جوین اجباری وجود ندارد.")

# دستور برای نمایش لیست کانال‌های جوین اجباری
@app.on_message(filters.text & filters.user(OWNER_ID) & filters.regex("^لیست جوین اجباری$"))
async def list_join_channels(client, message: Message):
    if required_channels:
        channels_list = "\n".join(required_channels)
        await message.reply(f"کانال‌های جوین اجباری:\n{channels_list}")
    else:
        await message.reply("هیچ کانال جوین اجباری ثبت نشده است.")

# دستور برای فعال کردن جوین اجباری
@app.on_message(filters.text & filters.user(OWNER_ID) & filters.regex("^جوین فعال$"))
async def enable_join(client, message: Message):
    global join_active
    join_active = True
    await message.reply("حالت جوین اجباری فعال شد. کاربران باید عضو کانال‌های اجباری شوند تا از ربات استفاده کنند.")

# دستور برای غیرفعال کردن جوین اجباری
@app.on_message(filters.text & filters.user(OWNER_ID) & filters.regex("^جوین غیرفعال$"))
async def disable_join(client, message: Message):
    global join_active
    join_active = False
    await message.reply("حالت جوین اجباری غیرفعال شد. کاربران می‌توانند بدون عضویت در کانال‌ها از ربات استفاده کنند.")

# دستور برای بررسی عضویت کاربر در کانال‌های جوین اجباری
@app.on_message(filters.text & filters.regex("عضو شدم"))
async def check_join_status(client, message: Message):
    if join_active:
        user_id = message.from_user.id
        joined_channels = []
        
        for channel in required_channels:
            try:
                # بررسی عضویت کاربر در هر کانال
                chat_member = await client.get_chat_member(channel, user_id)
                if chat_member.status in ['member', 'administrator']:
                    joined_channels.append(channel)
            except:
                continue

        # بررسی نتیجه
        if len(joined_channels) == len(required_channels):
            await message.reply("عضویت شما تایید شد. هم اکنون می‌توانید از ربات استفاده کنید.")
        else:
            await message.reply("شما هنوز عضو کانال‌های اجباری نشده‌اید.")
  
