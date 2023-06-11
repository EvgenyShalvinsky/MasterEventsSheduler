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


def create_user_table(base):
    try:
        base.cursor().execute('''CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                  Имя_мастера TEXT, 
                                                                  Услуга TEXT, 
                                                                  Время TEXT, 
                                                                  Стоимость TEXT,
                                                                  Буферное_время TEXT,
                                                                  Группа TEXT)'''
                              )
        base.commit()
        print('__________СОЗДАНА ТAБЛИЦА users______________\n master.db STATUS : OK')
    except Error:
        print(Error)
        print('Ошибка создания таблицы users')
    # finally:
    # base.close()


def insert_into_users(base, master_dict, group):
    #try:
    name = master_dict['name']
    usluga = master_dict['usluga']
    time = master_dict['usluga_time']
    cost = master_dict['cost']
    buffertime = master_dict['buffer_time']
    print(group)
    base.cursor().execute('''INSERT INTO users (Имя_мастера, 
                                                Услуга, 
                                                Время, 
                                                Стоимость,
                                                Буферное_время,
                                                Группа) VALUES (?, ?, ?, ?, ?, ?)''',
                          (name, usluga, time, cost, buffertime, group))
    base.commit()

    #except Error:
    #    print(Error)
    #    print('Ошибка добавления : '+name+' '+usluga+' '+time+' '+cost+' '+buffertime+' '+group)


def get_master(base, name):
    try:
        print(onstart.get_date()+'___Запрос инфо о мастере______________\n master.db STATUS : OK')
        master_usluga = base.cursor().execute('''SELECT * FROM users WHERE Имя_мастера = ?''', [name]).fetchone()
        return master_usluga
    except Error:
        print(onstart.get_date() + ' Ошибка выдачи информации о мастере')

def create_master_scheduler(base):
    try:
        print('__________СОЗДАНА ТАБЛИЦА scheduler______________\n scheduler.db STATUS : OK')
        base.cursor().execute(
            '''CREATE TABLE IF NOT EXISTS scheduler
            (
            schedule_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            Usluga TEXT,
            WeekDay TEXT, 
            Тimestart TEXT,
            Тimeend TEXT,

            )'''
        )
        base.commit()
    except Error:
        print(Error)
        print('Ошибка создания таблицы master')
    # finally:
    # base.close()
