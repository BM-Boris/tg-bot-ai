from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from oauth2client.service_account import ServiceAccountCredentials
import config


def drive_auth(left_json):

    gauth = GoogleAuth()
    scope = ["https://www.googleapis.com/auth/drive"]
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_dict(left_json, scope)
    drive = GoogleDrive(gauth)

    return drive

gdrive = drive_auth(config.left_json)


def update_personality(username, personality, gdrive = gdrive):

    drive = gdrive
    
    folderId = 'folder_id'
    
    file_list = drive.ListFile({'q': f"'{folderId}' in parents and trashed=false"}).GetList()
    file_id = None
    
    for file in file_list:
        if(file['title'] == username+'_config.txt'):
            file_id = file['id']
            file_user = drive.CreateFile({'id': file_id,
                             'parents': [{'id': folderId}]})

            content = file_user.GetContentString()
            file_user.SetContentString(personality)
            file_user.Upload()

            break
            

    if(file_id == None):
        file_user = drive.CreateFile({'title': username+'_config.txt',
                             'parents': [{'id': folderId}]})
        file_user.SetContentString(personality)
        file_user.Upload()

def remember_personality(username, personality, gdrive = gdrive):

    drive = gdrive
    
    folderId = 'folder_id'
    
    file_list = drive.ListFile({'q': f"'{folderId}' in parents and trashed=false"}).GetList()
    file_id = None
    
    for file in file_list:
        if(file['title'] == username+'_config.txt'):
            file_id = file['id']
            file_user = drive.CreateFile({'id': file_id,
                             'parents': [{'id': folderId}]})

            content = file_user.GetContentString()
            
            return content

    if(file_id == None):
        file_user = drive.CreateFile({'title': username+'_config.txt',
                             'parents': [{'id': folderId}]})
        file_user.SetContentString(personality)
        file_user.Upload()



def personalities(gdrive = gdrive):
    
    drive = gdrive
    
    folderId = 'folder_id'
    
    file_list = drive.ListFile({'q': f"'{folderId}' in parents and trashed=false"}).GetList()
    file_id = None
    
    for file in file_list:
        if(file['title'] == 'personalities.txt'):
            file_id = file['id']
            file_user = drive.CreateFile({'id': file_id,
                             'parents': [{'id': folderId}]})

            content = file_user.GetContentString()
            return content

    if(file_id == None):
        file_user = drive.CreateFile({'title': 'personalities.txt',
                             'parents': [{'id': folderId}]})
        file_user.SetContentString(str([{'Your Roles'}]))
        file_user.Upload()

persona = eval(personalities())