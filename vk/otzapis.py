import vkapi
from settings import token

def otzap(user_id):
    message = 'Отзапишу с занятия.\nВведите запрос следующего вида: отзапись, id занятия.\nНапример: "отзапись, 10".\nId занятия можно увидеть командой "расписание" (первая цифра).'
    vkapi.send_message(user_id, token, message, '')

keys = ['отзаписаться']
description = 'Отзапишу с занятия.'