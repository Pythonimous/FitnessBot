import vkapi
from settings import token
import db

def ul(user_id):
    a = db.list_all()
    if a: # если есть студенты
        lst = ';\n'.join([', '.join(i) for i in a])
    else:
        lst = 'Пока студентов нет.'
    vkapi.send_message(user_id, token, lst, '')

keys = ['список', 'люди']
description = 'Покажу существующих людей.'