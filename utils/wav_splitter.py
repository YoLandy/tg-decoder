import numpy as np
from pydub import AudioSegment
import os
import shutil

class WavSplitter():
    def __init__(self, audio_path):
        self.audio = AudioSegment.from_wav(audio_path)
        self.dir = self.makedir(audio_path)
    
    @staticmethod
    def makedir(filepath):
        print(filepath)
        dir_path = os.path.splitext(filepath)[0]
        dir_path = r'{}'.format(dir_path)
        
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)
            
        os.mkdir(dir_path)
        return dir_path
    
    def get_filename(self, indx):
        return os.path.join(self.dir, f'{indx}.wav')
            
    def render(self, data):
        filenames_speakers = []
        
        for id_, [[start, stop], speaker] in enumerate(data):
            start = int(start * 1000)
            stop = int(stop * 1000)
            
            chunk_path = self.get_filename(id_)
            audio_chunk = self.audio[start:stop]
            audio_chunk.export(chunk_path, format="wav")
            filenames_speakers.append((chunk_path, speaker))
        
        return filenames_speakers
    
if __name__ == '__main__':
    data = np.array(
        [
            [[1.9779286926994908, 10.466893039049237], 'SPEAKER_00'], 
            [[10.466893039049237, 33.845500848896435], 'SPEAKER_01'], 
            [[33.845500848896435, 34.60950764006791], 'SPEAKER_00'], 
            [[34.60950764006791, 37.27504244482173], 'SPEAKER_01'], 
            [[37.27504244482173, 105.88285229202037], 'SPEAKER_00'], 
            [[105.88285229202037, 110.31409168081495], 'SPEAKER_01'], 
            [[110.31409168081495, 110.43293718166385], 'SPEAKER_00'], 
            [[110.43293718166385, 111.40067911714772], 'SPEAKER_01'], 
            [[111.40067911714772, 116.08658743633276], 'SPEAKER_00'], 
            [[116.08658743633276, 123.13242784380307], 'SPEAKER_01'], 
            [[123.13242784380307, 132.52122241086587], 'SPEAKER_00']
        ], dtype=object
    )
    
    splitter = WavSplitter(r'C:\Users\Reny\Desktop\decoder\tmp\Сцена в баре.wav')
    print(splitter.render(data))
    