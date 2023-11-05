import os
from config import DOWNLOAD_FOLDER

def save_file(responce, file_name):
    filepath = os.path.join(DOWNLOAD_FOLDER, file_name)
    with open(filepath, 'wb') as file:
        file.write(responce.content)
    
    return filepath