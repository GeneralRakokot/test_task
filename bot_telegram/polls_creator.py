from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Dispatcher, types

from .keyboards import keyboard_polls, keyboard_polls_finish, keyboard_client

class FSM(StatesGroup):
    question = State()
    first_option = State()
    second_option = State()
    other_option = State()

# Улавливает только команду /create_poll при пустом состоянии
async def start_mode(message:  types.Message, state : FSMContext):
    await FSM.question.set()
    # В памяти создаем ссылки на массивы 'options' - варианты ответов в опросе
    # и 'service' - сервисные сообщения создания опроса, которые будут удалены
    async with state.proxy() as data:
        data['options'] = []
        data['service'] = []
        data['service'].append(
            await message.answer('Введите текст вопроса', reply_markup=keyboard_polls))
    await message.delete()
    await FSM.next()

# Улавливает состояние FSM.first_option
async def add_poll_first_option(message: types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['question'] = message.text
        data['service'].append(message)
        data['service'].append(
            await message.answer('Введите первый вариант ответа'))
    await FSM.next()

# Улавливает состояние FSM.second_option
async def add_poll_second_option(message: types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['options'].append(message.text)
        data['service'].append(message)
        data['service'].append(
            await message.answer('Введите второй вариант ответа'))
    await FSM.next()

# Улавливает состояние FSM.other_option
async def add_poll_other_option(message: types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['options'].append(message.text)
        data['service'].append(message)
        data['service'].append(
            await message.answer('Введите еще один вариант ответа или завершите создание', reply_markup=keyboard_polls_finish))

# Улавливает команду '/finish'. Завершает создание опроса и удаляет сервисные сообщения
async def finish_mode(message: types.Message, state : FSMContext):
    async with state.proxy() as data:
        await create_poll(message, data['question'], data['options'])
        await service_clear(data['service'])
    await state.finish()
    await message.delete()

# Улавливает команду '/cancel'. Отменяет создание опроса и удаляет сервисные сообщения
async def on_cancel(message: types.Message, state : FSMContext):
    async with state.proxy() as data:
        await service_clear(data['service'])
    await state.finish()
    await message.answer('Опрос отменен', reply_markup=keyboard_client)
    await message.delete()

# Принимает сообщение полбзователя для дальнейшего ответа в тот же чат, вопрос, варианты ответа
# Ничего не возвращает, пытается отправить в чат созданный опрос,
# при неудаче отправляет сообщение об ошибке
async def create_poll(message: types.Message, question: str, options: list):
    try:
        await message.answer_poll(question=question, options=options,
            is_anonymous=False, reply_markup=keyboard_client)
    except:
        await message.answer('Опрос отменен из-за некорректного заполнения', reply_markup=keyboard_client)

# Принимает массив сервисных сообщений, удаляет сервисные сообщения
async def service_clear(service_messages_array: list):
    for message in service_messages_array:
        await message.delete()

def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(start_mode, commands=['create_poll'], state=None)
    dispatcher.register_message_handler(finish_mode, commands=['finish'], state=FSM.other_option)
    dispatcher.register_message_handler(on_cancel, commands=['cancel'], state=FSM.question)
    dispatcher.register_message_handler(on_cancel, commands=['cancel'], state=FSM.first_option)
    dispatcher.register_message_handler(on_cancel, commands=['cancel'], state=FSM.second_option)
    dispatcher.register_message_handler(on_cancel, commands=['cancel'], state=FSM.other_option)
    dispatcher.register_message_handler(add_poll_first_option, state=FSM.first_option)
    dispatcher.register_message_handler(add_poll_second_option, state=FSM.second_option)
    dispatcher.register_message_handler(add_poll_other_option, state=FSM.other_option)




