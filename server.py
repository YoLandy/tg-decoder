from flask import Flask, request
from utils.tg_requests import send_message, get_file, get_file_id
from utils.setups import setup_tg
from utils.file_funcs import save_file
from utils.ext_translation import translators
from utils.diarization import Diarizator
from utils.wav_splitter import WavSplitter
from utils.whisper_short import Whisper_short
import os

from config import UNSUPPORTED_TYPE_MESSAGE, DOWNLOAD_FILE_MESSAGE

app = Flask(__name__)

short_model = Whisper_short()

@app.route("/", methods=["GET", "POST"])
def receive_update():
    if request.method == "POST":
        print(request.json)
        chat_id = request.json["message"]["chat"]["id"]
        print(chat_id)
        file_id = get_file_id(request.json)
        print(file_id)
        
        if not file_id:
            send_message(chat_id, UNSUPPORTED_TYPE_MESSAGE)
            return {"ok": True}
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
        
    return {"ok": True}
    

if __name__ == '__main__':
    setup_tg()
    app.run(debug=True)