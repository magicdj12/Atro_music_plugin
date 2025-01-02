import random
import time

import requests
from pyrogram import filters
from pyrogram.enums import ChatAction, PollType
from YukkiMusic import app


last_command_time = {}


@app.on_message(filters.command(["quiz"]))
async def quiz(client, message):
    user_id = message.from_user.id
    current_time = time.time()

    if user_id in last_command_time and current_time - last_command_time[user_id] < 5:
        await message.reply_text(
            "Pʟᴇᴀsᴇ ᴡᴀɪᴛ 𝟻 sᴇᴄᴏɴᴅs ʙᴇғᴏʀᴇ ᴜsɪɴɢ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴀɢᴀɪɴ."
        )
        return

    last_command_time[user_id] = current_time

    categories = [9, 17, 18, 20, 21, 27]
    await app.send_chat_action(message.chat.id, ChatAction.TYPING)

    url = f"https://opentdb.com/api.php?amount=1&category={random.choice(categories)}&type=multiple"
    response = requests.get(url).json()

    question_data = response["results"][0]
    question = question_data["question"]
    correct_answer = question_data["correct_answer"]
    incorrect_answers = question_data["incorrect_answers"]

    all_answers = incorrect_answers + [correct_answer]
    random.shuffle(all_answers)

    cid = all_answers.index(correct_answer)
    await app.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=all_answers,
        is_anonymous=False,
        type=PollType.QUIZ,
        correct_option_id=cid,
    )


__MODULE__ = "ربات اختصاصی◉"
__HELP__ = """

◉قوانین خرید اختصاصی

1-اولین قانون برای دریافت نمایندگی تیم رنجر سابقه کاری هست.

2-دومین قانون برای دریافت اختصاصی ارسال احراز هویت است 

3-سومین قانون برای دریافت نمایندگی احترام به مشتری های اختصاصی أترو هست.(یعنی فرد دیگه ای که نمایندگی داره احترام بزارید چون هر دو از یک تیم ربات دارید درصورت دعوا دوتا ربات آف میشود)

📌 3 تا مهم ترین قوانین دریافت نمایندگی أترو رو باید بپذیرید تا بتونید ربات اختصاصی برای شما ساخته بشود.

برای اطلاعات بیشتر و دریافت نمایندگی آیدی زیر مراجعه کنید.🔻

⛥ @BEBlNN

 ┈┅━┃𝙍𝘼𝙉𝙂𝙀𝙍┃━┅┈ ‌‌

"""
