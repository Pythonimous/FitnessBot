import vkapi
from settings import token

def new(user_id):
    message = 'Создам для вас новое занятие.\nВведите запрос следующего вида: создать, название, дата, время, размер группы.\nНапример: "создать, тренажерный зал, 12.09.18, 14:00, 30".'
    vkapi.send_message(user_id, token, message, '')

keys = ['занятие']
description = 'Создам новое занятие'