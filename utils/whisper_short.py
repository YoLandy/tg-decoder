#!/usr/bin/env python
# coding: utf-8

import torch
import whisper
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
