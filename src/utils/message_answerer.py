from src.utils.tg_parser import get_fileid_and_ext, get_text
from src.utils.tg_requests import send_message
from config.config import UNSUPPORTED_TYPE_MESSAGE, POSSIBLE_EXTENTIONS, START_MESSAGE

def answer_message(data, chat_id):
    file_id, ext = get_fileid_and_ext(data)
    
    if ext == 'txt' and get_text(data) == '/start':
        send_message(chat_id, START_MESSAGE) 
        return False, False

    if not ext or ext not in POSSIBLE_EXTENTIONS:
        send_message(chat_id, UNSUPPORTED_TYPE_MESSAGE)
        return False, False

    return file_id, ext

