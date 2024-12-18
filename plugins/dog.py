import requests
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto

# کلید API شما
access_key = "LMwYOz3wWqUxxo6picGIKg8VxpA4HJp1rUg2bPNWBc7V7pV6FgqoGh5z"

# کیبورد برای "بعدی" و "بستن"
girl_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(text="بعدی", callback_data="next_girl")],
        [InlineKeyboardButton(text="بستن", callback_data="close")],
    ]
)

app = Client("my_bot")

# دستور "/پروف دختر" برای ارسال عکس دخترانه
@app.on_message(filters.command(["پروف دختر"]))
async def girl_profile(c, m: Message):
    url = f"https://api.unsplash.com/photos/random?query=girl&client_id={access_key}"
    response = requests.get(url)
    data = response.json()

    if data:
        girl_url = data[0]["urls"]["regular"]  # گرفتن لینک عکس
        await m.reply_photo(girl_url, reply_markup=girl_keyboard)
    else:
        await m.reply_text("عکس پیدا نشد، لطفاً دوباره تلاش کنید.")

# تابع برای بارگذاری عکس بعدی
@app.on_callback_query(filters.regex("next_girl"))
async def next_girl(c, m: Message):
    url = f"https://api.unsplash.com/photos/random?query=girl&client_id={access_key}"
    response = requests.get(url)
    data = response.json()

    if data:
        girl_url = data[0]["urls"]["regular"]
        await m.edit_message_media(
            InputMediaPhoto(media=girl_url),
            reply_markup=girl_keyboard,
        )
    else:
        await m.edit_message_text("عکس پیدا نشد، لطفاً دوباره تلاش کنید.")

# تابع برای بستن
@app.on_callback_query(filters.regex("close"))
async def close(c, m: Message):
    await m.edit_message_text("ربات متوقف شد.")
