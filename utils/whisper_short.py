#!/usr/bin/env python
# coding: utf-8

import torch
import whisper
<<<<<<< Updated upstream
from config import CUDA
=======
#from config import CUDA

CUDA = False
>>>>>>> Stashed changes

class Whisper_short():
    def __init__(self):
        self.device = torch.device("cuda" if CUDA else "cpu")
        self.model = whisper.load_model("tiny", device=self.device)
        self.model.to(self.device)

    def __call__(self, audio_path, speakers=False):

        with torch.no_grad():
            preds = self.model.transcribe(audio_path)

        return preds['text']
<<<<<<< Updated upstream
=======


if __name__ == '__main__':
    filenames_speakers = [(r'C:\\Users\\koval\\OneDrive\\Документы\\GitHub\\tg-decoder\\tmp\\file_46\\0.wav', 'SPEAKER_01'), (r'C:\\Users\\koval\\OneDrive\\Документы\\GitHub\\tg-decoder\\tmp\\file_46\\1.wav', 'SPEAKER_00'), (r'C:\\Users\\koval\\OneDrive\\Документы\\GitHub\\tg-decoder\\tmp\\file_46\\2.wav', 'SPEAKER_01'), (r'C:\\Users\\koval\\OneDrive\\Документы\\GitHub\\tg-decoder\\tmp\\file_46\\3.wav', 'SPEAKER_00')]
    
    short_model = Whisper_short()
    
    for filepath, speaker in filenames_speakers:
        print(short_model(filepath), speaker)
>>>>>>> Stashed changes
