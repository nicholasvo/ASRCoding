import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav

# Function to record audio
def record_audio(duration = 10, samplerate = 16000, filename='recorded_audio'):
    print("Recording for 10 seconds...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    print("Recording finished.")
    wav.write(filename, samplerate, recording)  # Save as WAV file

