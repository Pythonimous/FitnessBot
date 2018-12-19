import vkapi
from settings import token

def id(user_id):
    message = 'Выведу список id студентов на занятии.\nВведите запрос следующего вида: спсзан, id занятия.\nНапример: "спсзан, 10".\nId занятия можно увидеть командой "расписание" (первая цифра).'

    vkapi.send_message(user_id, token, message, '')

keys = ['список_урока']
description = 'Покажу список студентов на занятии'