import pycld2 as cld2


class LanguageDetector:
    def __init__(self):
        self._model = cld2

    def is_english(self, utterance):
        if len(utterance.split()) <= 1:
            return True

        _, _, details = cld2.detect(utterance)

        if details[0][0].lower() == "unknown":
            return True

        if any(item[0].lower() == "english" for item in details):
            return True

        return False
