import asyncio
from datetime import datetime
from convertdate import islamic, jalali
from pyrogram import filters
from YukkiMusic import app

# نام ماه‌های شمسی و قمری
PERSIAN_MONTHS = [
    "فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور",
    "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"
]
ARABIC_MONTHS = [
    "محرم", "صفر", "ربیع الاول", "ربیع الثانی", "جمادی الاولى",
    "جمادی الثانیه", "رجب", "شعبان", "رمضان", "شوال", "ذی القعده", "ذی الحجه"
]

# توابع تبدیل تاریخ
def gregorian_to_jalali(date):
    y, m, d = jalali.from_gregorian(date.year, date.month, date.day)
    return f"{d} {PERSIAN_MONTHS[m-1]} {y}"

def gregorian_to_islamic(date):
    y, m, d = islamic.from_gregorian(date.year, date.month, date.day)
    return f"{d} {ARABIC_MONTHS[m-1]} {y}"

# تابع اصلی برای نمایش ساعت و تاریخ
@app.on_message(filters.command("time") & filters.group)
async def show_datetime(client, message):
    try:
        # اطلاعات تاریخ و ساعت
        now = datetime.now()
        jalali_date = gregorian_to_jalali(now)
        islamic_date = gregorian_to_islamic(now)
        gregorian_date = now.strftime("%A - %Y %d %B")
        current_time = now.strftime("%I:%M %p")  # نمایش ساعت به فرمت 12 ساعته

        # متن خروجی
        text = f"""ساعت و تاریخ:

• ساعت: {current_time}
• تاریخ امروز: {jalali_date}
• تاریخ قمری: {islamic_date}
• تاریخ میلادی: {gregorian_date}
"""

        # ارسال پیام
        await app.send_message(message.chat.id, text)
    except Exception as e:
        await asyncio.sleep(1)
        print(f"Error: {e}")

# اطلاعات ماژول
MODULE = "ساعت و تاریخ"
HELP = """
با این دستور می‌توانید ساعت و تاریخ کنونی را در سه فرمت (شمسی، قمری، میلادی) مشاهده کنید:
دستور:
/datetime
"""
