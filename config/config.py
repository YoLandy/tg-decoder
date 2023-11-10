import os
from config.utils.ConfigExceptions import VarNotFoundException
from config.utils.load_env import load_env

load_env()

try:
    DIARIZATION_ACCESS_TOKEN = os.environ['DIARIZATION_ACCESS_TOKEN']
except KeyError as e:
    raise VarNotFoundException('DIARIZATION_ACCESS_TOKEN')

try:
    TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
except Exception as e:
    raise VarNotFoundException('TELEGRAM_TOKEN')

FRAMERATE = 16000

CUDA = True
MODEL_TYPE = 'large'

POSSIBLE_TYPES = ['video', 'audio', 'document']
POSSIBLE_EXTENTIONS = ['mp4', 'mp3', 'wav', 'ogg']


DOWNLOAD_FOLDER = os.path.abspath('data/files/downloads')
TMP_FOLDER = os.path.abspath('data/files/tmp')

UNSUPPORTED_TYPE_MESSAGE = f'Извините, но бот принимает только {" .".join(POSSIBLE_EXTENTIONS)} файлы'
DOWNLOAD_FILE_MESSAGE= 'Загружаем данные на сервер'
START_MESSAGE = "Это транскрибатор бот. Отправь файл .mp3, .mp4 или .wav не больше 20мб и я его транскрибирую. Ты можешь оказаться в очереди на транскрибацию, тогда этот процесс займет некоторое время. Наберись терпения и дождись результата"
QUEUE_MESSAGE = lambda queue_num: f'Перед вами в очереди {queue_num} человек'
SETUP_DIARIZATOR_MESSAGE = 'Загружаем для разбиения по спикерам'
RUN_DIARIZATOR_MESSAGE = 'Запускаем разбиение по спикерам'

DONE_MESSAGE = 'Готово'
RUN_WAV_SPLITTER_MESSAGE = 'Обрабатываем файл для транскрибации'
START_TRANSCRIBATION_MESSAGE = 'Начинаем транскрибацию'
TRANSCRIBATION_PROGRESS_MESSAGE = lambda x: f'Транскрибировано примерно {x}%'