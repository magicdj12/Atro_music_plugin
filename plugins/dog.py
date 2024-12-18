import random
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message,
)
from YukkiMusic import app

# لیست لینک‌های عکس‌های دخترانه شاخ و شیک
girl_photos = [
    "https://images.unsplash.com/photo-1606852912494-00ec98c8f8f5",  # عکسی از یک دختر شیک
    "https://images.unsplash.com/photo-1592141272825-4f4054c76f17",  # عکسی از یک دختر با استایل خاص
    "https://images.unsplash.com/photo-1562772220-f63a1023a3d1",  # عکسی از یک دختر مدرن
    "https://images.unsplash.com/photo-1621946959861-ff86f72f70c7",  # عکسی از یک دختر زیبا
    "https://images.unsplash.com/photo-1637007300865-bbaf62a5155f",  # عکسی از یک دختر با سبک جذاب
    "https://images.unsplash.com/photo-1592119075364-6d1db2721ff5",  # عکسی از یک دختر جذاب و شیک
    "https://images.unsplash.com/photo-1615779020497-f3fd86c5d2d9",  # عکسی از یک دختر با استایل خاص
    "https://images.unsplash.com/photo-1571949811847-5f944302d10b",  # عکسی از یک دختر شیک و جذاب
    "https://images.unsplash.com/photo-1603333387913-8b68585f0ba4",  # عکسی از یک دختر شیک در خیابان
    "https://images.unsplash.com/photo-1605751267417-9a6e82b6b441",  # عکسی از یک دختر مدرن و با استایل
    "https://images.unsplash.com/photo-1572867711153-c255a24e7b42",  # عکس یک دختر با استایل خاص
    "https://images.unsplash.com/photo-1644927022901-c6c6d68cb01f",  # عکسی از یک دختر با استایل مدرن
    "https://images.unsplash.com/photo-1606464764431-3ed0e660a5d5",  # عکسی از یک دختر خوش‌تیپ
    "https://images.unsplash.com/photo-1581561275366-e23c6dcd1703",  # عکسی از یک دختر شیک در فضای باز
    "https://images.unsplash.com/photo-1616558035477-544b4f9de3b1",  # عکسی از یک دختر خوش‌لباس و شیک
    "https://images.unsplash.com/photo-1597657494662-65b348c3f8fa",  # عکسی از یک دختر شیک و خاص
    "https://images.unsplash.com/photo-1607600387782-90b688de93b2",  # عکسی از یک دختر در خیابان
    "https://images.unsplash.com/photo-1615786310331-70c8ff70de1a",  # عکسی از یک دختر با آرایش شیک
    "https://images.unsplash.com/photo-1600457636401-e232c0f409d3",  # عکسی از یک دختر شیک با استایل جذاب
    "https://images.unsplash.com/photo-1585421074931-bd0bb0c6ed56",  # عکسی از یک دختر شیک و شاد
    "https://images.unsplash.com/photo-1609984543193-8fe8e73b4387",  # عکسی از یک دختر مدرن و خاص
    "https://images.unsplash.com/photo-1606211849390-91f5f6e25c56",  # عکسی از یک دختر در فضای شهری
    "https://images.unsplash.com/photo-1599925997402-f3ad5036a20c",  # عکسی از یک دختر با استایل جالب
    "https://images.unsplash.com/photo-1612111416066-43eddddfb8bb",  # عکسی از یک دختر با لباس شیک
    "https://images.unsplash.com/photo-1604014704107-492e9da161d2",  # عکسی از یک دختر در فضای طبیعی
    "https://images.unsplash.com/photo-1599182684191-8db7f0d9d3ac",  # عکسی از یک دختر با استایل کلاسیک
    "https://images.unsplash.com/photo-1605763442188-e0d0177a03b5",  # عکسی از یک دختر در خیابان
    "https://images.unsplash.com/photo-1604629991954-5083f7cc5fa5",  # عکسی از یک دختر با استایل ورزشی
    "https://images.unsplash.com/photo-1599881133145-d9d3e299d38d",  # عکسی از یک دختر شیک در محیط شهری
    "https://images.unsplash.com/photo-1620044673315-7a68c6d29f28",  # عکسی از یک دختر زیبا
    "https://images.unsplash.com/photo-1620638041085-7abaf3c5dbb0",  # عکسی از یک دختر با استایل خاص
    "https://images.unsplash.com/photo-1607600387782-90b688de93b2",  # عکسی از یک دختر شیک
    "https://images.unsplash.com/photo-1614330335293-d6e089a1cf45",  # عکسی از یک دختر شیک و زیبا
    "https://images.unsplash.com/photo-1585777751304-592e1f45694e",  # عکسی از یک دختر در فضای باز
    "https://images.unsplash.com/photo-1600176092504-bc26be8ee435",  # عکسی از یک دختر با سبک شیک
    "https://images.unsplash.com/photo-1616104799448-e9d8d92a44c1",  # عکسی از یک دختر با استایل خاص
    "https://images.unsplash.com/photo-1605322097543-d32d5742ff91",  # عکسی از یک دختر با استایل مدرن
    "https://images.unsplash.com/photo-1598977263145-24095f90b508",  # عکسی از یک دختر در طبیعت
    "https://images.unsplash.com/photo-1612793435932-7e2ca82d5f32",  # عکسی از یک دختر با لباس شیک
    "https://images.unsplash.com/photo-1615648763748-0536898a01f6",  # عکسی از یک دختر با سبک جذاب
    "https://images.unsplash.com/photo-1603505314659-1209c3fdde78",  # عکسی از یک دختر شیک در خیابان
    "https://images.unsplash.com/photo-1591300536762-9b52e582fe76",  # عکسی از یک دختر خوش‌لباس
    "https://images.unsplash.com/photo-1616129338683-d274f88a7b7f",  # عکسی از یک دختر با استایل خاص
    "https://images.unsplash.com/photo-1616126954861-f10d1c43713f",  # عکسی از یک دختر با استایل جذاب
    "https://images.unsplash.com/photo-1621994996042-bcd6b6e1d325",  # عکسی از یک دختر زیبا
    "https://images.unsplash.com/photo-1600141352789-49f3cd89ab0f",  # عکسی از یک دختر شیک و باوقار
    "https://images.unsplash.com/photo-1599545434207-9a9b5d4d2c8c",  # عکسی از یک دختر مدرن و خوش‌تیپ
    "https://images.unsplash.com/photo-1605497647917-d79b50f65816",  # عکسی از یک دختر با استایل شیک
    "https://images.unsplash.com/photo-1607586464503-f1b5e9bca1b8",  # عکسی از یک دختر زیبا و شیک
    "https://images.unsplash.com/photo-1595381084774-d595e04626f2",  # عکسی از یک دختر در فضای طبیعی
    "https://images.unsplash.com/photo-1617810220349-e2fd21cb32d7",  # عکسی از یک دختر با لباس شیک
    "https://images.unsplash.com/photo-1612287999575-bf244f233340",  # عکسی از یک دختر شیک
    "https://images.unsplash.com/photo-1609862689938-7f31a4b96e1b",  # عکسی از یک دختر در فضای شهری
]

# کیبورد دکمه‌ها
girl_keyboard = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton(text="عکس بعدی", callback_data="next_girl")],
        [InlineKeyboardButton(text="بستن", callback_data="close")],
    ]
)

@app.on_message(filters.command(["پروف دختر"]))
async def girl_profile(c, m: Message):
    # انتخاب تصادفی یک عکس از لیست
    girl_url = random.choice(girl_photos)
    await m.reply_photo(girl_url, reply_markup=girl_keyboard)

@app.on_callback_query(filters.regex("next_girl"))
async def next_girl(c, m: CallbackQuery):
    # انتخاب تصادفی یک عکس جدید
    girl_url = random.choice(girl_photos)
    await m.edit_message_media(
        InputMediaPhoto(media=girl_url),
        reply_markup=girl_keyboard,
    )
