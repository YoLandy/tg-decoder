from config import FRAMERATE 
from pydub import AudioSegment
import shutil
import subprocess
import os

def get_filename(filepath):
    filename_ext = os.path.split(filepath)[-1]
    filename = os.path.splitext(filename_ext)[0]
    
    wav_filepath = os.path.join('tmp', filename + '.wav')
    
    if os.path.isfile(wav_filepath):
        os.remove(wav_filepath)
    
    return os.path.join('tmp', filename + '.wav')


def mp3_translate(filepath):
    
    wav_filepath = get_filename(filepath)
    
    sound = AudioSegment.from_mp3(filepath)
    sound.export(wav_filepath, format="wav")
    
    return wav_filepath
    
def mp4_translate(filepath):
    wav_filepath = get_filename(filepath)
    
    subprocess.run(
        ['ffmpeg', '-i', filepath, '-acodec', 'pcm_s16le', '-ar', '16000', wav_filepath]
    )
    return wav_filepath
    
    
def copy(filepath):
    wav_filepath = get_filename(filepath)
    shutil.copy(filepath, wav_filepath)
    return wav_filepath

translators = {
    '.mp3': mp3_translate,
    '.wav': copy,
    '.mp4': mp4_translate
}    
