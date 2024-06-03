from model import *
from audio import *

def main():
    asrCodingModel = ASRCodingModel()

    filename='recorded_audio'

    audio = record_audio(filename=filename)
    transcription = asrCodingModel.transcribe(filename)

    print(transcription)


if __name__ == '__main__':
    main()