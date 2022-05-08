import yaml
import os

from unittest import TestCase

_path = os.path.dirname(__file__)


class TestKnowledge(TestCase):
    def test_loading_knowledge_has_keys(self):
        data = yaml.safe_load(open(os.path.join(_path, './knowledge.yaml')))
        assert 'chatbot' in data.keys()
        assert 'permanent' in data.keys()
        assert 'items' in data.keys()
        assert 'default' in data.keys()
        assert 'profanity' in data.keys()