from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # Xác thực OAuth
    return GoogleDrive(gauth)

def fetch_files_from_drive(folder_url):
    """
    Lấy danh sách file trong Google Drive folder.
    """
    folder_id = folder_url.split("/")[-1]
    drive = authenticate_drive()
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    files = []
    for file in file_list:
        files.append({
            "id": file['id'],
            "title": file['title'],
            "mimeType": file['mimeType']
        })
    return files

def download_file_content(file_id):
    """
    Tải nội dung file từ Google Drive.
    """
    drive = authenticate_drive()
    file = drive.CreateFile({'id': file_id})
    return file.GetContentString()
