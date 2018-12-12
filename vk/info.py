import newtrain, timetable, delete, reset, student, student_del
import vkapi
from settings import token

def info(user_id):
    message = ''
    message += newtrain.keys[0] + ' - ' + newtrain.description + '\n'
    message += timetable.keys[0] + ' - ' + timetable.description + '\n'
    message += delete.keys[0] + ' - ' + delete.description + '\n'
    message += reset.keys[0] + ' - ' + reset.description + '\n'
    message += student.keys[0] + ' - ' + student.description + '\n'
    message += student_del.keys[0] + ' - ' + student_del.description + '\n'
    vkapi.send_message(user_id, token, message, '')

def idk(user_id):
    message = 'Не понимаю Вас. Введите "помощь", чтобы получить дополнительные команды.'
    vkapi.send_message(user_id, token, message, '')


keys = ['помощь', 'помоги', 'help']
description = 'Покажу список команд :)'