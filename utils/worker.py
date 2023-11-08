from flask import Flask, request
from utils.tg_requests import send_message, get_file, get_file_id, send_document
from utils.file_funcs import save_to_txt
from utils.file_funcs import save_file
from utils.ext_translation import translators
from utils.diarization import Diarizator
from utils.wav_splitter import WavSplitter
from utils.whisper_short import Whisper_short
from config import UNSUPPORTED_TYPE_MESSAGE, DOWNLOAD_FILE_MESSAGE, SETUP_DIARIZATOR_MESSAGE, RUN_DIARIZATOR_MESSAGE, RUN_WAV_SPLITTER_MESSAGE, START_TRANSCRIBATION_MESSAGE, TRANSCRIBATION_PROGRESS_MESSAGE, DONE_MESSAGE
import os

model = Whisper_short()

class Worker():
    def __init__(self, request_json, lock):
        self.lock = lock
        self.chat_id = request_json["message"]["chat"]["id"]
        print(self.chat_id)
        self.request_json = request_json
        self.is_running = False

    def render(self):
        try:
            self.is_running = True
            filepath = self.download_file()          
            if not filepath:
                self.is_running = False
                return False
        
            filepath = self.to_wav_file(filepath)

            data = self.diarization(filepath)
            print('diarization')
            data = self.split_wav_file(filepath, data)
            print('transcribe')

            self.lock.acquire()

            text_list = self.transcribe(data)

            self.send_txt(filepath, text_list)
            self.is_running = False

            self.lock.release()

        except Exception as e:
            self.send_message(str(e))
            self.is_running = False
            raise e

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
        self.send_message(SETUP_DIARIZATOR_MESSAGE) 

        diarizator = Diarizator(filepath)
        self.send_message(RUN_DIARIZATOR_MESSAGE) 

        data = diarizator.render()
        return data
    
    def split_wav_file(self, filepath, data):
        #self.send_message(SETUP_WAV_SPLITTER_MESSAGE)

        wav_splitter = WavSplitter(filepath)

        self.send_message(RUN_WAV_SPLITTER_MESSAGE)

        data = wav_splitter.render(data)
        return data

    def transcribe(self, data):
        self.send_message(START_TRANSCRIBATION_MESSAGE)

        text = []
        for i, [filepath, speaker] in enumerate(data):
            status_bar = 100 * i / len(data)
            self.send_message(TRANSCRIBATION_PROGRESS_MESSAGE(status_bar))
            text.append((model(filepath), speaker))

        self.send_message(DONE_MESSAGE)
        return text

    def send_txt(self, filepath, text_list):
        dir, filename = os.path.split(filepath)
        filename, ext = os.path.splitext(filename)
        filename += '.txt'

        text = '\n'.join([f'{speaker} : {replic}' for (replic, speaker) in text_list])

        send_document(save_to_txt(text, filename), self.chat_id)


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