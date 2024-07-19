# @dp.message_handler(commands=['boom'])
# async def bomber(message: types.Message):
#     await message.reply('Telegram Id Kiriting... ')
#     await BoomState.first.set()
#
#
# @dp.message_handler(state=BoomState.first)
# async def bomber(message: types.Message):
#     mess = 0
#     while mess < 101:
#         # a = await bot.send_message(chat_id=message.text, text='Gruppa Stop😂')
#         # await a.forward(chat_id=message.text)
#         # message_sent = await bot.send_message(chat_id=1336740177, text='Group😂')
#         # await message_sent.forward(chat_id=2166109253)
#         await asyncio.sleep(1)
#         print(mess)
#         mess += 1


# LANGUAGES = ["Uzbek🇺🇿", 'Türkçe🇹🇷', "English🇬🇧", "Español🇪🇸", "Français🇫🇷", "Deutsch🇩🇪", "Italiano🇮🇹", "Русский🇷🇺", "中文(Xitoy)🇨🇳", "日本語(Yapon)🇯🇵", "한국어(Koreys)🇰🇷", "(Arab)عربي🇸🇦"]
# langs = ['uz', 'tr', 'en', 'es', 'fr', 'de', 'it', 'ru', 'cn', 'jp', 'kr', 'sa']


# def language_buttons():
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     for lang in langs:
#         buttons = [types.InlineKeyboardButton(text=x, callback_data=lang) for x in LANGUAGES]
#     markup.add(*buttons)
#     return markup


# def second_language_buttons():
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     for lang in langs:
#         buttons = [types.InlineKeyboardButton(text=x, callback_data=lang) for x in LANGUAGES]
#     markup.add(*buttons)
#     return markup


# @dp.message_handler(commands=['translate'])
# async def translate_command(message: types.Message):
#     await message.reply(f"So'z Yozing...")
#     await message.answer("Qaysi Tildan: ", reply_markup=language_buttons())
#     await TranslateState.first.set()
#
#
# def language_buttons():
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     buttons = [types.InlineKeyboardButton(text=lang, callback_data=lang) for lang in LANGUAGES]
#     markup.add(*buttons)
#     return markup
#
#
# @dp.callback_query_handler(lambda c: c.data in LANGUAGES, state=TranslateState.first)
# async def process_language_choice(callback_query: types.CallbackQuery, state: FSMContext):
#     selected_language = callback_query.data
#     await bot.answer_callback_query(callback_query.id, f"Selected language: {selected_language}")
#     await bot.send_message(callback_query.from_user.id, f"You have selected {selected_language}.")
#     await state.update_data(selected_language)
#     await TranslateState.second.set()
#
#
# @dp.message_handler(state=TranslateState.second)
# async def translate_command2(message: types.Message, state: FSMContext):
#     await message.answer("Qaysi Tilga: ", reply_markup=sec_language_buttons())
#     await state.update_data(None)
#     await TranslateState.third.set()
#
#
# def sec_language_buttons():
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     buttons = [types.InlineKeyboardButton(text=lang, callback_data=lang) for lang in LANGUAGES]
#     markup.add(*buttons)
#     return markup
#
#
# @dp.callback_query_handler(lambda c: c.data in LANGUAGES, state=TranslateState.third)
# async def process_language_choice(callback_query: types.CallbackQuery, state: FSMContext):
#     selected_language = callback_query.data
#     await bot.answer_callback_query(callback_query.id, f"Selected language: {selected_language}")
#     await bot.send_message(callback_query.from_user.id, f"You have selected {selected_language}.")
#     await state.update_data(selected_language)
#     data = await state.get_data()
#     await bot.answer_callback_query(callback_query.from_user.id, text=data.get('first'))


# VIDEO_QUALITIES = ["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p", "4320p"]


# @dp.message_handler(state=TranslateState.first)
# async def name_to(message: types.Message, state: FSMContext):
#     mess = message.text
    # en_trans = EnTarjimon(text=mess)
    # ru_trans = RuTarjimon(text=mess)
    # await message.answer(text=f'Kiritildi - {mess}\n'
    #                           f'Ingliz Tilida - {en_trans}\nRus Tilida - {ru_trans}')
    # await state.finish()


# @dp.message_handler(state=CreatePost.video, content_types=types.ContentType.VIDEO)
# async def create_post1(message: types.Message, state: FSMContext):
#     print('video')
#     video = message.video
#     file_info = await bot.get_file(video.file_id)
#     file_path = file_info.file_path
#     file_url = f'https://api.telegram.org/file/bot{token}/{file_path}'
#     await state.update_data(video=file_url)
#     await message.answer("Kodini Kiriting...")
#     await CreatePost.code.set()
#
#
# @dp.message_handler(state=CreatePost.code)
# async def create_post2(message: types.Message, state: FSMContext):
#     print('code')
#     await state.update_data(code=message.text)
#     await message.answer("Nomini Kiriting...")
#     await CreatePost.title.set()
#
#
# @dp.message_handler(state=CreatePost.title)
# async def create_post3(message: types.Message, state: FSMContext):
#     print('title')
#     await state.update_data(title=message.text)
#     await message.answer("Chiqarilgan Sanasini Kiriting...")
#     await CreatePost.created_date.set()
#
#
# @dp.message_handler(state=CreatePost.created_date)
# async def create_post4(message: types.Message, state: FSMContext):
#     print('created_date')
#     await state.update_data(created_date=message.text)
#     await message.answer("Tilini Kiriting...")
#     await CreatePost.language.set()
#
#
# @dp.message_handler(state=CreatePost.language)
# async def create_post5(message: types.Message, state: FSMContext):
#     print('language')
#     await state.update_data(language=message.text)
#     await message.answer("Davlatini Kiriting...")
#     await CreatePost.country.set()
#
#
# @dp.message_handler(state=CreatePost.country)
# async def create_post6(message: types.Message, state: FSMContext):
#     print('country')
#     await state.update_data(country=message.text)
#     await message.answer("Video Uzunligini Kiriting...")
#     await CreatePost.time_of.set()
#
#
# @dp.message_handler(state=CreatePost.time_of)
# async def create_post7(message: types.Message, state: FSMContext):
#     print('time_of')
#     await state.update_data(time_of=message.text)
#     await message.answer("Janrini Kiriting...")
#     await CreatePost.genre.set()
#
#
# @dp.message_handler(state=CreatePost.genre)
# async def create_post8(message: types.Message, state: FSMContext):
#     print('genre')
#     await state.update_data(genre=message.text)
#     await message.answer("Sifatini Kiriting...")
#     await CreatePost.quality.set()
#
#
# @dp.message_handler(state=CreatePost.quality)
# async def create_post9(message: types.Message, state: FSMContext):
#     print('quality')
#     await state.update_data(quality=message.text)
#     await message.answer("Kategoriyasini Tanlang Kiriting...")
#     url = f"{BASE_URL}/category/"
#     response = requests.get(url=url).text
#     dat = json.loads(response)
#     for x in dat:
#         for key, value in x.items():
#             await message.answer(text=f"{key}: {value}")
#     await CreatePost.category.set()
#
#
# @dp.message_handler(state=CreatePost.category)
# async def create_post10(message: types.Message, state: FSMContext):
#     print('category')
#     await state.update_data(category=message.text)
#     # await state.finish()
#     dat = await state.get_data()
#     async with aiohttp.ClientSession() as session:
#         async with session.get(dat.get('video')) as response:
#             video_data = response.read()
#             files = {'file': ('video.mp4', video_data)}
#             await state.update_data(video=files)
#     await message.answer(text=f"Data: {dat}")
#     vid = create_post(dat.get('video'),
#                       dat.get('code'),
#                       dat.get('title'),
#                       dat.get('created_date'),
#                       dat.get('language'),
#                       dat.get('country'),
#                       dat.get('time_of'),
#                       dat.get('genre'),
#                       dat.get('quality'),
#                       )
#     print(vid)
    # await message.answer_video(vid['video'], caption=f"Nomi: {vid['title']}🎬\n"
    #                                                  f"‣ Kodi: {vid['code']}\n"
    #                                                  f"‣ Tili: {vid['language']}\n"
    #                                                  f"‣ Mamlakati: {vid['country']}\n"
    #                                                  f"‣ Davomiyligi: {vid['time_of']}\n"
    #                                                  f"‣ Sifati: {vid['quality']}\n"
    #                                                  f"‣ Chiqarilgan Sanasi: {vid['created_date']}\n"
    #                                                  f"‣ Janri: {vid['genre']}\n"
    #                                                  f"‣ Kategoriyasi: {vid['category']}", )