from model import *
from audio import *
import time
import json
import jiwer

def main():
    asrCodingModel = ASRCodingModel()

    # Read JSON data from a file
    with open('labels.json', 'r') as file:
        dataset = json.load(file)

    raw_predictions = []
    smooth_predictions = []
    refined_predictions = []
    gold_labels = []

    # Iterate through data and transcribe
    for data in dataset:
        audio_path = './audio_files/' + data['filename']
        
        raw_transcription, smooth_transcription, output = asrCodingModel.transcribe_test(audio=audio_path)

        gold_labels.append(data['transcription'])
        raw_predictions.append(raw_transcription)
        smooth_predictions.append(smooth_transcription)
        refined_predictions.append(output.refinedTranscript)

    # Word error rates
    raw_wer = jiwer.wer(gold_labels, raw_predictions)
    smooth_wer = jiwer.wer(gold_labels, smooth_predictions)
    refined_wer = jiwer.wer(gold_labels, refined_predictions)

    print(raw_wer, smooth_wer, refined_wer)

    # Task completion / recognized command


    

if __name__ == '__main__':
    main()