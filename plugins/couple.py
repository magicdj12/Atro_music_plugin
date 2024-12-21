
# import os
# import random
# import requests
# from PIL import Image, ImageDraw, ImageFont
# from pyrogram import filters
# from pyrogram.enums import ChatType, ChatMembersFilter
# from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from YukkiMusic import app

# # لیست اشعار عاشقانه
# LOVE_QUOTES = [
#     "عشق همین است، در نگاه تو گم شدن...",
#     "تو تمام دلیل زندگی منی...",
#     "با تو تمام جهان زیباست...",
#     "هر لحظه که با توام، زندگی عاشقانه‌تر است...",
#     "در نگاهت هزار راز عشق نهفته است..."
# ]

# # تصویر پیش‌فرض
# DEFAULT_IMAGE_URL = "https://telegra.ph/file/05aa686cf52fc666184bf.jpg"
# DEFAULT_IMAGE_PATH = "default_pfp.png"

# def download_default_image():
#     if not os.path.exists(DEFAULT_IMAGE_PATH):
#         response = requests.get(DEFAULT_IMAGE_URL)
#         if response.status_code == 200:
#             with open(DEFAULT_IMAGE_PATH, "wb") as f:
#                 f.write(response.content)

# # برش دایره‌ای عکس
# def circle_crop(image_path):
#     img = Image.open(image_path).resize((256, 256))
#     mask = Image.new("L", img.size, 0)
#     draw = ImageDraw.Draw(mask)
#     draw.ellipse((0, 0) + img.size, fill=255)
#     img.putalpha(mask)
#     return img

# # دستورات اصلی
# @app.on_message(filters.command("زوج"))
# async def select_couple(_, message):
#     chat_id = message.chat.id
#     if message.chat.type == ChatType.PRIVATE:
#         return await message.reply_text("این دستور فقط در گروه‌ها کار می‌کند.")

#     # حالت انتخابی
#     args = message.text.split()
#     if len(args) > 1:
#         try:
#             user1 = await app.get_users(args[1])
#             user2 = await app.get_users(args[2])
#         except Exception:
#             return await message.reply_text("لطفاً آی‌دی یا یوزرنیم معتبر وارد کنید.")
#         c1, c2 = user1.id, user2.id
#     else:  # حالت تصادفی
#         members = [
#             m.user
#             async for m in app.get_chat_members(chat_id, filter=ChatMembersFilter.RECENT)
#             if not m.user.is_bot
#         ]
#         if len(members) < 2:
#             return await message.reply_text("اعضای کافی برای انتخاب وجود ندارد.")
#         random.shuffle(members)
#         c1, c2 = members[0].id, members[1].id

#     # دریافت عکس و نام‌ها
#     user1 = await app.get_users(c1)
#     user2 = await app.get_users(c2)
#     name1, name2 = user1.first_name, user2.first_name

#     download_default_image()

#     p1_path = "pfp1.png"
#     p2_path = "pfp2.png"
#     try:
#         p1 = await app.download_media(user1.photo.big_file_id, p1_path) if user1.photo else DEFAULT_IMAGE_PATH
#         p2 = await app.download_media(user2.photo.big_file_id, p2_path) if user2.photo else DEFAULT_IMAGE_PATH
#     except:
#         p1, p2 = DEFAULT_IMAGE_PATH, DEFAULT_IMAGE_PATH

#     # تنظیم عکس‌ها
#     background = Image.new("RGB", (1024, 512), "black")
#     draw = ImageDraw.Draw(background)

#     img1 = circle_crop(p1)
#     img2 = circle_crop(p2)

#     background.paste(img1, (128, 128), img1)
#     background.paste(img2, (640, 128), img2)

#     # اضافه کردن نام‌ها
#     font = ImageFont.truetype("arial.ttf", 40)
#     draw.text((128, 400), name1, fill="white", font=font)
#     draw.text((640, 400), name2, fill="white", font=font)

#     # افزودن شعر
#     quote = random.choice(LOVE_QUOTES)
#     draw.text((256, 450), quote, fill="white", font=font)

#     # ذخیره و ارسال
#     result_path = "couple_result.png"
#     background.save(result_path)

#     # دکمه شیشه‌ای
#     keyboard = InlineKeyboardMarkup(
#         [[InlineKeyboardButton("منو ببر گروهت", callback_data="show_groups")]]
#     )

#     await message.reply_photo(
#         result_path, 
#         caption=f"{name1} ❤️ {name2}\n{quote}", 
#         reply_markup=keyboard
#     )

#     # پاک کردن فایل‌ها
#     for path in [p1_path, p2_path, result_path]:
#         if os.path.exists(path):
#             os.remove(path)

# # هندلر برای نمایش گروه‌ها
# @app.on_callback_query(filters.regex("show_groups"))
# async def show_user_groups(client, callback_query):
#     user_id = callback_query.from_user.id
#     groups = [
#         chat async for chat in client.get_dialogs()
#         if chat.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP]
#         and chat.chat.member_count
#         and user_id in [m.user.id async for m in client.get_chat_members(chat.chat.id)]
#     ]
#     if groups:
#         group_names = "\n".join([chat.chat.title for chat in groups])
#         await callback_query.message.reply_text(f"📋 لیست گروه‌های شما:\n\n{group_names}")
#     else:
#         await callback_query.message.reply_text("❌ شما در هیچ گروهی عضو نیستید.")
