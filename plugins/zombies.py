import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv
from os import getenv

# Load .env variables
load_dotenv()

# Importing configuration variables from .env
API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")
OWNER_ID = int(getenv("OWNER_ID", ""))
LOG_GROUP_ID = getenv("LOG_GROUP_ID", "")
SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "")

# Initialize the bot
app = Client("YukkiMusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# List to store the required join channels
required_channels = []

# Command to add a channel to the mandatory join list
@app.on_message(filters.text & filters.user(OWNER_ID) & filters.regex("^جوین اجباری$"))
async def add_join_channel(client, message: Message):
    # Asking for the channel ID or link
    await message.reply("لطفا لینک یا آیدی عددی کانال مورد نظر را ارسال کنید.")

# Handle the channel link/ID after the user sends it
@app.on_message(filters.text & filters.user(OWNER_ID) & filters.regex("^(https?://|[0-9]+)$"))
async def process_join_channel(client, message: Message):
    channel = message.text.strip()
    
    # Check if it's already in the list
    if channel not in required_channels:
        required_channels.append(channel)
        # Create an inline button for the channel
        button = InlineKeyboardButton(f"عضویت در کانال {channel}", url=channel)
        # Create a confirmation button for joining
        confirm_button = InlineKeyboardButton("عضو شدم", callback_data=f"confirm_{channel}")
        
        # Send a confirmation message with the buttons
        keyboard = InlineKeyboardMarkup([[button], [confirm_button]])
        await message.reply(f"کانال {channel} به لیست جوین اجباری اضافه شد.", reply_markup=keyboard)
    else:
        await message.reply("این کانال قبلاً به لیست اضافه شده است.")

# Command to list all mandatory join channels
@app.on_message(filters.text & filters.user(OWNER_ID) & filters.regex("^لیست جوین اجباری$"))
async def list_join_channels(client, message: Message):
    if required_channels:
        await message.reply("\n".join(required_channels))
    else:
        await message.reply("هیچ کانال اجباری برای جوین وجود ندارد.")

# Command to remove a channel from the mandatory join list
@app.on_message(filters.text & filters.user(OWNER_ID) & filters.regex("^حذف جوین اجباری$"))
async def remove_join_channel(client, message: Message):
    # Asking for the channel ID or link to remove
    await message.reply("لطفا لینک یا آیدی عددی کانالی که می‌خواهید حذف کنید را ارسال کنید.")

# Handle the channel link/ID to remove after the user sends it
@app.on_message(filters.text & filters.user(OWNER_ID) & filters.regex("^(https?://|[0-9]+)$"))
async def process_remove_channel(client, message: Message):
    channel = message.text.strip()
    
    # Check if the channel exists in the list
    if channel in required_channels:
        required_channels.remove(channel)
        await message.reply(f"کانال {channel} از لیست جوین اجباری حذف شد.")
    else:
        await message.reply("این کانال در لیست جوین اجباری وجود ندارد.")

# Command to activate join requirement (JoinOn)
@app.on_message(filters.text & filters.user(OWNER_ID) & filters.regex("^جوین فعال$"))
async def join_on(client, message: Message):
    if required_channels:
        await message.reply(f"جوین اجباری فعال شد. کاربران باید به کانال‌های زیر بپیوندند: {', '.join(required_channels)}.")
    else:
        await message.reply("هیچ کانال اجباری برای جوین تنظیم نشده است.")

# Command to deactivate join requirement (JoinOff)
@app.on_message(filters.text & filters.user(OWNER_ID) & filters.regex("^جوین غیرفعال$"))
async def join_off(client, message: Message):
    await message.reply("جوین اجباری غیرفعال شد. کاربران می‌توانند بدون پیوستن به کانال‌ها از ربات استفاده کنند.")

# Command to check if a user is a member of the required channels
@app.on_message(filters.text & filters.regex("^بررسی جوین$"))
async def check_join(client, message: Message):
    user_id = message.from_user.id
    if required_channels:
        for channel in required_channels:
            try:
                member = await client.get_chat_member(channel, user_id)
                if member.status not in ['member', 'administrator', 'creator']:
                    await message.reply(f"برای استفاده از ربات باید به کانال {channel} بپیوندید.")
                    return
            except:
                await message.reply(f"ربات نتواست بررسی کند که شما عضو کانال {channel} هستید.")
                return
        await message.reply("شما عضو تمام کانال‌های اجباری هستید.")
    else:
        await message.reply("هیچ کانال اجباری تنظیم نشده است.")

# Callback query handler to confirm user membership
@app.on_callback_query(filters.regex("^confirm_"))
async def confirm_membership(client, callback_query):
    user_id = callback_query.from_user.id
    channel = callback_query.data.split("_")[1]
    
    try:
        member = await client.get_chat_member(channel, user_id)
        if member.status in ['member', 'administrator', 'creator']:
            await callback_query.answer("عضویت شما تایید شد. هم‌اکنون می‌توانید از ربات استفاده کنید.", show_alert=True)
        else:
            await callback_query.answer("شما هنوز عضو کانال‌های ما نشده‌اید.", show_alert=True)
    except:
        await callback_query.answer("خطا در بررسی عضویت. لطفا دوباره تلاش کنید.", show_alert=True)
