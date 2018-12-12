import vkapi
import db
from settings import token

def new(user_id):
    db.del_user(user_id)
    message = 'Вы удалены!'
    vkapi.send_message(user_id, token, message, '')

keys = ['удалиться']
description = 'удалю вас из списка'