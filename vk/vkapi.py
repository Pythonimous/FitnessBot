import vk
from settings import token

#google часть

session = vk.Session(access_token = token)
api = vk.API(session, v=5.50)


def send_message(user_id, token, message, attachment=""):
    api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment=attachment)