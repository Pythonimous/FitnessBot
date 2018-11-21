import vk
import random
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from settings import credentials

session = vk.Session()
api = vk.API(session, v=5.50)


def send_message(user_id, token, message, attachment=""):
    api.messages.send(access_token=token, user_id=str(user_id), message=message, attachment=attachment)

def get_random_wall_picture(group_id, token):
    max_num = api.photos.get(owner_id=group_id, album_id='wall', count=0, access_token=token)['count']
    num = random.randint(1, max_num)
    photo = api.photos.get(owner_id=str(group_id), album_id='wall', count=1, offset=num, access_token=token)['items'][0]['id']
    attachment = 'photo' + str(group_id) + '_' + str(photo)
    return attachment

#google часть

def auth():
    gauth = GoogleAuth(settings_file='settings.yaml')
    # Try to load saved client credentials
    gauth.LoadCredentialsFile(credentials)
    if gauth.credentials is None:
    # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
    # Refresh them if expired
        gauth.Refresh()
    else:
    # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("credentials.json")

    return gauth

drive = GoogleDrive(auth())

def to_drive(file):
    g_file = drive.CreateFile({'title': '{}'.format(file)})  # создаём объект с названием файла
    g_file.SetContentFile(file) # указываем, из какого файла в текущей директории тащить содержимое
    g_file.Upload()
    #print(g_file)
    print('Success!')

def from_drive(file):
    files = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList() # список всех файлов в корневом каталоге
    #print(len(files))
    for g_file in files:
        #print(g_file)
        if g_file['title'] == file: # нашли наш файл
            g_file.GetContentFile(file) # перезаписываем файл данными с диска
            print('Success!')

