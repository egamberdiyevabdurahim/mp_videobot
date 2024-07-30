from aiogram.dispatcher.filters.state import State, StatesGroup


class CreatePost(StatesGroup):
    video = State()
    code = State()
    title = State()
    created_date = State()
    language = State()
    country = State()
    time_of = State()
    genre = State()
    quality = State()
    category = State()


class RegisterUser(StatesGroup):
    first_name = State()
    last_name = State()
    username = State()
    password = State()
    telegram_id = State()


class LoginState(StatesGroup):
    username = State()
    password = State()
    telegram_id = State()


class ImgToPdfState(StatesGroup):
    img = State()
    for_img = State()
    name = State()


class TranslateState(StatesGroup):
    first = State()
    second = State()
    third = State()


class PDFHistoryState(StatesGroup):
    first = State()


class CommandState(StatesGroup):
    first = State()


class BackgroundEraserState(StatesGroup):
    name = State()
    img = State()


class BackgroundHistoryState(StatesGroup):
    first = State()
