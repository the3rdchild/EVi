import os
import sys
import sounddevice as sd
import numpy as np
import time
from scipy.io.wavfile import write
import importlib.util

rec_dir = os.path.dirname(os.path.abspath(__file__))
EVi = os.path.join(rec_dir, '..')
sys.path.append(EVi)

from path import dbmeter, save_path

spec = importlib.util.spec_from_file_location("k", dbmeter)
db_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db_module)

sampling_rate = 44100
record_duration = 5 

def record_audio(filename, duration, rate):
    print("Recording started...")
    recording = sd.rec(int(duration * rate), samplerate=rate, channels=1, dtype='int16')
    sd.wait() 
    write(filename, rate, recording) 
    print(f"Recording saved as {filename}")

while True:
    db = float(db_module.db)  # Convert db to float
    if db > 65.00:  # Check if db is above threshold
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = os.path.join(save_path, f"recording_{timestamp}.wav")
        record_audio(filename, record_duration, sampling_rate)
        
    time.sleep(1) 