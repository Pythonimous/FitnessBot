import vkapi
from settings import token
import db

def res(user_id):
    if db.list_timetable(): # если есть занятия
        db.reset_timetable()
        msg = 'Сделано!'
    else:
        msg = 'Пока на эту неделю не назначено ни одного занятия.'
    vkapi.send_message(user_id, token, msg, '')

keys = ['сброс', 'сбросить']
description = 'Сброшу текущее расписание.'