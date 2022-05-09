import pycld2 as cld2


class LanguageDetector:
    def __init__(self):
        self._model = cld2

    def is_english(self, utterance):
        _, _, details = cld2.detect(utterance)
        if details[0][0].lower() in ["english", "unknown"]:
            return True

        return False
