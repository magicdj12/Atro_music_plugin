import random
from pyrogram import filters
from YukkiMusic import app

# تعریف تابع برای فرمان "love"
@app.on_message(filters.command(["love", "کراش", "عشق"], prefixes=["", "/"]))
async def love_command(client, message):  # افزودن async برای پشتیبانی از همزمانی
    args = message.text.split()[1:]  # حذف دستور و دریافت نام‌ها
    if len(args) >= 2:
        name1 = args[0].strip()
        name2 = args[1].strip()

        love_percentage = random.randint(10, 100)  # استفاده از random برای تولید عدد تصادفی
        love_message = get_random_message(love_percentage)

        # طراحی پاسخ
        response = f"""
💖  {name1} 💕 {name2} 💖
📖 عشق شما: {love_percentage}%

📝 {love_message}
"""
    else:
        response = "لطفاً بعد از دستور /love دو نام وارد کنید."

    await client.send_message(chat_id=message.chat.id, text=response)  # استفاده از await

def get_random_message(love_percentage):
    if love_percentage <= 30:
        return random.choice(
            [
                "عشق در هوای شما موج می‌زند، اما هنوز نیاز به جرقه‌ای دارد.",
                "شروع خوبی است، اما راه زیادی برای رشد دارید.",
                "این تازه آغاز یک داستان زیباست.",
            ]
        )
    elif love_percentage <= 70:
        return random.choice(
            [
                "اتصال قوی‌ای بین شما وجود دارد. آن را پرورش دهید.",
                "شانس خوبی دارید، روی آن کار کنید.",
                "عشق میان شما در حال شکوفه زدن است، ادامه دهید.",
            ]
        )
    else:
        return random.choice(
            [
                "وای! این یک پیوند آسمانی است!",
                "عشق کامل! این پیوند را گرامی بدارید.",
                "سرنوشت شما را برای هم ساخته است. تبریک می‌گویم!",
            ]
        )
