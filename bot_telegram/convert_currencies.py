import requests

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types

from .keyboards import keyboard_convert_step_1, keyboard_convert_step_2, keyboard_client

# Ключ API для конвертации
API_KEY = '6wM6hi6LPdzTLAogKxhKOu6UDVAgmlLw'

class FSM(StatesGroup):
    value = State()
    count = State()

# Улавливает только команду /convert_currencies при пустом состоянии
async def start_mode(message:  types.Message):
    await FSM.value.set()
    await message.answer('Выберите в какую валюту будем переводить или напишите идентификатор из 3-х букв', reply_markup=keyboard_convert_step_1)

# Улавливает состояние FSM.value
async def value_command(message:  types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['value'] = message.text
    await FSM.next()
    await message.answer('Какое кол-во рублей конвертировать?', reply_markup=keyboard_convert_step_2)

# Улавливает состояние FSM.count
async def count_command(message:  types.Message, state: FSMContext):
    service_message = await message.answer('Запрос принят, ожидайте ответ', reply_markup=keyboard_client)
    async with state.proxy() as data:
        message_answer = 'После перевода получим:\n\n' + await get_converted_currency(
            message.text, data['value']) + ' ' +data['value']
    await message.reply(message_answer, reply_markup=keyboard_client)
    await state.finish()
    await service_message.delete()

# Принимает количесвто и идентификатор валюты, в которую переводим рубли.
# Возвращает результат конвертации в строчном формате,
# если запрос не удался, возвращает текст о неудачном подключении
async def get_converted_currency(ammount: str, currency: str = 'USD') -> str:
    url = "https://api.apilayer.com/exchangerates_data/convert?to=%s&from=RUB&amount=%s" % (currency, ammount)
    answer = 'Сервис в данный момент не доступен'

    payload = {}
    headers= {
      "apikey": "6wM6hi6LPdzTLAogKxhKOu6UDVAgmlLw"
    }
    try:
        response = requests.request("GET", url, headers=headers, data = payload)
    except:
        return answer
    else:
        result = response.json()
        try:
            current = result['result']
        except:
            return '*Ошибка при конвертации в'
        return str(current)

def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start_mode, commands=['convert_currencies'], state=None)
    dispatcher.register_message_handler(value_command, state=FSM.value)
    dispatcher.register_message_handler(count_command, state=FSM.count)
