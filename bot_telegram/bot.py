from random import randint

import config
from bot_telegram import weather
from bot_telegram import convert_currencies
from bot_telegram import polls_creator

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from bot_telegram.keyboards import keyboard_client

storage = MemoryStorage()
bot = Bot(config.TOKEN_API)
dispatcher = Dispatcher(bot, storage=storage)

weather.register_handlers(dispatcher)
convert_currencies.register_handlers(dispatcher)
polls_creator.register_handlers(dispatcher)

# Пытается отправить сообщение в личку, если не выходит, отправляет его в тот же чат, откуда уловил команду
# Работает и с текстовыми сообщениями и с фотографиями, может оставлять подписи к фото
async def try_to_send_it(message: types.Message, text: str = '', photo_url: str = ''):
    if photo_url != '':
        try:
            await bot.send_photo(
                chat_id=message.from_user.id, photo=photo_url, caption=text, reply_markup=keyboard_client)
        except:
            await bot.send_photo(
                chat_id=message.chat.id, photo=photo_url, caption=text, reply_markup=keyboard_client)
    elif text != '':
        try:
            await bot.send_message(message.from_user.id, text, reply_markup=keyboard_client)
        except:
            await message.answer(text=text, reply_markup=keyboard_client)

# Улавливает команду /start, приветствует также в одном сообщении отправляет текст с описанием всех команд
# Тест приветствия в config.START_MESSAGE, текст описания команд в config.HELP_MESSAGE
@dispatcher.message_handler(commands=['start'])
async def command_start(message: types.Message):
    message_answer = config.START_MESSAGE + '\n' + config.HELP_MESSAGE
    await try_to_send_it(message, message_answer)
    await message.delete()

# Улавливает команду /help, отправляет текст с описанием всех команд
# Текст описания команд в config.HELP_MESSAGE
@dispatcher.message_handler(commands=['help'])
async def command_help(message: types.Message):
    await try_to_send_it(message, config.HELP_MESSAGE)

# Улавливает команду /random_cutenes, отправляет случайное фото из массива config.PICTURES_ARRAY
@dispatcher.message_handler(commands=['random_cutenes'])
async def command_random_cuteness(message: types.Message):
    new_picture = config.PICTURES_ARRAY[randint(0, len(config.PICTURES_ARRAY) - 1)]
    await try_to_send_it(message, photo_url=new_picture)
    await message.delete()

# Запуск бота
def start():
    executor.start_polling(dispatcher, skip_updates=True)