print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaaaaaaaaaaaaaaaaa')

# import os
import csv
import datetime
import json
# import time
# import schedule
import img2pdf
import logging
# import asyncio
from io import BytesIO

from datetime import datetime
# from aiogram.types import ContentType
from aiogram import Bot, Dispatcher, types
# from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.contrib.middlewares.logging import LoggingMiddleware
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from aiogram.types import PhotoSize

import private
from api import (find_post, create_simple_user, history,
                 id_detector, used_adder,
                 check_user, sign_in)
from state import (RegisterUser, ImgToPdfState, PDFHistoryState,
                   LoginState)
# from Translator.translator import translator


bot = Bot(token=private.token)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

# COMMANDS = ['/start', '/register', '/login', '/img_to_pdf', '/pdf_history']


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    print("heyyyyyyyyyyyy")
    await message.reply(f"Assalamu Aleykum\n{message.from_user.first_name} Botimizga Xush Kelibsiz😊!")
    await message.answer("Kinoni Olish Uchun\nKino Kodini Kiriting... \n"
                         "Rasmni PDF ga aylantirish uchun /img_to_pdf ni bosing\n"
                         "Ro'yxatdan O'tmagan Bo'lsangiz /register ni bosing Va Ro'yxatdan O'ting\n"
                         "Tekshirish Uchun Birornarsa Yozing!")
    await message.answer("MP Universal Bot:\n"
                         "1) Rasmlarni PDF Formatiga Aylantiradi\n"
                         "2) Kodli Kinolar\n"
                         "3) Registratsiya✅\n\n"
                         "Registratsiyaning Afzalliklari:\n"
                         "1) 1 ta username, parol bilan ko'pkina profillarda ishlatsa Bo'ladi✅\n"
                         "2) Agar Telegram Profilingiz Uchib Ketsa Va Siz Bizning Botimizga "
                         "Sizga Kerak Bo'ladigon Kinoni Kodi Yoki PDF lar ni Qayta Tiklash Imkoni Bor:\n"
                         "      1) Yangi Telegram Profildan Botimizga O'tib Registartsiya yani Eski "
                         "username, parolingizni Kiritsangiz Va /pdf_history Bossangiz Barcha "
                         "PDF Laringizni Tiklash Iloji Bor!")


@dp.message_handler(commands=['register'])
async def register_command(message: types.Message):
    a = check_user(message.from_user.id)
    if a == 'Not Signed-in':
        await message.reply("Yangi Username Kiriting...\n"
                            "Etiborli Bo'ling Agarda Username Xato Kiritilsa Va Siz Bosh Telegram-dan "
                            "PDF laringizni Va Kino Uchun Yozgan Muxim Kodlaringizni Tiklay Olmaysiz!")
        await RegisterUser.username.set()
    elif a is True:
        await message.reply("Siz Registratsiyadan O'tgansiz\n")


@dp.message_handler(commands=['login'])
async def login_command(message: types.Message):
    a = check_user(message.from_user.id)
    if a == 'Not Signed-in':
        await message.reply("Username Kiriting...\n")
        await LoginState.username.set()
    elif a is True:
        await message.reply("Siz Login Qilgansiz\n"
                            "Savollar Uchun @MasterPhoneAdmin")


@dp.message_handler(commands=['pdf_history'])
async def pdf_history_command(message: types.Message):
    user = check_user(message.from_user.id)
    if user is True:
        mus = await message.answer("Yuklanmoqda...")
        id_of = id_detector(message.from_user.id)
        await message.answer_chat_action(action=types.ChatActions.TYPING)
        try:
            with open(f'CSV/{id_of}.csv', 'r') as f:
                lines = csv.reader(f, delimiter='|')
                for line in lines:
                    strip = line[2][:11].split("-"), line[2][11:16].split(":")
                    await mus.delete()
                    await message.answer(f"{line[0]}) Nomi: <{line[1]}>\n"
                                         f"Botga Yuklangan Sana: "
                                         f"{datetime(int(strip[0][0]), int(strip[0][1]), int(strip[0][2]), int(strip[1][0]), int(strip[1][1])).strftime('%m/%d/%Y %H:%M')}")
                await message.answer("Bulardan Birini Olish Uchun Raqamini Kiriting...")
            await PDFHistoryState.first.set()
        except FileNotFoundError:
            await mus.delete()
            await message.answer("Sizda Hechqanday PDF yo'q")
    elif user == 'Not Signed-in':
        await message.reply(f"{message.from_user.first_name} - Siz Botimizdan "
                            f"Ro'yxatdan O'tmagansiz Yoki Login Qilmagansiz\n"
                            f"Ro'yxatdan O'tish uchun /register ni Bosing\n"
                            f"Login Qilish Uchun /login ni Bosing")


@dp.message_handler(commands=['img_to_pdf'])
async def img_to_pdf_command(message: types.Message):
    user = check_user(message.from_user.id)
    if user is True:
        await message.reply(f"Rasm Yuboring...")
        await ImgToPdfState.img.set()
    elif user == 'Not Signed-in':
        await message.reply(f"{message.from_user.first_name} - Siz Botimizdan "
                            f"Ro'yxatdan O'tmagansiz Yoki Login Qilmagansiz\n"
                            f"Ro'yxatdan O'tish uchun /register ni Bosing\n"
                            f"Login Qilish Uchun /login ni Bosing")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def founding(message: types.Message):
    user = check_user(message.from_user.id)
    if user is True:
        used_adder(message.from_user.id)
        code = message.text
        txt = await message.reply(text="Qidirilmoqda... ")
        vid = find_post(message.text)
        await txt.delete()
        if vid is None:
            await message.reply(f"{code} - Bonday Kodli Kino Mavjud Emas\nIltimos Qaytadan Urunib Ko'ring!")
        else:
            history(code, message.from_user.id)
            await message.reply(text="Topildi✅")
            beige1 = '🔸'
            blue1 = '🔹'
            mus = await message.answer(text=10 * beige1)
            for i in range(1, 11):
                blue = i * blue1
                beige = (10 - i) * beige1
                await message.answer_chat_action(action=types.ChatActions.TYPING)
                await mus.edit_text(f'{blue}{beige}\n {i * 10}% Yuklanmoqda')
                # await asyncio.sleep(0.000001)
            await mus.delete()
            await message.answer_video(vid['video'], caption=f"Nomi: {vid['title']}🎬\n"
                                                             f"‣ Kodi: {vid['code']}\n"
                                                             f"‣ Tili: {vid['language']}\n"
                                                             f"‣ Mamlakati: {vid['country']}\n"
                                                             f"‣ Davomiyligi: {vid['time_of']}\n"
                                                             f"‣ Sifati: {vid['quality']}\n"
                                                             f"‣ Chiqarilgan Sanasi: {vid['created_date']}\n"
                                                             f"‣ Janri: {vid['genre']}\n"
                                                             f"‣ Kategoriyasi: {vid['category']}",)
    elif user == 'Not Signed-in':
        await message.reply(f"{message.from_user.first_name} - Siz Botimizdan "
                            f"Ro'yxatdan O'tmagansiz Yoki Login Qilmagansiz\n"
                            f"Ro'yxatdan O'tish uchun /register ni Bosing\n"
                            f"Login Qilish Uchun /login ni Bosing")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# STATES
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# REGISTER STATE
@dp.message_handler(state=RegisterUser.username)
async def register1(message: types.Message, state: FSMContext):
    if message.from_user.last_name is None:
        last_name = 'Mavjud Emas'
    else:
        last_name = message.from_user.last_name
    await state.update_data(username=message.text)
    await state.update_data(first_name=message.from_user.first_name)
    await state.update_data(last_name=last_name)
    await state.update_data(telegram_id=message.from_user.id)
    await message.reply(f"Parol Kiriting...")
    await RegisterUser.password.set()


@dp.message_handler(state=RegisterUser.password)
async def register2(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    dat = await state.get_data()
    a = create_simple_user(dat.get('telegram_id'),
                           dat.get('first_name'),
                           dat.get('last_name'),
                           dat.get('password'),
                           dat.get('username')
                           )
    mus = await message.answer("Yuklanmoqda...")
    if a == 'Sign-In':
        await mus.delete()
        await message.answer("Bunday Username Mavjud!")
        await state.finish()
    elif a is None:
        await state.finish()
        await mus.delete()
        await message.answer(f"{message.from_user.first_name} - Siz Muvaffaqiyatli Ro'yxatdan O'tdingiz!")
        used_adder(message.from_user.id)


# LOGIN STATE
@dp.message_handler(state=LoginState.username)
async def login1(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.update_data(telegram_id=message.from_user.id)
    await message.answer("Parolni Kiriting...")
    await LoginState.password.set()


@dp.message_handler(state=LoginState.password)
async def login2(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    dat = await state.get_data()
    a = sign_in(dat.get('telegram_id'),
                dat.get('password'),
                dat.get('username')
                )
    if a == "Password is incorrect":
        await message.answer("Parol Xato")
        await state.finish()
    elif a == 'Not Registered':
        await message.answer("Siz Ro'yxatdan O'tmagansiz!")
        await state.finish()
    elif a is None:
        await message.answer(f"{message.from_user.first_name} - Siz Muvaffaqiyatli Login Qildingiz!")
        await state.finish()
        used_adder(message.from_user.id)


# IMG TO PDF STATE
@dp.message_handler(state=ImgToPdfState.img, content_types=types.ContentType.PHOTO)
async def img_to(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    photo_file = await photo.download(destination=BytesIO())
    pdf_bytes = img2pdf.convert(photo_file)
    await state.update_data(img=pdf_bytes)
    await state.update_data(for_img=photo)
    photo_file.close()
    await message.answer(text='Nomini Kiriting: \n'
                              "Nomiga Ahamiyatli Bo'ling Sababi Tiklayotkanizda Nomi Va Sanasi Bilan Tiklaysiz!")
    used_adder(message.from_user.id)
    await ImgToPdfState.name.set()


@dp.message_handler(state=ImgToPdfState.name)
async def name_to(message: types.Message, state: FSMContext):
    beige1 = '🔸'
    blue1 = '🔹'
    mus = await message.answer(text=10 * beige1)
    for i in range(1, 11):
        blue = i * blue1
        beige = (10 - i) * beige1
        await message.answer_chat_action(action=types.ChatActions.TYPING)
        await mus.edit_text(f'{blue}{beige}\n {i * 10}% Rasm PDF ga Aylantirilmoqda')
    data = await state.get_data()
    pdf_stream = BytesIO(data.get('img'))
    name = message.text
    pdf_stream.name = f'{name}.pdf'
    await mus.delete()
    await message.answer("Tayyor✅")
    await message.reply_document(pdf_stream)
    id_of = id_detector(message.from_user.id)
    try:
        with open(f'CSV/{id_of}.csv', 'r') as f:
            lines = csv.reader(f, delimiter='|')
            code = [num[0] for num in lines]
    except FileNotFoundError:
        code = [0]
    with open(f'CSV/{id_of}.csv', 'a') as f:
        a = json.dumps(dict(data.get('for_img')))
        f.write(f"{int(max(code))+1}|{name}|{datetime.now()}|{a}\n")
    used_adder(message.from_user.id)
    await state.finish()


# PDF HISTORY
@dp.message_handler(state=PDFHistoryState.first)
async def pdf_history1(message: types.Message, state: FSMContext):
    a = await message.answer('Aniqlanmoqda...')
    code = message.text
    id_of = id_detector(message.from_user.id)
    used_adder(message.from_user.id)
    try:
        with open(f'CSV/{id_of}.csv', 'r') as f:
            lines = csv.reader(f, delimiter='|')
            mess = False
            for line in lines:
                if line[0] == code:
                    await a.delete()
                    beige1 = '🔸'
                    blue1 = '🔹'
                    mus = await message.answer(text=10 * beige1)
                    for i in range(1, 11):
                        blue = i * blue1
                        beige = (10 - i) * beige1
                        await message.answer_chat_action(action=types.ChatActions.TYPING)
                        await mus.edit_text(f'{blue}{beige}\n {i * 10}% Yuklanmoqda')
                    mess = True
                    a = json.loads(line[3])
                    b = PhotoSize(**a)
                    photo_file = await b.download(destination=BytesIO())
                    pdf_bytes = img2pdf.convert(photo_file)
                    photo_file.close()
                    pdf_stream = BytesIO(pdf_bytes)
                    pdf_stream.name = f"{line[1]}.pdf"
                    await mus.delete()
                    await message.answer("Tayyor✅")
                    await message.reply_document(pdf_stream)
                    await state.finish()
                    break
            if not mess:
                await a.delete()
                await message.answer("Xato Kiritdingiz\nBoshidan Urunib Ko'ring!")
                await state.finish()
    except FileNotFoundError:
        await a.delete()
        await message.answer("Sizda PDF lar tarihi mavjud emas!\nAvval Rasmni PAD formatga aylantiring /img_to_pdf")
        await state.finish()


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.create_task(scheduler())
    executor.start_polling(dp, skip_updates=True)
