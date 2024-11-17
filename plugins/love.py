import random

from pyrogram import filters

from YukkiMusic import app


def get_random_message(love_percentage):
    if love_percentage <= 30:
        return random.choice(
            [
                "عشق در هوا موج می‌زند اما به کمی جرقه نیاز دارد.",
                "شروع خوبی است اما جای پیشرفت دارد.",
                "این فقط آغاز چیزی زیباست.",

            ]
        )
    elif love_percentage <= 70:
        return random.choice(
            [
                "یک ارتباط قوی وجود دارد. به پرورشش ادامه دهید.",
                "شانس خوبی دارید. روی آن کار کنید.",
                "عشق در حال شکوفایی است، ادامه دهید."

            ]
        )
    else:
        return random.choice(
            [
            "وای! این یک پیوند آسمانی است!",
            "جفتی کامل! این رابطه را گرامی بدارید.",
            "سرنوشت شما با هم بودن است. تبریک می‌گویم!"
            ]
        )


@app.on_message(filters.command(["love","عشق","علاقه","دوست"],prefixes=['','/']))
def love_command(client, message):
    command, *args = message.text.split(" ")
    if len(args) >= 2:
        name1 = args[0].strip()
        name2 = args[1].strip()

        love_percentage = random.randint(10, 100)
        love_message = get_random_message(love_percentage)

        response = f"{name1}💕 + {name2}💕 = {love_percentage}%\n\n{love_message}"
    else:
        response = "لطفا دو نام را انتخاب کنید /عشق دستور."
    app.send_message(message.chat.id, response)


__MODULE__ = "عشق"
__HELP__ = """
**ماشین حساب عشق:**

• `/love [نام1] [نام2]`: درصد عشق بین دو نفر را محاسبه می‌کند.
• `/عشق [نام1] [نام2]`: درصد عشق بین دو نفر را محاسبه می‌کند.
"""
