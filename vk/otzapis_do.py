import vkapi
from settings import token
import db

def unenrol(user_id, lst):
    user_timetable_list = [db.get_lesson(lesson_id) for lesson_id in db.user_lessons(user_id)]
    train_id = lst[0]
    if len(lst) != 1:
        message = 'Неверный формат, попробуйте ещё раз.'
    elif not user_timetable_list:
        message = 'Вы пока не записаны ни на одно занятие!'
    else:
        db.del_from_lesson(train_id, user_id)
        message = 'Сделано!'
    vkapi.send_message(user_id, token, message, '')

keys = ['отзапись']