import yaml
import os

from unittest import TestCase

_path = os.path.dirname(__file__)


class TestConfig(TestCase):
    def test_connection_is_in_config(self):
        data = yaml.safe_load(open(os.path.join(_path, './config.yaml')))
        assert 'connection' in data.keys()

    def test_host_and_port_are_in_config(self):
        data = yaml.safe_load(open(os.path.join(_path, './config.yaml')))
        expected_host = "127.0.0.1"
        expected_port = 8080
        assert data["connection"]["host"] == expected_host
        assert data["connection"]["port"] == expected_port
