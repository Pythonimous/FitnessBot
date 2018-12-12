import vkapi
from settings import token
import db

def check(user_id):
    timetable_list = db.list_timetable()
    lessons = '*Расписание:*'
    if timetable_list: # если есть занятия
        for les in timetable_list: # добавляем строчки с уроками
            lesson = '\n{}: {}, {} {}. Осталось мест: {}'.format(les[4], les[0].capitalize(), les[1], les[2], les[3])
            #print(lesson)
            lessons += lesson
    else:
        lessons = 'Пока на эту неделю не назначено ни одного занятия.'
    vkapi.send_message(user_id, token, lessons, '')

keys = ['расписание']
description = 'Покажу расписание на неделю.'