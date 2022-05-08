from unittest import TestCase
from detoxify import Detoxify


class TestProfanityDetector(TestCase):
    def test_threat(self):
        detox = Detoxify("original")
        results = detox.predict("I am going to murder your komodo dragon.")
        assert results["toxicity"] > 0.5
        assert results["threat"] > 0.5

        assert results["obscene"] < 0.5
        assert results["insult"] < 0.5
        assert results["severe_toxicity"] < 0.5
        assert results["identity_attack"] < 0.5

    def test_toxicity_absence(self):
        detox = Detoxify("original")
        results = detox.predict("Puppies, rainbows, and honey.")
        assert results["toxicity"] < 0.5
        assert results["threat"] < 0.5
        assert results["obscene"] < 0.5
        assert results["insult"] < 0.5
        assert results["severe_toxicity"] < 0.5
        assert results["identity_attack"] < 0.5
