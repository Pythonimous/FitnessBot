from flask import Flask, request, json
from settings import confirmation_token, token
import info, newtrain, newtrain_do, timetable, delete, delete_do, reset, student, student_do, student_del, userslist, id, id_do
import mylist, zapis, zapis_do, otzapis, otzapis_do, uberinfo

from get_json import admin as ad
import vkapi

app = Flask(__name__)

@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':

        user_id = data['object']['user_id']

        text = (data['object']['body']).lower().split(', ')

        def otkaz():
            message = 'И как ты, товарищ, забрал(ся/лась) сюда?\nЭтого же в помощи нет!\nНу, ты не преподаватель, так что низя :)'
            vkapi.send_message(user_id, token, message, '')

        admin = ad(user_id, data)

        if len(text) == 1:
            key = text[0]

            if key in newtrain.keys:
                if admin:
                    newtrain.new(user_id)
                else:
                    otkaz()

            elif key in info.keys:
                info.info(user_id, admin)
            elif key in timetable.keys:
                timetable.check(user_id)
            elif key in delete.keys:
                if admin:
                    delete.desc(user_id)
                else:
                    otkaz()

            elif key in reset.keys:
                if admin:
                    reset.res(user_id)
                else:
                    otkaz()

            elif key in student.keys:
                student.new(user_id)
            elif key in student_del.keys:
                student_del.new(user_id)
            elif key in userslist.keys:
                userslist.ul(user_id)
            elif key in zapis.keys:
                zapis.zap(user_id)
            elif key in otzapis.keys:
                otzapis.otzap(user_id)
            elif key in mylist.keys:
                mylist.inform(user_id)
            elif key in id.keys:
                if admin:
                    id.id(user_id)
                else:
                    otkaz()
            elif key in uberinfo.keys:
                if admin:
                    uberinfo.info(user_id)
                else:
                    otkaz()
            else:
                info.idk(user_id)

        elif len(text) > 1:
            if text[0] in newtrain_do.keys:
                if admin:
                    newtrain_do.new(user_id, text[1:])
                else:
                    otkaz()
            elif text[0] in delete_do.keys:
                if admin:
                    delete_do.dele(user_id, text[1:])
                else:
                    otkaz()
            elif text[0] in student_do.keys:
                student_do.new(user_id, text[1:])
            elif text[0] in zapis_do.keys:
                zapis_do.enrol(user_id, text[1:])
            elif text[0] in otzapis_do.keys:
                otzapis_do.unenrol(user_id, text[1:])
            elif text[0] in id_do.keys:
                if admin:
                    id_do.id(user_id, text[1:])
                else:
                    otkaz()
            else:
                info.idk(user_id)

        return 'ok'