import vkapi
from settings import token
import db

def new(user_id, lst):

    if len(lst) != 3:
        message1 = 'Неверные данные, попробуйте ещё раз.'
    else:
        message1 = 'Внесено!\nВаш ID: ' + str(user_id)
        db.add_student(user_id, lst[0], lst[1], lst[2])
        vkapi.send_message(user_id, token, message1, '')

keys = ['всписок', 'внестись']