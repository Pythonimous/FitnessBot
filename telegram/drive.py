from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def auth():
    '''
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    '''
    gauth = GoogleAuth(settings_file='settings.yaml')
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("credentials.json")
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

gauth = auth()

drive = GoogleDrive(gauth)

# запись файла на диск
def to_drive(file):
    g_file = drive.CreateFile({'title': '{}'.format(file)})  # создаём объект с названием файла
    g_file.SetContentFile(file) # указываем, из какого файла в текущей директории тащить содержимое
    g_file.Upload()
    #print(g_file)
    print('Success!')

#to_drive('easy.py')


# чтение файла
def from_drive(file):
    files = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList() # список всех файлов в корневом каталоге
    #print(len(files))
    for g_file in files:
        #print(g_file)
        if g_file['title'] == file: # нашли наш файл
            g_file.GetContentFile(file) # перезаписываем файл данными с диска
            print('Success!')
#from_drive('easy.py')
