import vkapi
from settings import token
import db

def enrol(user_id, lst):
    open_list = db.list_open()
    timetable_list = db.list_timetable()
    train_id = lst[0]
    if len(lst) != 1:
        message = 'Неверный формат, попробуйте ещё раз.'
    elif open_list:
        db.add_to_lesson(train_id, user_id)
        message = 'Вы записались на занятие!'
    elif not timetable_list:
        message = 'Пока занятий на неделе нет.'
    else:
        message = 'К сожалению, свободных мест нет.'
    vkapi.send_message(user_id, token, message, '')

keys = ['запись']