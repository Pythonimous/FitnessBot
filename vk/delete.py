import vkapi
from settings import token

def desc(user_id):
    message = 'Удалю занятие по ID.\nВведите ID группы (число перед двоеточием у соответствующего занятия в "расписании".\nНапример: "удалить, 38"'
    vkapi.send_message(user_id, token, message, '')

keys = ['удалить']
description = 'Удалю занятие по ID'