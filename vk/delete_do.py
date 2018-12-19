import vkapi
from settings import token
import db

def dele(user_id, lst):

    if len(lst) != 1:
        message = 'Неверный формат, попробуйте ещё раз.'
    else:
        message = 'Удалено!'
        ids = db.list_lesson(lst[0])
        less = db.get_lesson(lst[0])
        message1 = 'Уведомляем, что ваше занятие (' + ', '.join(less[:3]) + ') было отменено!'
        for i in ids:
            vkapi.send_message(i, token, message1, '')
        db.del_lesson(int(lst[0]))
        vkapi.send_message(user_id, token, message, '')

keys = ['удалить', 'удаление']