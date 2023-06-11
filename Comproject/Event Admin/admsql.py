import sqlite3
import config
from sqlite3 import Error

import onstart


def sql_start():
    try:
        global base  # Объевление базы и курсора
        base = sqlite3.connect(config.LOTO_BASE_PATH)
        print('__________НАЙДЕНА БАЗА ДАННЫХ________\n master.db STATUS : CONNECTED')
        return base
    except Error:
        print(Error)

def create_event_table(base):
    try:
        base.cursor().execute('''CREATE TABLE IF NOT EXISTS event(event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                  Event_name TEXT, 
                                                                  Description TEXT, 
                                                                  Date TEXT,
                                                                  Time TEXT, 
                                                                  User_count TEXT,
                                                                  Price TEXT)'''
                              )
        base.commit()
        print('__________СОЗДАНА ТAБЛИЦА events______________\n master.db STATUS : OK')
    except Error:
        print(Error)
        print('Ошибка создания таблицы users')

def insert_into_event(base, event_dict):
    event = str(event_dict['event_name'])
    description = str(event_dict['description'])
    day = str(event_dict['event_day'])
    time = str(event_dict['event_time'])
    price = str(event_dict['price'])
    user_count = str(event_dict['user_count'])
    base.cursor().execute('''INSERT INTO event(Event_name, 
                                               Description, 
                                               Date, 
                                               Time, 
                                               User_count,
                                               Price) 
                                               VALUES(?, ?, ?, ?, ?, ?)''',
                          (event, description, day, time, price, user_count))
    base.commit()
    print(onstart.get_date()+' Добвленно новое событие')

def get_event_names(base):
    event_names = base.cursor().execute('''SELECT Event_name FROM event''').fetchall()
    return event_names

def get_description_by_name(base, event_name):
    descripton = base.cursor().execute('''SELECT Description FROM event WHERE Event_name = ?''', [event_name]).fetchone()
    return descripton[0]

def get_event_day_by_name(base, event_name):
    event_day = base.cursor().execute('''SELECT Date FROM event WHERE Event_name = ?''', [event_name]).fetchone()
    return event_day[0]

def get_event_time_by_name(base, event_name):
    event_time = base.cursor().execute('''SELECT Time FROM event WHERE Event_name = ?''', [event_name]).fetchone()
    return event_time[0]

def get_price_by_name(base, event_name):
    price = base.cursor().execute('''SELECT Price FROM event WHERE Event_name = ?''', [event_name]).fetchone()
    return price[0]

def get_user_count_by_name(base, event_name):
    user_count = base.cursor().execute('''SELECT User_count FROM event WHERE Event_name = ?''', [event_name]).fetchone()
    return user_count[0]