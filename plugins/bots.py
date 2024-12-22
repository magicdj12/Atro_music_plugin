from datetime import datetime
import jdatetime
from pytz import timezone
from pyrogram import filters
from YukkiMusic import app

# نام ماه‌های شمسی و میلادی به فارسی
PERSIAN_SOLAR_MONTHS = [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
]

PERSIAN_GREGORIAN_MONTHS = [
    "ژانویه", "فوریه", "مارس", "آوریل", "مه", "ژوئن",
    "ژوئیه", "اوت", "سپتامبر", "اکتبر", "نوامبر", "دسامبر"
]

# توابع تبدیل تاریخ
def gregorian_to_jalali(date):
    jalali_date = jdatetime.date.fromgregorian(day=date.day, month=date.month, year=date.year)
    day = jalali_date.day
    month = PERSIAN_SOLAR_MONTHS[jalali_date.month - 1]
    year = jalali_date.year
    return f"{day} {month} {year}"

def gregorian_to_persian(date):
    day = date.day
    month = PERSIAN_GREGORIAN_MONTHS[date.month - 1]
    year = date.year
    return f"{day} {month} {year}"

# فیلتر دستورات خاص
valid_commands = ["ساعت", "امروز", "تاریخ"]
exact_command_filter = filters.text & filters.group & (filters.regex(f"^({'|'.join(valid_commands)})$"))

# تابع اصلی
@app.on_message(exact_command_filter)
async def show_datetime(client, message):
    try:
        # تنظیم منطقه زمانی
        iran_tz = timezone("Asia/Tehran")
        afghanistan_tz = timezone("Asia/Kabul")

        # دریافت زمان و تاریخ
        iran_time = datetime.now(iran_tz)
        afghanistan_time = datetime.now(afghanistan_tz)

        jalali_date = gregorian_to_jalali(iran_time)
        gregorian_date = gregorian_to_persian(iran_time)

        iran_formatted_time = iran_time.strftime("%H:%M")
        afghanistan_formatted_time = afghanistan_time.strftime("%H:%M")

        # پاسخ
        text = f"""🌟 اطلاعات ساعت و تاریخ 🌟

🕰 ساعت‌ها:
   🇮🇷 ایران: {iran_formatted_time}
   🇦🇫 افغانستان: {afghanistan_formatted_time}

📅 تاریخ‌ها:
   🌞 شمسی: {jalali_date}
   🌍 میلادی: {gregorian_date}

✨ یک روز فوق‌العاده برای شما! ✨
"""
        await app.send_message(message.chat.id, text)
    except Exception as e:
        print(f"خطا رخ داده: {e}")
        await message.reply("⚠️ مشکلی در دریافت ساعت و تاریخ رخ داده است.")
