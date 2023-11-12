from src.downloader.downloader import Downloader
from src.waver.waver import Waver
from src.diarizator.diarizator import Diarizator
from src.wav_splitter.wav_splitter import WavSplitter
from src.combiner.combiner import Combiner
from src.summarizer.summarizer import Summarizer
from src.utils.tg_requests import send_message, send_document
from src.utils.file_funcs import save_to_txt

from config.config import DOWNLOAD_FILE_MESSAGE, START_TRANSCRIBATION_MESSAGE, \
                          SETUP_DIARIZATOR_MESSAGE, RUN_DIARIZATOR_MESSAGE, \
                          TRANSCRIBATION_PROGRESS_MESSAGE, DONE_MESSAGE, \
                          RUN_WAV_SPLITTER_MESSAGE

import os

class Worker():
    def __init__(self, task, model):
        self.file_id = task['file_id']
        self.ext = task['ext']
        self.chat_id = task['chat_id']
        self.lock = task['lock']
        self.is_running = False

        self.model = model
        self.downloader = Downloader(self.file_id)
        self.waver = Waver(self.ext)

    def run(self):
        self.is_running = True
        filepath = self.download()
        filepath = self.to_wav(filepath)
        
        self.lock.acquire()
        
        timeslices_by_speaker = self.diarization(filepath)
        text_with_time = self.transcribe(filepath)
        combined_text = self.combine(timeslices_by_speaker, text_with_time)
        
        self.lock.release()

        text = '\n'.join([f'{speaker} : {replic}' for (replic, speaker) in combined_text])
        self.send_text(filepath, text, summary=False)

        self.lock.acquire()
        summarized_text = self.summarize(combined_text)
        self.lock.release()
        print(summarized_text)
        self.send_text(filepath, summarized_text, summary=True)

        self.is_running = False

    def summarize(self, combined_text):
        summarizer = Summarizer(combined_text)
        summary = summarizer.summarize()
        return summary

    def combine(self, diarization, text_with_time):
        combiner = Combiner(diarization, text_with_time)
        combined_text = combiner.combine()
        return combined_text

    def download(self):
        send_message(self.chat_id, DOWNLOAD_FILE_MESSAGE)
        return self.downloader.download_file()
    
    def diarization(self, filepath):
        send_message(self.chat_id, SETUP_DIARIZATOR_MESSAGE)
        diarizator = Diarizator(filepath)

        send_message(self.chat_id, RUN_DIARIZATOR_MESSAGE)
        timeslices_by_speaker = diarizator.render()
        return timeslices_by_speaker

    def to_wav(self, filepath):
        return self.waver.to_wav(filepath)

    def split_wav(self, timeslices_by_speaker, filepath):
        wav_splitter = WavSplitter(filepath)
        send_message(self.chat_id, RUN_WAV_SPLITTER_MESSAGE)
        filepaths_speakers = wav_splitter.render(timeslices_by_speaker)
        return filepaths_speakers

    def transcribe(self, filepath):
        send_message(self.chat_id, START_TRANSCRIBATION_MESSAGE)
        text_with_time = self.model(filepath, self.chat_id)
        send_message(self.chat_id, DONE_MESSAGE)
        return text_with_time

    def send_text(self, filepath, text, summary=False):
        dir, filename = os.path.split(filepath)
        filename, ext = os.path.splitext(filename)
        if summary:
            filename += '_summary'
        filename += '.txt'

        send_document(save_to_txt(text, filename), self.chat_id)
