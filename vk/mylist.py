import vkapi
from settings import token
import db

def inform(user_id):
    user_tt_list = [db.get_lesson(lesson_id) for lesson_id in db.user_lessons(user_id)]
    lessons = 'Мои занятия:'
    if user_tt_list:
        for les in user_tt_list: # добавляем строчки с занятиями
            lesson = '`\n— {}, {} {}`'.format(les[0].capitalize(), les[1], les[2])
            lessons = lessons+lesson
    else:
        lessons = 'Пока что вы не записаны ни на одно занятие.'
    vkapi.send_message(user_id, token, lessons, '')

keys = ['моизанятия']
description = 'Скажу, на какие занятия вы записаны.'