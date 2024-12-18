import random
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from YukkiMusic import app

# ذخیره امتیازات کاربران
player_scores = {}

def update_score(user_id, username, points):
    if user_id not in player_scores:
        player_scores[user_id] = {"username": username, "score": 0}
    player_scores[user_id]["username"] = username
    player_scores[user_id]["score"] += points

    if player_scores[user_id]["score"] < 0:
        player_scores[user_id]["score"] = 0

def get_leaderboard():
    sorted_scores = sorted(player_scores.items(), key=lambda x: x[1]["score"], reverse=True)
    leaderboard = "🏆 جدول امتیازات:\n"
    for i, (user_id, data) in enumerate(sorted_scores[:10], start=1):
        leaderboard += f"{i}. {data['username']} - {data['score']} امتیاز\n"
    return leaderboard

funny_responses = [
    "😅 نزدیک بود، ولی اشتباهه!",
    "😂 اشتباه گفتی، بهتره بیشتر مطالعه کنی!",
    "🤣 جواب غلط بود، ولی اشکالی نداره دفعه بعد بهتر تلاش کن!"
]

# =====================
# بازی اطلاعات عمومی (فارسی - ایران و افغانستان)
# =====================
quiz_questions = [
    {"question": "پایتخت افغانستان کدام شهر است؟", "answer": "کابل"},
    {"question": "رود معروفی که از افغانستان و تاجیکستان عبور می‌کند چیست؟", "answer": "آمودریا"},
    {"question": "پایتخت ایران کدام شهر است؟", "answer": "تهران"},
    {"question": "بلندترین قله ایران چه نام دارد؟", "answer": "دماوند"},
    {"question": "زبان رسمی افغانستان چیست؟", "answer": "دری"},
    {"question": "نویسنده کتاب بوف کور چه کسی است؟", "answer": "صادق هدایت"},
    {"question": "میدان آزادی در کدام شهر ایران قرار دارد؟", "answer": "تهران"},
    {"question": "مسجد کبود در کدام شهر ایران واقع شده است؟", "answer": "تبریز"},
    {"question": "بزرگ‌ترین دریاچه افغانستان کدام است؟", "answer": "دریاچه بند امیر"},
    {"question": "نخستین شاعر فارسی‌گوی افغانستان چه کسی است؟", "answer": "رودکی"},
]

@app.on_message(filters.text & filters.regex(r"^(quiz|سؤال)$"))
async def quiz_game(client, message: Message):
    question = random.choice(quiz_questions)
    await message.reply(f"❓ سؤال اطلاعات عمومی:\n{question['question']}")

    def check_answer(m: Message):
        return m.text.strip()

    try:
        answer = await app.listen(message.chat.id, filters=filters.create(check_answer), timeout=20)
        user_answer = answer.text.strip()

        if user_answer == question["answer"]:
            update_score(answer.from_user.id, answer.from_user.first_name, 20)
            await answer.reply(f"🎉 درست حدس زدی! امتیاز 20 به شما اضافه شد.\n\n{get_leaderboard()}")
        else:
            if player_scores.get(answer.from_user.id, {"score": 0})["score"] > 0:
                update_score(answer.from_user.id, answer.from_user.first_name, -10)
                await answer.reply(
                    f"❌ اشتباه بود! جواب درست: {question['answer']}.\n"
                    f"10 امتیاز از شما کم شد.\n\n{random.choice(funny_responses)}\n\n{get_leaderboard()}"
                )
            else:
                await answer.reply(
                    f"❌ اشتباه بود! جواب درست: {question['answer']}.\n{random.choice(funny_responses)}"
                )

    except asyncio.TimeoutError:
        await message.reply(f"⏰ زمان تمام شد! پاسخ درست: {question['answer']}")

# =====================
# مشاهده جدول امتیازات
# =====================
@app.on_message(filters.text & filters.regex(r"^(leaderboard|جدول)$"))
async def show_leaderboard(client, message: Message):
    leaderboard = get_leaderboard()
    await message.reply(leaderboard)
