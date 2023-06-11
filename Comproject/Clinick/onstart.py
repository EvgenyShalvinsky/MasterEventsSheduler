import datetime

def get_date():
    today = datetime.datetime.now()
    now = today.strftime("%Y-%m-%d %H:%M:%S")
    return now

onstart_msm = get_date()+' Бот запущен '