import os

DB = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'flask',
    'passwd': 'password',
    'db': 'flask_app'
}

# upload file save path
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

FILE_STORAGE_FOLDER = UPLOAD_FOLDER

print(UPLOAD_FOLDER)