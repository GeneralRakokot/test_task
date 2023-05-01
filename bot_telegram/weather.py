import requests

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types

from .keyboards import keyboard_weather_step_1, keyboard_client

# Ключ API для сайта openweathermap
API_KEY = "4ca1e300971635777c09ef709a23276b"

class FSM(StatesGroup):
    city = State()

# Улавливает только команду /weather при пустом состоянии
async def start_mode(message:  types.Message):
    await FSM.city.set()
    await message.answer('Выбирете город', reply_markup=keyboard_weather_step_1)

# Улавливает состояние FSM.city
async def weather_command(message: types.Message, state : FSMContext):
    message_answer = 'Ну и погодка, сегодня ' + await get_weather(message.text)
    await message.reply(message_answer, reply_markup=keyboard_client)
    await state.finish()

# Принимает название города, возвращает погоду в данном регионе,
# если запрос не удался, возвращает текст о неудачном подключении
async def get_weather(city: str) -> str:
    url = "https://api.openweathermap.org/data/2.5/weather?q=%s,ru&appid=%s&lang=ru" % (city, API_KEY)
    answer = '\n\nСервис в данный момент не доступен'
    try:
        response = requests.get(url)
    except:
        return answer
    else:
        result = response.json()
        try:
            current = result['weather'][0]["description"]
        except:
            return answer
        else:
            return str(current)

def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start_mode, commands=['weather'], state=None)
    dispatcher.register_message_handler(weather_command, state=FSM.city)