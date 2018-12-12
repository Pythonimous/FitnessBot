import vkapi
from settings import token
import db

def dele(user_id, lst):

    if len(lst) != 1:
        message1 = 'Неверный формат, попробуйте ещё раз.'
    else:
        message1 = 'Удалено!'
        db.del_lesson(int(lst[0]))
        vkapi.send_message(user_id, token, message1, '')

keys = ['удалить', 'удаление']