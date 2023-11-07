from flask import Flask, request
from utils.tg_requests import send_message, get_file, get_file_id
from utils.setups import setup_tg
from utils.file_funcs import save_file
from utils.ext_translation import translators
from utils.diarization import Diarizator
from utils.wav_splitter import WavSplitter
from utils.whisper_short import Whisper_short
from config import UNSUPPORTED_TYPE_MESSAGE, DOWNLOAD_FILE_MESSAGE
import os

model = Whisper_short()

class Worker():
    def __init__(self, request_json):
        self.chat_id = request_json["message"]["chat"]["id"]
        print(self.chat_id)
        self.request_json = request_json

    def render(self):
        filepath = self.download_file()          
        if not filepath:
            return False
        
        filepath = self.to_wav_file(filepath)

        data = self.diarization(filepath)
        print('diarization')
        data = self.split_wav_file(filepath, data)
        print('transcribe')
        self.transcribe(data)

    def download_file(self):
        file_id = get_file_id(self.request_json)
        print('file_id', file_id)

        if not file_id:
            self.send_message(UNSUPPORTED_TYPE_MESSAGE)
            return False
        
        self.send_message(DOWNLOAD_FILE_MESSAGE)
        print('downloading')
        resp, filename = get_file(file_id)       
        filepath = save_file(resp, filename)

        return filepath

    def to_wav_file(self, filepath):
        self.send_message('Преобразуем файл')
        print('to_wav')
        file_ext = os.path.splitext(filepath)[-1]
        filepath = translators[file_ext](filepath)
        return filepath

    def diarization(self, filepath):
        self.send_message('Загружаем для разбиения по спикерам') 

        diarizator = Diarizator(filepath)
        self.send_message('Запускаем разбиение по спикерам') 

        data = diarizator.render()
        return data
    
    def split_wav_file(self, filepath, data):
        self.send_message('В процессе разбиение по спикерам')

        wav_splitter = WavSplitter(filepath)

        self.send_message('Разбиваем по спикерам')

        data = wav_splitter.render(data)
        return data

    def transcribe(self, data):
        self.send_message('Начинаем транскрибацию')

        text = []
        for i, [filepath, speaker] in enumerate(data):
            self.send_message(f'Транскрибировано примерно {int(100 * i / len(data))}%')
            text.append((model(filepath), speaker))

        self.send_message('Готово')
        self.send_message(str(text))


    def send_message(self, text):
        send_message(self.chat_id, text)

'''
print(request.json)
chat_id = request.json["message"]["chat"]["id"]
print(chat_id)
file_id = get_file_id(request.json)
print(file_id)

if not file_id:
    send_message(chat_id, UNSUPPORTED_TYPE_MESSAGE)

print('1')    

print('1') 
send_message(chat_id, DOWNLOAD_FILE_MESSAGE)

resp, filename = get_file(file_id)        

filepath = save_file(resp, filename)

print(filepath)

send_message(chat_id, 'Преобразуем файл')
        
file_ext = os.path.splitext(filepath)[-1]
filepath = translators[file_ext](filepath)

send_message(chat_id, 'Загружаем для разбиения по спикерам') 

diarizator = Diarizator(filepath)

send_message(chat_id, 'Запускаем разбиение по спикерам') 

data = diarizator.render()

send_message(chat_id, 'В процессе разбиение по спикерам')

wav_splitter = WavSplitter(filepath)

send_message(chat_id, 'Разбиваем по спикерам')

data = wav_splitter.render(data)

send_message(chat_id, 'Начинаем транскрибацию')

text = []
for i, [filepath, speaker] in enumerate(data):
    send_message(chat_id, f'Транскрибировано примерно {int(100 * i / len(data))}')
    text.append((short_model(filepath), speaker))

send_message(chat_id, 'Готово')
send_message(chat_id, str(text))
'''