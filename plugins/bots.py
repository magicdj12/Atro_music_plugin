import asyncio
from datetime import datetime
import jdatetime  # برای تاریخ شمسی
from pytz import timezone  # برای تنظیم منطقه زمانی
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

# ترکیب فیلترها
combined_filters = filters.command(["time", "امروز", "تاریخ"], prefixes=["", "/"]) & filters.group

# تابع اصلی برای نمایش ساعت و تاریخ
@app.on_message(combined_filters)
async def show_datetime(client, message):
    try:
        # تنظیم منطقه زمانی
        iran_tz = timezone("Asia/Tehran")
        afghanistan_tz = timezone("Asia/Kabul")

        # ساعت و تاریخ در هر منطقه
        iran_time = datetime.now(iran_tz)
        afghanistan_time = datetime.now(afghanistan_tz)

        # تبدیل تاریخ و زمان
        jalali_date = gregorian_to_jalali(iran_time)
        gregorian_date = gregorian_to_persian(iran_time)

        # قالب‌بندی زمان‌ها
        iran_formatted_time = iran_time.strftime("%I:%M %p")
        afghanistan_formatted_time = afghanistan_time.strftime("%I:%M %p")

        # متن خروجی
        text = f"""ساعت و تاریخ:

• ساعت ایران: {iran_formatted_time}
• ساعت افغانستان: {afghanistan_formatted_time}
• تاریخ امروز (شمسی): {jalali_date}
• تاریخ میلادی: {gregorian_date}
"""

        # ارسال پیام
        await app.send_message(message.chat.id, text)
    except Exception as e:
        await asyncio.sleep(1)
        print(f"Error: {e}")
