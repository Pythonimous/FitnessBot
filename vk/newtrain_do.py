import vkapi
from settings import token
import db

def new(user_id, lst):

    if len(lst) != 4:
        message1 = 'Неверный формат расписания, попробуйте ещё раз.'
    else:
        message1 = 'Внесено!'
        db.add_lesson(lst[0], lst[1], lst[2], lst[3])
        vkapi.send_message(user_id, token, message1, '')

keys = ['создать', 'занятие']