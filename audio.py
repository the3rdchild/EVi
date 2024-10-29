import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import time

THRESHOLD_DB = 10  # dB threshold
SAMPLERATE = 44100  # sampling rate
DURATION = 5  # duration of recording in seconds

def db_level(audio_data):
    rms = np.sqrt(np.mean(audio_data**2))
    db = 20 * np.log10(rms) if rms > 0 else -np.inf
    return db

def record_audio():
    print("Recording...")
    audio_data = sd.rec(int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=1)
    sd.wait()
    timestamp = int(time.time())
    wav.write(f'recorded_{timestamp}.wav', SAMPLERATE, audio_data)
    print(f"Saved as recorded_{timestamp}.wav")

def main():
    #monitor audio level
    with sd.InputStream(samplerate=SAMPLERATE, channels=1, callback=None):
        print("Chill, bro is listening...")
        while True:
            audio_data = sd.rec(int(0.5 * SAMPLERATE), samplerate=SAMPLERATE, channels=1)
            sd.wait()
            audio_data = np.squeeze(audio_data)
            
            if db_level(audio_data) >= THRESHOLD_DB:
                record_audio()
            else:
                print("Sound below threshold")

if __name__ == "__main__":
    main()
