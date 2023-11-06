import os

FRAMERATE = 16000
DIARIZATION_ACCESS_TOKEN = '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'
CUDA = True
MODEL_TYPE = 'large'

POSSIBLE_TYPES = ['video', 'audio', 'document']
POSSIBLE_EXTENTIONS = ['mp4', 'mp3', 'wav']


DOWNLOAD_FOLDER = os.path.abspath('downloads')

TELEGRAM_TOKEN = '6611573360:AAEq0QhjF_OuBCCM5H3qAiif0ox7XCcgmxo'
UNSUPPORTED_TYPE_MESSAGE = f'Извините, но бот принимает только {" .".join(POSSIBLE_EXTENTIONS)} файлы'
DOWNLOAD_FILE_MESSAGE= 'Загружаем данные на сервер'