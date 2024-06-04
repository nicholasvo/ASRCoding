from pydub import AudioSegment
import argparse

# Helper functions to convert from .mp3 to .wav
def convert_mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

def convert_mp3_to_wav(file_prefix, start_index, end_index):
    # Batch convert of mp3
    for i in range(start_index, end_index):
        mp3_path = './audio_files/' + file_prefix + str(i) + ".mp3"
        wav_path = './audio_files/' + file_prefix + str(i) + ".wav"
        convert_mp3_to_wav(mp3_path=mp3_path, wav_path=wav_path)


def main():
    parser = argparse.ArgumentParser(description="Convert MP3 to WAV")
    parser.add_argument('mp3_path', type=str, help='Path to the input MP3 file')
    parser.add_argument('wav_path', type=str, help='Path to the output WAV file')
    
    args = parser.parse_args()
    
    
    
    convert_mp3_to_wav(args.mp3_path, args.wav_path)
    

if __name__ == '__main__':
    main()
