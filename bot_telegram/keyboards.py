from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

# Общее клавиатуры

button_weather = KeyboardButton('/weather')
button_convert_currencies = KeyboardButton('/convert_currencies')
button_random_cuteness = KeyboardButton('/random_cutenes')
button_create_poll = KeyboardButton('/create_poll')

keyboard_client = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_client.add(button_weather).add(button_convert_currencies).add(button_random_cuteness).add(button_create_poll)

# Погода клавиатуры

# Шаг 1
button_weather_step_1_1 = KeyboardButton('Moscow')
button_weather_step_1_2 = KeyboardButton('Saint Petersburg')
button_weather_step_1_3 = KeyboardButton('Novosibirsk')

keyboard_weather_step_1 = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_weather_step_1.add(
    button_weather_step_1_1).add(button_weather_step_1_2).add(button_weather_step_1_3)

# Конвертация клавиатуры

# Шаг 1
button_convert_step_1_1 = KeyboardButton('USD')
button_convert_step_1_2 = KeyboardButton('EUR')
button_convert_step_1_3 = KeyboardButton('KZT')

keyboard_convert_step_1 = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_convert_step_1.row(
    button_convert_step_1_1, button_convert_step_1_2, button_convert_step_1_3)

# Шаг 2
button_convert_step_2_1 = KeyboardButton('100')
button_convert_step_2_2 = KeyboardButton('1000')
button_convert_step_2_3 = KeyboardButton('10000')

keyboard_convert_step_2 = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_convert_step_2.row(
    button_convert_step_2_1, button_convert_step_2_2, button_convert_step_2_3)

# Опросы клавиатура

button_poll_cancel = KeyboardButton('/cancel')

# Клавиатура с кнопкой /cancel
keyboard_polls = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_polls.add(button_poll_cancel)

button_poll_finish = KeyboardButton('/finish')

# Клавиатура с кнопкой /cancel и /finish
keyboard_polls_finish = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_polls_finish.add(button_poll_finish).add(button_poll_cancel)