from unittest import TestCase

import pycld2 as cld2


class TestLanguage(TestCase):
    def test_english_is_recognised(self):
        _, _, details = cld2.detect("Hello, would you like some tea?")
        expected = "ENGLISH"
        assert details[0][0] == expected

    def test_not_english(self):
        _, _, details = cld2.detect("Salve, vuole una pizza?")
        expected = "ITALIAN"
        assert details[0][0] == expected

    def test_not_english2(self):
        _, _, details = cld2.detect("Hej, vill du ha lite palt")
        expected = "SWEDISH"
        assert details[0][0] == expected
