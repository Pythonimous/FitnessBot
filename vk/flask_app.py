from flask import Flask, request, json
from settings import confirmation_token
import info, newtrain, newtrain_do, timetable, delete, delete_do, reset, student, student_do, student_del

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
        if len(text) == 1:
            key = text[0]
            if key in newtrain.keys:
                newtrain.new(user_id)
            elif key in info.keys:
                info.info(user_id)
            elif key in timetable.keys:
                timetable.check(user_id)
            elif key in delete.keys:
                delete.desc(user_id)
            elif key in reset.keys:
                reset.res(user_id)
            elif key in student.keys:
                student.new(user_id)
            elif key in student_del.keys:
                student_del.new(user_id)

        elif len(text) > 1:
            if text[0] in newtrain_do.keys:
                newtrain_do.new(user_id, text[1:])
            elif text[0] in delete_do.keys:
                delete_do.dele(user_id, text[1:])
            elif text[0] in student_do.keys:
                student_do.new(user_id, text[1:])
        else:
            info.idk(user_id)

        return 'ok'