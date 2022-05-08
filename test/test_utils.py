from unittest import TestCase

from src.utils import query_refers_to_prior_dialogue


class TestUtils(TestCase):
    def test_yours_triggerprior_dialogue_activation(self):
        predicted = query_refers_to_prior_dialogue("what is yours")
        expected = True
        assert predicted == expected
