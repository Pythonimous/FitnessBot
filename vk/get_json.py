from vkapi import api

def admin(user_id, data):
    user_id = data['object']['user_id']
    group_id = data['group_id']
    req = api.groups.getById(group_id = group_id, fields=['contacts'])[0]
    cts = req['contacts']
    for i in cts:
        if user_id == i['user_id']:
            flag = True
            break
        else:
            flag = False
    return flag