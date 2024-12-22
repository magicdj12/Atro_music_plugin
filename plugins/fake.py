# import requests
# from pyrogram import Client, filters
# from datetime import datetime
# import logging

# # تنظیمات لاگ برای اشکال زدایی
# logging.basicConfig(level=logging.DEBUG)

# # توکن API برای OpenWeatherMap
# API_KEY = "d4a358f84c4bb3b49d8132a49be0fc20"  # توکن خود را اینجا وارد کنید

# # ساخت اپلیکیشن Pyrogram
# app = Client("weather_bot")

# # تابع برای دریافت اطلاعات وضعیت آب و هوا
# def get_weather(city_name):
#     url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&cnt=6&appid={API_KEY}&units=metric&lang=fa"
#     response = requests.get(url)
#     data = response.json()

#     # بررسی اینکه داده‌ها دریافت شده‌اند یا خیر
#     if data["cod"] != "404":
#         city = data["city"]["name"]
#         country = data["city"]["country"]
#         lat = data["city"]["coord"]["lat"]
#         lon = data["city"]["coord"]["lon"]

#         # درخواست وضعیت خورشید
#         sun_url = f"http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=fa"
#         sun_response = requests.get(sun_url)
#         sun_data = sun_response.json()

#         sunrise = sun_data["current"]["sunrise"]
#         sunset = sun_data["current"]["sunset"]

#         # تبدیل زمان از UNIX به فرمت قابل خواندن
#         sunrise_time = datetime.utcfromtimestamp(sunrise).strftime('%H:%M:%S')
#         sunset_time = datetime.utcfromtimestamp(sunset).strftime('%H:%M:%S')

#         # شروع گزارش وضعیت آب و هوا
#         weather_report = f"🌍 وضعیت آب و هوا برای {city}, {country} 🌍\n\n"

#         # آیکون‌های وضعیت آب و هوا
#         weather_icons = {
#             "clear": "☀️", "clouds": "☁️", "rain": "🌧", "snow": "❄️", 
#             "thunderstorm": "⛈", "drizzle": "🌦", "mist": "🌫", "haze": "🌫"
#         }

#         # اطلاعات وضعیت آب و هوا برای 5 روز آینده
#         for day in range(5):
#             day_info = data["list"][day]

#             date = day_info["dt_txt"]
#             temp = day_info["main"]["temp"]
#             feels_like = day_info["main"]["feels_like"]
#             description = day_info["weather"][0]["description"]
#             weather_icon = weather_icons.get(day_info["weather"][0]["main"].lower(), "🌍")
#             wind_speed = day_info["wind"]["speed"]
#             humidity = day_info["main"]["humidity"]
#             pressure = day_info["main"]["pressure"]
#             visibility = day_info["visibility"] / 1000  # تبدیل به کیلومتر
#             rain = day_info.get("rain", {}).get("3h", 0)
#             snow = day_info.get("snow", {}).get("3h", 0)

#             # اضافه کردن اطلاعات هر روز به گزارش
#             weather_report += f"""
# 📅 {date} {weather_icon}:
#    🌡 دما: {temp}°C (احساس دما: {feels_like}°C)
#    🌤 وضعیت: {description}
#    🌬 سرعت باد: {wind_speed} متر بر ثانیه
#    💧 رطوبت: {humidity}%
#    🌬 فشار هوا: {pressure} hPa
#    🌫 دید افقی: {visibility} کیلومتر
#    🌧 بارش باران: {rain} میلی‌متر
#    ❄️ بارش برف: {snow} میلی‌متر
#    -------------------------
#             """

#         # اضافه کردن وضعیت خورشید
#         weather_report += f"""
# 🌅 زمان طلوع خورشید: {sunrise_time} UTC
# 🌇 زمان غروب خورشید: {sunset_time} UTC
#         """

#         return weather_report
#     else:
#         return "متاسفانه اطلاعاتی برای این شهر یافت نشد. لطفا دوباره تلاش کنید."


# # دستور برای دریافت وضعیت آب و هوا
# @app.on_message(filters.text & filters.regex(r"^(آب و هوای|هوای)\s+([^\s]+)"))
# async def weather(_, message):
#     try:
#         # دریافت نام شهر از پیام کاربر
#         city_name = message.text.split(maxsplit=1)[1].strip()
#         logging.debug(f"City Name: {city_name}")  # لاگ نام شهر وارد شده

#         # دریافت اطلاعات وضعیت آب و هوا
#         weather_info = get_weather(city_name)
#         logging.debug(f"Weather Info: {weather_info}")  # لاگ وضعیت آب و هوا

#         # ارسال پاسخ به کاربر
#         await message.reply_text(weather_info)

#     except IndexError:
#         logging.error("Error: No city provided")  # لاگ خطا در صورت عدم ارسال نام شهر
#         await message.reply_text("لطفا نام شهری را وارد کنید. مثال: آب و هوای تهران")
#     except Exception as e:
#         logging.error(f"Unexpected error: {e}")  # لاگ خطاهای غیرمنتظره
#         await message.reply_text(f"خطا: {e}")
