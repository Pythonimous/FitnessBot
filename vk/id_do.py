import vkapi
from settings import token
import db

def id(user_id, lst):
    train_id = lst[0]
    if len(lst) != 1:
        user_list = 'Неверный формат, попробуйте ещё раз.'
    else:
        lesson = db.get_lesson(train_id)
        user_ids = db.list_lesson(train_id)
        users = db.list_them(user_ids)
        if users:
            user_list = ''
            for i, user in enumerate(users):
                user_list+='`{}) {} {}, {}`\n'.format(i+1, user[0], user[1], user[2])
            user_list+='`\nОсталось мест: {}`'.format(lesson[4])
            print(user_list)
        else:
            user_list = 'На занятие пока никто не записан.'
    vkapi.send_message(user_id, token, user_list, '')

keys = ['спсзан']