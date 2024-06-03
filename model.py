import whisper
import nltk
from chain import *

vocab = ["move", "turn", "left", "pick", "beeper", "put", "underscore", "for", "range", "front", "clear", "present", "bag", "in", "beepers", "blocked", "if", "while", "indent", "return"]

class ASRCodingModel():
    def __init__(self, model_type = "base.en"):
        self.model = whisper.load_model(model_type)
        self.llm = LLMChain()
        self.vocab = vocab

    def remove_punctuation(self, text: str):
        words = nltk.word_tokenize(text)
        words = [word for word in words if word.isalnum()]
        
        return words

    def smooth_levenshtein(self, raw_transcription: str, error_threshold = 1):
        smoothed_transcription = ""

        # Remove any punctuation and return as list of words
        words_no_punct = self.remove_punctuation(raw_transcription)

        # Iterate through words and smooth if necessary, else append original word
        for word in words_no_punct:

            word = word.lower()
            best_match = None
            best_score = float('inf')

            for vocab_word in self.vocab:
                distance = nltk.edit_distance(vocab_word, word)
                if distance < best_score:
                    best_score = distance
                    best_match = vocab_word

            if best_score <= error_threshold:
                smoothed_transcription += " " + best_match
            else:
                smoothed_transcription += " " + word

        return smoothed_transcription


    def transcribe(self, audio):

        # Get Raw Transcription
        raw_transcription = self.model.transcribe(audio)['text']

        # Smooth transcription
        smooth_transcription = self.smooth_levenshtein(raw_transcription, 1)

        # Filter response type
        output = self.llm.structured_llm_call(smooth_transcription)

        if output.isValid == False:
            return False, output.errorMessage
        else:
            return True, '\n'.join(output.commandList)