from TOKEN import TOKEN
from aiogram import Dispatcher, Bot, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import mysql.connector
import random

bot = Bot(TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
string_text = "a45345lppskraw2-48023979weujfakjw3ofna-0j312-3emraw0-430-24e0a-j231r-0aw43m0-1k3e-amfpa"

db = mysql.connector.Connect(
    host="localhost",
    user="root",
    password="free_fire0102",
    database="asisstent_bot"
)

cursor = db.cursor()


class UserStatesGroup(StatesGroup):
    first_name = State()
    last_name = State()
    phone_number = State()
    message = State()

    Photo = State()


async def create_new_user(state):
    async with state.proxy() as data:
        user = cursor.execute("INSERT INTO users (first_name, last_name, phone_number, message, Photo) "
                              "VALUES (%s, %s, %s, %s, %s)", (data['first_name'], data['last_name']
                                                              , data['phone_number'], data['message'], data['Photo']))
        db.commit()

    return user


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    register_btn = types.InlineKeyboardButton(text='/Register')
    kb.add(register_btn)
    await bot.send_message(message.chat.id, "Welcome To The Asisstant Bot", reply_markup=kb)


@dp.message_handler(commands=['Register'], state=None)
async def register(message: types.Message):
    chat_id = message.chat.id
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    cancel_btn = types.InlineKeyboardButton(text='/cancel')
    kb.add(cancel_btn)
    await bot.send_message(chat_id, "Enter Your Name", reply_markup=kb)
    await UserStatesGroup.first_name.set()


@dp.message_handler(state=UserStatesGroup.first_name)
async def enter_first_name(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        data['first_name'] = message.text
        print(data)
    await UserStatesGroup.next()
    await bot.send_message(chat_id, "Enter Your Last Name")


@dp.message_handler(state=UserStatesGroup.last_name)
async def enter_last_name(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        data['last_name'] = message.text
        print(data)
    await UserStatesGroup.next()
    await bot.send_message(chat_id, "Enter Your Phone Number\nIt should start with (+998)")


@dp.message_handler(state=UserStatesGroup.phone_number)
async def enter_phone_number(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    message.text.strip()
    split_msg = message.text.split("+")
    number_part = split_msg[1]
    try:
        print(int(number_part))
        async with state.proxy() as data:
            data['phone_number'] = message.text
            print(data)
        await UserStatesGroup.next()
        await bot.send_message(chat_id, "Enter Your Message")
    except ValueError:
        return await bot.send_message(chat_id, "You should enter a number")


@dp.message_handler(state=UserStatesGroup.message)
async def enter_message(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    async with state.proxy() as data:
        data['message'] = message.text
        print(data)
    await UserStatesGroup.next()
    await bot.send_message(chat_id, "Send Your Photo")


@dp.message_handler(lambda message: not message.photo, state=UserStatesGroup.Photo)
async def check_photo(message: types.Message):
    await message.reply("It's not a photo!.title()")


@dp.message_handler(content_types=['photo'], state=UserStatesGroup.Photo)
async def enter_photo(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "Downloading Proccess... ")

    get_channel_id = await bot.get_chat('@ixiyasov')
    channel_id = get_channel_id.id
    file_id = message.photo[-1].file_id
    file_info = await bot.get_file(file_id)
    downloaded_file = await bot.download_file(file_info.file_path)
    file_name = file_info.file_path.split("/")[1]
    rand_len = random.randint(1, len(string_text) - 1)
    rand_choice = string_text[: rand_len]
    hash_file_name = rand_choice + file_name

    async with state.proxy() as data_1:
        data_1['Photo'] = hash_file_name
        print(data_1)

    data = await state.get_data()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    phone_number = data.get('phone_number')
    user_message = data.get('message')
    photo = data.get('Photo')

    await bot.send_photo(chat_id=channel_id, photo=downloaded_file, caption=f"First Name: <b>{first_name}</b>\n"
                                                                            f"Last Name: <b>{last_name}</b>\n"
                                                                            f"Phone Number: <b>{phone_number}</b>\n"
                                                                            f"Message: <b>{user_message}</b>\n"
                                                                            f"Photo: <b>{photo}</b>", parse_mode='HTML')
    await create_new_user(state)
    await state.finish()
    await bot.send_message(chat_id=message.chat.id, text='Data successfully Saved',
                           reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    executor.start_polling(dp)
