from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

button_weather = KeyboardButton('/weather')
button_convert_currencies = KeyboardButton('/convert_currencies')
button_random_cuteness = KeyboardButton('/random_cutenes')

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_client.add(button_weather).add(button_convert_currencies).add(button_random_cuteness)
