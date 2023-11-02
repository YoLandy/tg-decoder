#!/usr/bin/env python
# coding: utf-8

import torch
import whisper
from scipy.io.wavfile import read
from config import CUDA

class Whisper_short():
    def __init__(self):
        self.device = torch.device("cuda" if CUDA else "cpu")
        self.model = whisper.load_model("large", device=self.device)
        self.model.to(self.device)

    def __call__(self, audio_path, speakers=False):

        with torch.no_grad():
            preds = self.model.transcribe(audio_path)

        return preds['text']


if __name__ == '__main__':
    filenames_speakers = [('C:\\Users\\Reny\\Desktop\\decoder\\tmp\\Сцена в баре\\0.wav', 'SPEAKER_00'), ('C:\\Users\\Reny\\Desktop\\decoder\\tmp\\Сцена в баре\\1.wav', 'SPEAKER_01'), ('C:\\Users\\Reny\\Desktop\\decoder\\tmp\\Сцена в баре\\2.wav', 'SPEAKER_00'), ('C:\\Users\\Reny\\Desktop\\decoder\\tmp\\Сцена в баре\\3.wav', 'SPEAKER_01'), ('C:\\Users\\Reny\\Desktop\\decoder\\tmp\\Сцена в баре\\4.wav', 'SPEAKER_00'), ('C:\\Users\\Reny\\Desktop\\decoder\\tmp\\Сцена в баре\\5.wav', 'SPEAKER_01'), ('C:\\Users\\Reny\\Desktop\\decoder\\tmp\\Сцена в баре\\6.wav', 'SPEAKER_00'), ('C:\\Users\\Reny\\Desktop\\decoder\\tmp\\Сцена в баре\\7.wav', 'SPEAKER_01'), ('C:\\Users\\Reny\\Desktop\\decoder\\tmp\\Сцена в баре\\8.wav', 'SPEAKER_00'), ('C:\\Users\\Reny\\Desktop\\decoder\\tmp\\Сцена в баре\\9.wav', 'SPEAKER_01'), ('C:\\Users\\Reny\\Desktop\\decoder\\tmp\\Сцена в баре\\10.wav', 'SPEAKER_00')]
    
    short_model = Whisper_short()
    
    for filepath, speaker in filenames_speakers:
        print(short_model(filepath), speaker)