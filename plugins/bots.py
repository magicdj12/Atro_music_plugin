import asyncio
from datetime import datetime
import jdatetime  # برای تاریخ شمسی
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

# تابع اصلی برای نمایش ساعت و تاریخ
@app.on_message(filters.command(["time","امروز","تاریخ"],prefixes=["", "/"])) & filters.group
async def show_datetime(client, message):
    try:
        # اطلاعات تاریخ و ساعت
        now = datetime.now()
        jalali_date = gregorian_to_jalali(now)
        gregorian_date = gregorian_to_persian(now)
        current_time = now.strftime("%I:%M %p")  # نمایش ساعت به فرمت 12 ساعته

        # متن خروجی
        text = f"""ساعت و تاریخ:

• ساعت: {current_time}
• تاریخ امروز (شمسی): {jalali_date}
• تاریخ میلادی: {gregorian_date}
"""

        # ارسال پیام
        await app.send_message(message.chat.id, text)
    except Exception as e:
        await asyncio.sleep(1)
        print(f"Error: {e}")
