import vkapi
from settings import token

def new(user_id):
    message = 'Добавлю вас в список.\nВведите: всписок, фамилия, имя, группа.\nНапример: "всписок, Иванов, Иван, 15БИ".'
    vkapi.send_message(user_id, token, message, '')

keys = ['внестись']
description = 'внесу вас в список'