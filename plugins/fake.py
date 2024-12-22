import requests
from pyrogram import filters
from YukkiMusic import app
from datetime import datetime

# کلید API برای OpenWeatherMap
API_KEY = "fbad98e4e8954e5ea39164949242212"

# تابع برای دریافت اطلاعات آب و هوا
def get_weather(city_name):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_name}&cnt=6&appid={API_KEY}&units=metric&lang=fa"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != "404":
        city = data["city"]["name"]
        country = data["city"]["country"]
        lat = data["city"]["coord"]["lat"]
        lon = data["city"]["coord"]["lon"]

        # اطلاعات طلوع و غروب خورشید
        sun_url = f"http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=fa"
        sun_response = requests.get(sun_url)
        sun_data = sun_response.json()

        sunrise = sun_data["current"]["sunrise"]
        sunset = sun_data["current"]["sunset"]

        sunrise_time = datetime.utcfromtimestamp(sunrise).strftime('%H:%M:%S')
        sunset_time = datetime.utcfromtimestamp(sunset).strftime('%H:%M:%S')

        # گزارش وضعیت آب و هوا
        weather_report = f"🌍 وضعیت آب و هوا برای {city}, {country} 🌍\n\n"

        weather_icons = {
            "clear": "☀️", "clouds": "☁️", "rain": "🌧", "snow": "❄️", 
            "thunderstorm": "⛈", "drizzle": "🌦", "mist": "🌫", "haze": "🌫"
        }

        for day in range(5):
            day_info = data["list"][day]

            date = day_info["dt_txt"]
            temp = day_info["main"]["temp"]
            feels_like = day_info["main"]["feels_like"]
            description = day_info["weather"][0]["description"]
            weather_icon = weather_icons.get(day_info["weather"][0]["main"].lower(), "🌍")
            wind_speed = day_info["wind"]["speed"]
            humidity = day_info["main"]["humidity"]
            pressure = day_info["main"]["pressure"]
            visibility = day_info["visibility"] / 1000  # تبدیل به کیلومتر
            rain = day_info.get("rain", {}).get("3h", 0)
            snow = day_info.get("snow", {}).get("3h", 0)

            weather_report += f"""
📅 {date} {weather_icon}:
   🌡 دما: {temp}°C (احساس دما: {feels_like}°C)
   🌤 وضعیت: {description}
   🌬 سرعت باد: {wind_speed} متر بر ثانیه
   💧 رطوبت: {humidity}%
   🌬 فشار هوا: {pressure} hPa
   🌫 دید افقی: {visibility} کیلومتر
   🌧 بارش باران: {rain} میلی‌متر
   ❄️ بارش برف: {snow} میلی‌متر
   -------------------------
            """

        weather_report += f"""
🌅 زمان طلوع خورشید: {sunrise_time} UTC
🌇 زمان غروب خورشید: {sunset_time} UTC
        """

        return weather_report
    else:
        return "متاسفانه اطلاعاتی برای این شهر یافت نشد. لطفا دوباره تلاش کنید."

# دستور برای نمایش وضعیت آب و هوا
@app.on_message(filters.text & (filters.group | filters.private | filters.channel))
async def weather(_, message):
    try:
        text = message.text.lower()

        # بررسی دستور و دریافت نام شهر
        if "آب و هوای" in text or "هوای" in text:
            parts = text.split(maxsplit=1)

            if len(parts) > 1:
                city_name = parts[1].strip()

                # دریافت اطلاعات وضعیت آب و هوا
                weather_info = get_weather(city_name)

                # ارسال وضعیت آب و هوا به کاربر
                await message.reply_text(weather_info)
            else:
                await message.reply_text("لطفا نام شهری را وارد کنید. مثال: آب و هوای تهران")
    except Exception as e:
        await message.reply_text(f"خطا: {e}")
