from detoxify import Detoxify


class ToxicityDetector:
    def __init__(self, model_name, toxic_threshold=0.5):
        self._model = Detoxify(model_name)
        self._toxic_threshold = toxic_threshold

    def is_toxic(self, utterance):
        results = self._model.predict(utterance)
        return results["toxicity"] > self._toxic_threshold
