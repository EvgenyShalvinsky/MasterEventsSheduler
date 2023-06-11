import config
import asyncio
import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, message, LabeledPrice, PreCheckoutQuery, ContentTypes
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import onstart
import admsql

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token=config.Token)#, storage=MemoryStorage())

#loop = asyncio.get_event_loop()
storage=MemoryStorage()

# Диспетчер
dp = Dispatcher(bot, storage=storage)

db = admsql.sql_start()


class GetEvent (StatesGroup):
    event_name = State()
    description = State()
    event_day = State()
    event_time = State()
    user_count = State()
    price = State()


@dp.message_handler(commands=['start', 'help'])
async def cmd_start(message: types.Message):
    await bot.send_message(731620137, text='Пользователь : '+str(message.from_user.id)+' подключился')
    await bot.send_message(message.from_user.id, text='Введите команду \n /new_event - добавить событие')



# Хэндлер на команду /new_event ожидается имя пользоалеля
@dp.message_handler(commands=['new_event'])
async def cmd_add_event(message: types.Message):
    await bot.send_message(message.from_user.id, text='Если вы хотите добавить новое Мероприятие\nВведите его Название')
    await GetEvent.event_name.set()
# Хэндлер на команду /new_event ожидается обработка названия, запрос описания
async def get_event_name(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    event_name = message.text
    await state.update_data(event_name=event_name)
    await GetEvent.next()
    await bot.send_message(chat_id, 'Введите описание мероприятия : ')
# Хэндлер на команду /new_event ожидается обработка описания , запрос даты
async def get_description(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    description = message.text
    await state.update_data(description=description)
    await GetEvent.next()
    await bot.send_message(chat_id, 'Введите дату мероприятия в формате гггг-мм-дд : ')
# Хэндлер на команду /new_event ожидается дата, запрос времени
async def get_event_day(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    event_day = message.text
    await state.update_data(event_day=event_day)
    await GetEvent.next()
    await bot.send_message(chat_id, 'Введите время начала мероприятия в формате ЧЧ:ММ : ')
# Хэндлер на команду /new_event ожидается дата, запрос времени
async def get_event_time(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    event_time = message.text
    await state.update_data(event_time=event_time)
    await GetEvent.next()
    await bot.send_message(chat_id, 'Введите количество участников : ')
# Хэндлер на команду /new_event ожидается дата, запрос времени
async def get_user_count(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    user_count = message.text
    await state.update_data(user_count=user_count)
    await GetEvent.next()
    await bot.send_message(chat_id, 'Введите цену участия мероприятия :')
# Хэндлер на команду /new_event ожидается дата, запрос времени
async def get_price(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    price = message.text
    await state.update_data(price=price)
    event_dict = await state.get_data()
    admsql.insert_into_event(db, event_dict)
    await bot.send_message(chat_id, text='Добавлено новое Cобытие'
                                         '\n'+str(event_dict['event_name'])
                                         +'\nДата : '+str(event_dict['event_day'])
                                         +'\nНачало в '
                                         +str(event_dict['event_time'])
                                         +'\nОписание :\n'
                                         +str(event_dict['description'])
                                         +'\nЦена : '+str(event_dict['price'])
                                         +'\nДоступно мест : '+str(event_dict['user_count']))
    await state.finish()
# Хэндлер на команду /event пользователю выводится список мероприятий
@dp.message_handler(commands=['event'])
async def cmd_show_event(message: types.Message):
    events = admsql.get_event_names(db)
    print(events)
    for event_name in list(events):
        description = admsql.get_description_by_name(db, str(event_name[0]))
        event_day = admsql.get_event_day_by_name(db, str(event_name[0]))
        event_time = admsql.get_event_time_by_name(db, str(event_name[0]))
        price = admsql.get_price_by_name(db, str(event_name[0]))
        user_count = admsql.get_user_count_by_name(db, str(event_name[0]))
        await bot.send_message(message.from_user.id, text=str(event_name[0])+'\nОписание :\n'
                                                          +str(description)
                                                          +'\n'+str(event_day)
                                                          +'\nв '+str(event_time)
                                                          +'\nЦена :'+str(price)
                                                          +'\nКоличество мест : '+str(user_count))
        event_name=+1




dp.register_message_handler(get_event_name, state=GetEvent.event_name)
dp.register_message_handler(get_description, state=GetEvent.description)
dp.register_message_handler(get_event_day, state=GetEvent.event_day)
dp.register_message_handler(get_event_time, state=GetEvent.event_time)
dp.register_message_handler(get_price, state=GetEvent.price)
dp.register_message_handler(get_user_count, state=GetEvent.user_count)


async def main():

    await dp.start_polling(bot)



if __name__ == '__main__':
    print(onstart.onstart_msm)
    admsql.create_event_table(db)
    asyncio.run(main())


