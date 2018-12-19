import newtrain, timetable, delete, reset, student, student_del, userslist, id, zapis, otzapis, mylist
import vkapi
from settings import token

def info(user_id):
    message = ''
    message += timetable.keys[0] + ' - ' + timetable.description + '\n'
    message += userslist.keys[0] + ' - ' + userslist.description + '\n'
    message += student.keys[0] + ' - ' + student.description + '\n'
    message += student_del.keys[0] + ' - ' + student_del.description + '\n'
    message += zapis.keys[0] + ' - ' + zapis.description + '\n'
    message += otzapis.keys[0] + ' - ' + otzapis.description + '\n'
    message += mylist.keys[0] + ' - ' + mylist.description + '\n'
    message += newtrain.keys[0] + ' - ' + newtrain.description + '\n'
    message += delete.keys[0] + ' - ' + delete.description + '\n'
    message += reset.keys[0] + ' - ' + reset.description + '\n'
    message += id.keys[0] + ' - ' + id.description + '\n'
    vkapi.send_message(user_id, token, message, '')


keys = ['уберпомощь']