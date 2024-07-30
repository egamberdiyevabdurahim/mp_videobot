import os
import csv
import datetime
import json

import img2pdf
import logging

from io import BytesIO

from rembg import remove

from PIL import Image

from datetime import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from aiogram.types import PhotoSize

import private
from api import (find_post, create_simple_user, history,
                 id_detector, used_adder,
                 check_user, sign_in, about)
from state import (RegisterUser, ImgToPdfState, PDFHistoryState,
                   LoginState, CommandState, BackgroundEraserState,
                   BackgroundHistoryState)


bot = Bot(token=private.token)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)


COMMANDS = ['/start', '/stop', '/register', '/login', '/img_to_pdf', '/pdf_history']


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# COMMADS

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(f"Assalamu Aleykum\n{message.from_user.first_name} Botimizga Xush Kelibsiz😊!\n\n"
                        "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")
    await message.answer(f"Kinoni Olish Uchun\nKino Kodini Kiriting... \n"
                         f"Rasmni PDF ga aylantirish uchun /img_to_pdf ni bosing\n"
                         f"Rasmni Background-i ni Uchirish Uchun /background_eraser ni bosing\n"
                         f"Ro'yxatdan O'tmagan Bo'lsangiz /register ni bosing Va Ro'yxatdan O'ting\n"
                         f"Tekshirish Uchun Birornarsa Yozing!")
    await message.answer("MP Universal Bot:\n"
                         "1) Rasmlarni PDF Formatiga Aylantiradi\n"
                         "2) Rasmlarni Background(Orqa Fon)-i ni Uchiradi\n"
                         "2) Kodli Kinolar\n"
                         "3) Registratsiya✅\n\n"
                         "Registratsiyaning Afzalliklari:\n"
                         "1) 1 ta username, parol bilan ko'pkina profillarda ishlatsa Bo'ladi✅\n"
                         "2) Agar Telegram Profilingiz Uchib Ketsa Va Siz Bizning Botimizga "
                         "Sizga Kerak Bo'ladigon Kinoni Kodi, Background-i Uchirilgan Rasmlar Yoki PDF lar ni Qayta Tiklash Imkoni Bor:\n"
                         "      1) Yangi Telegram Profildan Botimizga O'tib Registartsiya yani Eski "
                         "username, parolingizni Kiritsangiz Va:"
                                    "1) /pdf_history Bossangiz Barcha PDF Laringizni Tiklash Iloji Bor!"
                                    "2) /back_er_history Bossangiz Barcha Background-i Uchirilgan Rasmlarni Tiklash Iloji Bor!")


@dp.message_handler(commands=['register'])
async def register_command(message: types.Message):
    a = check_user(message.from_user.id)
    if a == 'Not Signed-in':
        await message.reply("Yangi Username Kiriting...\n"
                            "Etiborli Bo'ling Agarda Username Xato Kiritilsa Va Siz Bosh Telegram-dan "
                            "PDF laringizni Va Kino Uchun Yozgan Muxim Kodlaringizni Tiklay Olmaysiz!\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")
        await RegisterUser.username.set()
    elif a is True:
        await message.reply("Siz Registratsiyadan O'tgansiz\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")


@dp.message_handler(commands=['login'])
async def login_command(message: types.Message):
    a = check_user(message.from_user.id)
    if a == 'Not Signed-in':
        await message.reply("Username Kiriting...\n")
        await LoginState.username.set()
    elif a is True:
        await message.reply("Siz Login Qilgansiz\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")


@dp.message_handler(commands=['pdf_history'])
async def pdf_history_command(message: types.Message):
    user = check_user(message.from_user.id)
    if user is True:
        mus = await message.answer("Yuklanmoqda...")
        id_of = id_detector(message.from_user.id)
        await message.answer_chat_action(action=types.ChatActions.TYPING)
        try:
            with open(f'CSV/{id_of}?PDF.csv', 'r') as f:
                lines = csv.reader(f, delimiter='|')
                await mus.delete()
                for line in lines:
                    strip = line[2][:11].split("-"), line[2][11:16].split(":")
                    await message.answer(f"{line[0]}) Nomi: <{line[1]}>\n"
                                        f"Botga Yuklangan Sana: "
                                        f"{datetime(int(strip[0][0]), int(strip[0][1]), int(strip[0][2]), int(strip[1][0]), int(strip[1][1])).strftime('%m/%d/%Y %H:%M')}")
                await message.answer("Bulardan Birini Olish Uchun Raqamini Kiriting...\n\n"
                                    "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")
            await PDFHistoryState.first.set()
        except FileNotFoundError:
            await mus.edit_text(f"Sizda PDF-ga Aylantirilgan Rasmlar Mavjud Emas!")
    elif user == 'Not Signed-in':
        await message.reply(f"{message.from_user.first_name} - Siz Botimizdan "
                            f"Ro'yxatdan O'tmagansiz Yoki Login Qilmagansiz\n"
                            f"Ro'yxatdan O'tish uchun /register ni Bosing\n"
                            f"Login Qilish Uchun /login ni Bosing\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")


@dp.message_handler(commands=['img_to_pdf'])
async def img_to_pdf_command(message: types.Message):
    user = check_user(message.from_user.id)
    if user is True:
        await message.reply("Rasm Yuboring...")
        await ImgToPdfState.img.set()
    elif user == 'Not Signed-in':
        await message.reply(f"{message.from_user.first_name} - Siz Botimizdan "
                            f"Ro'yxatdan O'tmagansiz Yoki Login Qilmagansiz\n"
                            f"Ro'yxatdan O'tish uchun /register ni Bosing\n"
                            f"Login Qilish Uchun /login ni Bosing\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")


@dp.message_handler(commands=["profile"])
async def profile(message: types.Message):
    user = check_user(message.from_user.id)
    if user is True:
        mess = await message.answer("Yuklanmoqda...")
        abo = about(message.from_user.id)
        await mess.delete()
        await message.reply(f"Sizning Malumotlaringiz:\n"
                         f"Username: {abo.get('username')}\n"
                         f"Ism: {abo.get('first_name')}\n"
                         f"Familya: {abo.get('last_name')}\n"
                         f"Parol: {abo.get('password')}\n"
                         f"Telegram ID-yingiz: {message.from_user.id}\n\n"
                         "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")
    elif user == 'Not Signed-in':
        await message.reply(f"{message.from_user.first_name} - Siz Botimizdan "
                            f"Ro'yxatdan O'tmagansiz Yoki Login Qilmagansiz\n"
                            f"Ro'yxatdan O'tish uchun /register ni Bosing\n"
                            f"Login Qilish Uchun /login ni Bosing\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")


@dp.message_handler(commands=['background_eraser'])
async def backgroud_eraser_command(message: types.Message):
    user = check_user(message.from_user.id)
    if user is True:
        await message.reply("Rasm Yuboring...")
        await BackgroundEraserState.img.set()
    else:
        await message.reply(f"{message.from_user.first_name} - Siz Botimizdan "
                            f"Ro'yxatdan O'tmagansiz Yoki Login Qilmagansiz\n"
                            f"Ro'yxatdan O'tish uchun /register ni Bosing\n"
                            f"Login Qilish Uchun /login ni Bosing\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")


@dp.message_handler(commands=['back_er_history'])
async def background_eraser_history_command(message: types.Message):
    user = check_user(message.from_user.id)
    if user is True:
        mus = await message.answer("Yuklanmoqda...")
        id_of = id_detector(message.from_user.id)
        await message.answer_chat_action(action=types.ChatActions.TYPING)
        try:
            with open(f'CSV/{id_of}?Back.csv', 'r') as f:
                lines = csv.reader(f, delimiter='|')
                await mus.delete()
                for line in lines:
                    strip = line[2][:11].split("-"), line[2][11:16].split(":")
                    await message.answer(f"{line[0]}) Nomi: <{line[1]}>\n"
                                        f"Botga Yuklangan Sana: "
                                        f"{datetime(int(strip[0][0]), int(strip[0][1]), int(strip[0][2]), int(strip[1][0]), int(strip[1][1])).strftime('%m/%d/%Y %H:%M')}")
                await message.answer("Bulardan Birini Olish Uchun Raqamini Kiriting...\n\n"
                                    "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")
            await BackgroundHistoryState.first.set()
        except FileNotFoundError:
            await message.answer("Sizda Background(Orqa Fon)-i Uchirilgan Rasm Mavjud Emas!")
    elif user == 'Not Signed-in':
        await message.reply(f"{message.from_user.first_name} - Siz Botimizdan "
                            f"Ro'yxatdan O'tmagansiz Yoki Login Qilmagansiz\n"
                            f"Ro'yxatdan O'tish uchun /register ni Bosing\n"
                            f"Login Qilish Uchun /login ni Bosing\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")


@dp.message_handler(commands=['support', 'help'])
async def support_command(message: types.Message):
    await message.answer(f"Yordam, Maslahat, Yangi Ideyalar, Xatolar Uchun:\n"
                         "@MasterPhoneAdmin✅")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# VIDEO FOUNDING

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
            await message.reply(f"{code} - Bonday Kodli Kino Mavjud Emas\nIltimos Qaytadan Urunib Ko'ring!\n\n"
                               "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")
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
                                                             f"‣ Kategoriyasi: {vid['category']}\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")
    elif user == 'Not Signed-in':
        await message.reply(f"{message.from_user.first_name} - Siz Botimizdan "
                            f"Ro'yxatdan O'tmagansiz Yoki Login Qilmagansiz\n"
                            f"Ro'yxatdan O'tish uchun /register ni Bosing\n"
                            f"Login Qilish Uchun /login ni Bosing\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# STATES
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# REGISTER STATE
@dp.message_handler(state=RegisterUser.username)
async def register1(message: types.Message, state: FSMContext):
    commad_check = await stop1(message=message)
    if commad_check is True:
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
    else:
        await state.finish()


@dp.message_handler(state=RegisterUser.password)
async def register2(message: types.Message, state: FSMContext):
    commad_check = await stop1(message=message)
    if commad_check is True:
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
            await message.answer("Bunday Username Mavjud!\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")
            await state.finish()
        elif a is None:
            await state.finish()
            await mus.delete()
            await message.answer(f"{message.from_user.first_name} - Siz Muvaffaqiyatli Ro'yxatdan O'tdingiz!\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")
            used_adder(message.from_user.id)
    else:
        await state.finish()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# LOGIN STATE
@dp.message_handler(state=LoginState.username)
async def login1(message: types.Message, state: FSMContext):
    commad_check = await stop1(message=message)
    if commad_check is True:
        await state.update_data(username=message.text)
        await state.update_data(telegram_id=message.from_user.id)
        await message.answer("Parolni Kiriting...")
        await LoginState.password.set()
    else:
        await state.finish()


@dp.message_handler(state=LoginState.password)
async def login2(message: types.Message, state: FSMContext):
    commad_check = await stop1(message=message)
    if commad_check is True:
        await state.update_data(password=message.text)
        dat = await state.get_data()
        a = sign_in(dat.get('telegram_id'),
                    dat.get('password'),
                    dat.get('username')
                    )
        if a == "Password is incorrect":
            await message.answer("Parol Xato\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")
            await state.finish()
        elif a == 'Not Registered':
            await message.answer("Siz Ro'yxatdan O'tmagansiz!\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")
            await state.finish()
        elif a is None:
            await message.answer(f"{message.from_user.first_name} - Siz Muvaffaqiyatli Login Qildingiz!\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")
            await state.finish()
            used_adder(message.from_user.id)
    else:
        await state.finish()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# IMG TO PDF STATE
@dp.message_handler(state=ImgToPdfState.img, content_types=types.ContentType.ANY)
async def img_to(message: types.Message, state: FSMContext):
    if message.content_type == types.ContentType.PHOTO:
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
    else:
        await message.answer("PDF-ga Aylantirish Uchun Rasm Yuboring...\n"
                             "Boshidan Ishaltish Uchun Bosing --> /img_to_pdf\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")
        used_adder(message.from_user.id)
        await state.finish()


@dp.message_handler(state=ImgToPdfState.name)
async def name_to(message: types.Message, state: FSMContext):
    commad_check = await stop1(message=message)
    if commad_check is True:
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
        await message.reply_document(pdf_stream, caption="By: @MPUniversalBot\n\nXatolar, Maslahat, Yangi Ideyalar Uchun /support")
        id_of = id_detector(message.from_user.id)
        try:
            with open(f'CSV/{id_of}?PDF.csv', 'r') as f:
                lines = csv.reader(f, delimiter='|')
                code = [num[0] for num in lines]
        except FileNotFoundError:
            code = [0]
        with open(f'CSV/{id_of}?PDF.csv', 'a') as f:
            a = json.dumps(dict(data.get('for_img')))
            f.write(f"{int(max(code))+1}|{name}|{datetime.now()}|{a}\n")
        used_adder(message.from_user.id)
        await state.finish()
    else:
        await state.finish()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# PDF HISTORY STATE
@dp.message_handler(state=PDFHistoryState.first)
async def pdf_history1(message: types.Message, state: FSMContext):
    commad_check = await stop1(message=message)
    if commad_check is True:
        a = await message.answer('Aniqlanmoqda...')
        code = message.text
        id_of = id_detector(message.from_user.id)
        used_adder(message.from_user.id)
        with open(f'CSV/{id_of}?PDF.csv', 'r') as f:
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
                    await message.reply_document(pdf_stream, caption="By: @MPUniversalBot\n\nXatolar, Maslahat, Yangi Ideyalar Uchun /support")
                    await state.finish()
                    break
            if not mess:
                await a.delete()
                await message.answer("Xato Kiritdingiz\nBoshidan Urunib Ko'ring!\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")
                await state.finish()
    else:
         await state.finish()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# IMG BACKGROUND ERASER STATE

@dp.message_handler(state=BackgroundEraserState.img, content_types=types.ContentType.ANY)
async def img_to_back(message: types.Message, state: FSMContext):
    if message.content_type == types.ContentType.PHOTO:
        photo = message.photo[-1]
        photo_file = await photo.download(destination=BytesIO())
        await state.update_data(img=photo)
        photo_file.close()
        await message.answer(text='Nomini Kiriting: \n'
                                    "Nomiga Ahamiyatli Bo'ling Sababi Tiklayotkanizda Nomi Va Sanasi Bilan Tiklaysiz!")
        used_adder(message.from_user.id)
        await BackgroundEraserState.name.set()
    else:
        await message.answer("Background(Orqa Fon)-ni O'chirish Uchun Rasm Yuboring...\n"
                             "Boshidan Ishaltish Uchun Bosing --> /background_eraser\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")
        used_adder(message.from_user.id)
        await state.finish()


@dp.message_handler(state=BackgroundEraserState.name)
async def name_to_background(message: types.Message, state: FSMContext):
    commad_check = await stop1(message=message)
    if commad_check is True:
        beige1 = '🔸'
        blue1 = '🔹'
        mus = await message.answer(text=10 * beige1)
        for i in range(1, 11):
            blue = i * blue1
            beige = (10 - i) * beige1
            await message.answer_chat_action(action=types.ChatActions.TYPING)
            await mus.edit_text(f'{blue}{beige}\n {i * 10}% Rasmni Background(Orqa Fon)-i Uchirilmoqda')
        data = await state.get_data()
        name = message.text
        photo = data.get('img')
        photo_file = await photo.download(destination=BytesIO())
    
        input_image = Image.open(photo_file)
        output_image = remove(input_image)

        output_bytes = BytesIO()
        output_image.save(output_bytes, format='PNG')
        output_bytes.seek(0)

        await mus.delete()
        await message.answer("Tayyor✅")
        await message.reply_photo(photo=output_bytes, caption=f"{name}\nBy: @MPUniversalBot\n\nXatolar, Maslahat, Yangi Ideyalar Uchun /support")
        id_of = id_detector(message.from_user.id)
        try:
            with open(f'CSV/{id_of}?Back.csv', 'r') as f:
                lines = csv.reader(f, delimiter='|')
                code = [num[0] for num in lines]
        except FileNotFoundError:
            code = [0]
        with open(f'CSV/{id_of}?Back.csv', 'a') as f:
            a = json.dumps(dict(data.get('img')))
            f.write(f"{int(max(code))+1}|{name}|{datetime.now()}|{a}\n")
        used_adder(message.from_user.id)
        await state.finish()
    else:
        await state.finish()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# IMG BACKGROUND ERASER HISTORY STATE

@dp.message_handler(state=BackgroundHistoryState.first)
async def background_eraser_history1(message: types.Message, state: FSMContext):
    commad_check = await stop1(message=message)
    if commad_check is True:
        a = await message.answer('Aniqlanmoqda...')
        code = message.text
        id_of = id_detector(message.from_user.id)
        used_adder(message.from_user.id)
        with open(f'CSV/{id_of}?Back.csv', 'r') as f:
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

                    input_image = Image.open(photo_file)
                    output_image = remove(input_image)

                    output_bytes = BytesIO()
                    output_image.save(output_bytes, format='PNG')
                    output_bytes.seek(0)

                    photo_file = await b.download(destination=BytesIO())
                    photo_file.seek(0)

                    await mus.delete()
                    await message.answer("Tayyor✅")
                    await message.answer_photo(photo=photo_file, caption=f"Orginal Rasm: {line[1]}\nBy: @MPUniversalBot\n\nXatolar, Maslahat, Yangi Ideyalar Uchun /support")
                    photo_file.close()
                    await message.reply_photo(photo=output_bytes, caption=f"Background(Orqa Fon)-i Uchirilgan Rasm: {line[1]}\nBy: @MPUniversalBot\n\nXatolar, Maslahat, Yangi Ideyalar Uchun /support")
                    await state.finish()
                    break
            if not mess:
                await a.delete()
                await message.answer("Xato Kiritdingiz\nBoshidan Urunib Ko'ring!\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")
                await state.finish()
    else:
         await state.finish()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# STOP STATE

@dp.message_handler(content_types=types.ContentType.TEXT)
async def stop1(message: types.Message):
    if message.text in COMMANDS:
         await message.answer("Toxtatildi!\n"
                              "Komanda Kiritkan Bo'lsangiz Boshidan Kiriting!\n\n"
                            "Xatolar, Maslahat, Yangi Ideyalar Uchun /support")
         return False
    return True


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# RUNNING
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
