import config
import asyncio
import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, message, LabeledPrice, PreCheckoutQuery, ContentTypes
from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import onstart
import sql

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token=config.Token)#, storage=MemoryStorage())

#loop = asyncio.get_event_loop()
storage=MemoryStorage()

# Диспетчер
dp = Dispatcher(bot, storage=storage)

db = sql.sql_start()
#_________________________Состояния_____________

class Master (StatesGroup):
    name = State()
    usluga = State()
    usluga_time = State()
    cost = State()
    buffer_time = State()
    group = State()

class Scheduler (StatesGroup):
    week_day = State()
    time_start = State()
    time_end = State()
#_________________________Keyboars______________
rasp_kb = InlineKeyboardMarkup(row_width=1)
rasp_btn_1 = InlineKeyboardButton(text='Повторяющееся', callback_data='rasp_1')
rasp_btn_2 = InlineKeyboardButton(text='Разовое', callback_data='rasp_2')
rasp_kb.add(rasp_btn_1).add(rasp_btn_2)

week_kb = InlineKeyboardMarkup(row_width=1)
week_btn_mon = InlineKeyboardButton(text='Понедельник', callback_data='Pn')
week_btn_tue = InlineKeyboardButton(text='Вторник', callback_data='Wt')
week_btn_wed = InlineKeyboardButton(text='Среда', callback_data='Sr')
week_btn_Tru = InlineKeyboardButton(text='Черверг', callback_data='Ch')
week_btn_fri = InlineKeyboardButton(text='Пятница', callback_data='Pt')
week_btn_sat = InlineKeyboardButton(text='Суббота', callback_data='Sb')
week_btn_sun = InlineKeyboardButton(text='Воскресенье', callback_data='VS')
week_kb.add(week_btn_mon)\
    .add(week_btn_tue).add(week_btn_wed).add(week_btn_Tru).add(week_btn_fri).add(week_btn_sat).add(week_btn_sun)
#_________________________Команды_______________

# Хэндлер на команду /start
@dp.message_handler(commands=['start', 'help'])
async def cmd_start(message: types.Message):
    await bot.send_message(731620137, text='Пользователь : '+str(message.from_user.id)+' подключился')

# Хэндлер на команду /master
@dp.message_handler(commands=['master'])
async def cmd_add_mater(message: types.Message):
    await bot.send_message(message.from_user.id, text='Если вы хотите добавить нового пользователя Мастер\nВведите свое Имя')
    await Master.name.set()

async def get_master_name(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    name = message.text
    await state.update_data(name=name)
    await Master.next()
    await bot.send_message(chat_id, 'Введите завание выполняемой услуги : ')

async def get_usluga(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    usluga = message.text
    await state.update_data(usluga=usluga)
    await Master.next()
    await bot.send_message(chat_id, 'Введите время в минутах затрачиваемое на услугу  : ')

async def get_usluga_time(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    usluga_time = message.text
    await state.update_data(usluga_time=usluga_time)
    await Master.next()
    await bot.send_message(chat_id, 'Введите стоимость услуги : ')

async def get_cost(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    cost = message.text
    await state.update_data(cost=cost)
    await Master.next()
    await bot.send_message(chat_id, 'Введите время в минутах \nза сколько можно отказаться от услусги : ')


async def get_buffer_time(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    buffer_time = message.text
    await state.update_data(buffer_time=buffer_time)
    await Master.next()
    await bot.send_message(chat_id, text='Введите группу :')

async def get_master_group(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    group = message.text
    master_dict = await state.get_data("name")
    sql.insert_into_users(db, master_dict, str(group))
    await bot.send_message(chat_id, text='Успешно добавлен новый мастер')
    await bot.send_message(chat_id, text=sql.get_master(db, str(master_dict['name'])))
    await state.finish()

@dp.message_handler(commands=['rasp'])
async def cmd_add_schedule(message: types.Message):
    await bot.send_message(message.from_user.id, text='Выберите тип расписания', reply_markup=rasp_kb)

@dp.callback_query_handler(lambda cdq: cdq.data == 'rasp_1')
async def rasp_1(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id, text='Выберите дни недели : ', reply_markup=week_kb)


@dp.callback_query_handler(lambda cdq: cdq.data == 'rasp_2')
async def rasp_2(callback_query: types.CallbackQuery):
    chat_id = callback_query.message.chat.id
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id, text='Что бы добавить новое расписание'
                                         '\nВведите первые две буквы'
                                         '\nдня недели пн, вт, ср, чт, пт, сб, вс : ')
    await Scheduler.week_day.set()

async def get_week_day(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    week_day = message.text
    await state.update_data(week_day=week_day)
    await Scheduler.next()
    await bot.send_message(chat_id, text='Введите время начала работы в формате чч:мм :')

async def get_start_time(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    time_start = message.text
    await state.update_data(time_start=time_start)
    await Scheduler.next()
    await bot.send_message(chat_id, text='Введите время окночания работы в формате чч:мм :')

async def get_end_time(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    time_end = message.text
    await state.update_data(time_end=time_end)
    rasp_dict = await state.get_data()
    await bot.send_message(chat_id, text='Добавлено новое расписание\n в '
                                         +str(rasp_dict['week_day'])
                                         +'\nНачало в '
                                         +str(rasp_dict['time_start'])
                                         +'\nОкончание в '
                                         +str(rasp_dict['time_end']))
    await state.finish()





#__________________________Основная часть___________________________
dp.register_message_handler(get_master_name, state=Master.name)
dp.register_message_handler(get_usluga, state=Master.usluga)
dp.register_message_handler(get_usluga_time, state=Master.usluga_time)
dp.register_message_handler(get_cost, state=Master.cost)
dp.register_message_handler(get_buffer_time, state=Master.buffer_time)
dp.register_message_handler(get_master_group, state=Master.group)
dp.register_message_handler(get_week_day, state=Scheduler.week_day)
dp.register_message_handler(get_start_time, state=Scheduler.time_start)
dp.register_message_handler(get_end_time, state=Scheduler.time_end)


async def main():
    await dp.start_polling(bot)

# Главная функция действия при старте
if __name__ == '__main__':
    print(onstart.onstart_msm)
    sql.create_user_table(db)
    asyncio.run(main())
