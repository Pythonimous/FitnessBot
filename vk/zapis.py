import vkapi
from settings import token

def zap(user_id):
    message = 'Запишу на занятие.\nВведите запрос следующего вида: запись, id занятия.\nНапример: "запись, 10".\nId занятия можно увидеть командой "расписание" (первая цифра).'
    vkapi.send_message(user_id, token, message, '')

keys = ['записаться']
description = 'Запишу на занятие.'