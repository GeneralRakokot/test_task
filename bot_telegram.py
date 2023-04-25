import config
from aiogram import Bot, Dispatcher, executor, types
from keyboards import keyboard_client
from bot_behavior import weather, convert_currencies

bot = Bot(config.TOKEN_API)
dispatcher = Dispatcher(bot)

async def try_to_send_it(message: types.Message, answer_text: str):
    try:
        await bot.send_message(message.from_user.id, answer_text,reply_markup=keyboard_client)
    except:
        await message.answer(text=answer_text,reply_markup=keyboard_client)

@dispatcher.message_handler(commands=['start'])
async def command_start(message: types.Message):
    message_answer = config.START_MESSAGE + '\n' + config.HELP_MESSAGE
    await try_to_send_it(message, message_answer)
    await message.delete()

@dispatcher.message_handler(commands=['help'])
async def command_help(message: types.Message):
    await try_to_send_it(message, config.HELP_MESSAGE)

import random

@dispatcher.message_handler(commands=['weather'])
async def command_weather(message: types.Message):
    message_answer = 'Ну и погодка сегодня\n\n' + await weather.get_weather_temp(str(random.randint(0, 180)), str(random.randint(0, 90)))
    await try_to_send_it(message, message_answer)

@dispatcher.message_handler(commands=['convert_currencies'])
async def command_convert_currencies(message: types.Message):
    message_answer = 'Курс валют\n\n' + await convert_currencies.get_converted_currency('RUB')
    await try_to_send_it(message, message_answer)

@dispatcher.message_handler(commands=['random_cutenes'])
async def command_random_cuteness(message: types.Message):
    await try_to_send_it(message, 'Картинка')

@dispatcher.message_handler()
async def command_random_cuteness(message: types.Message):
    await try_to_send_it(message, 'Неизвестная команда')

def handlers_register(dispatcher : Dispatcher):
    dispatcher.register_message_handler(command_start, commands=['start'])
    dispatcher.register_message_handler(command_help, commands=['help'])
    dispatcher.register_message_handler(command_weather, commands=['weather'])
    dispatcher.register_message_handler(command_convert_currencies, commands=['convert_currencies'])
    dispatcher.register_message_handler(command_random_cuteness, commands=['random_cuteness'])

def start():
    executor.start_polling(dispatcher, skip_updates=True)