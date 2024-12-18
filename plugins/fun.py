import random
import asyncio
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from YukkiMusic import app

# ذخیره امتیازات کاربران
player_scores = {}

def update_score(user_id, username, points):
    if user_id not in player_scores:
        player_scores[user_id] = {"username": username, "score": 0}
    player_scores[user_id]["score"] += points

def get_leaderboard():
    sorted_scores = sorted(player_scores.items(), key=lambda x: x[1]["score"], reverse=True)
    leaderboard = "🏆 جدول امتیازات:\n"
    for i, (user_id, data) in enumerate(sorted_scores[:10], start=1):
        leaderboard += f"{i}. {data['username']} - {data['score']} امتیاز\n"
    return leaderboard

# =====================
# بازی ریاضی رقابتی
# =====================
@app.on_message(filters.text & filters.regex(r"^(math|ریاضی)$"))
async def math_game(client, message: Message):
    num1, num2 = random.randint(1, 10), random.randint(1, 10)
    operator = random.choice(["+", "-", "*"])
    correct_answer = eval(f"{num1} {operator} {num2}")
    
    question = f"❓ سؤال ریاضی: {num1} {operator} {num2} = ?"
    await message.reply(question)

    def check_answer(m: Message):
        return m.text.isdigit() and int(m.text) == correct_answer

    try:
        answer = await app.listen(message.chat.id, filters=filters.create(check_answer), timeout=15)
        update_score(answer.from_user.id, answer.from_user.first_name, 10)
        await answer.reply(f"🎉 درست حدس زدی! امتیاز 10 به شما اضافه شد.\n\n{get_leaderboard()}")
    except asyncio.TimeoutError:
        await message.reply(f"⏰ زمان تمام شد! پاسخ درست: {correct_answer}")

# =====================
# بازی معمای تصویری
# =====================
images = [
    {"url": "https://via.placeholder.com/300x300?text=Cat", "answer": "cat"},
    {"url": "https://via.placeholder.com/300x300?text=Dog", "answer": "dog"},
    {"url": "https://via.placeholder.com/300x300?text=Car", "answer": "car"},
]

@app.on_message(filters.text & filters.regex(r"^(image|تصویر)$"))
async def image_game(client, message: Message):
    image = random.choice(images)
    await message.reply_photo(image["url"], caption="🔍 این چیست؟")

    def check_answer(m: Message):
        return m.text.strip().lower() == image["answer"]

    try:
        answer = await app.listen(message.chat.id, filters=filters.create(check_answer), timeout=20)
        update_score(answer.from_user.id, answer.from_user.first_name, 15)
        await answer.reply(f"🎉 درست حدس زدی! امتیاز 15 به شما اضافه شد.\n\n{get_leaderboard()}")
    except asyncio.TimeoutError:
        await message.reply(f"⏰ زمان تمام شد! پاسخ درست: {image['answer']}")

# =====================
# بازی اطلاعات عمومی
# =====================
quiz_questions = [
    {"question": "What is the capital of France?", "answer": "paris"},
    {"question": "Who wrote 'Hamlet'?", "answer": "shakespeare"},
    {"question": "What is the square root of 64?", "answer": "8"},
]

@app.on_message(filters.text & filters.regex(r"^(quiz|سؤال)$"))
async def quiz_game(client, message: Message):
    question = random.choice(quiz_questions)
    await message.reply(f"❓ سؤال اطلاعات عمومی:\n{question['question']}")

    def check_answer(m: Message):
        return m.text.strip().lower() == question["answer"]

    try:
        answer = await app.listen(message.chat.id, filters=filters.create(check_answer), timeout=20)
        update_score(answer.from_user.id, answer.from_user.first_name, 20)
        await answer.reply(f"🎉 درست حدس زدی! امتیاز 20 به شما اضافه شد.\n\n{get_leaderboard()}")
    except asyncio.TimeoutError:
        await message.reply(f"⏰ زمان تمام شد! پاسخ درست: {question['answer']}")

# =====================
# مشاهده جدول امتیازات
# =====================
@app.on_message(filters.text & filters.regex(r"^(leaderboard|جدول)$"))
async def show_leaderboard(client, message: Message):
    leaderboard = get_leaderboard()
    await message.reply(leaderboard)
