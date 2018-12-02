import abc
import requests
import json


class FileFetcher(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def fetch(url):
        pass


class LocalCSVFetcher(FileFetcher):
    def fetch(self, url):
        with open(url, 'r') as f:
            data = f.readlines()
        return data


class RemoteCSVFetcher(FileFetcher):
    _requests_module = None

    def __init__(self, requests_module=None):
        if requests_module:
            assert hasattr(requests_module, 'get')
            self._requests_module = requests_module

        assert self._requests_module

    def fetch(self, url):
        response = self._requests_module.get(url)
        if response.status_code != 200:
            raise RuntimeError('HTTPS request for {} failed with status code {}' \
                               .format(url, response.status_code))
        return list(response.iter_lines(decode_unicode=True))

RemoteCSVFetcher._requests_module = requests


class LocalJSONFetcher(FileFetcher):
    _json_module = None

    def __init__(self):
        assert self._json_module

    def fetch(self, url):
        with open(url, 'r') as f:
            data = self._json_module.load(f)
        return data

LocalJSONFetcher._json_module = json


class RemoteJSONFetcher(FileFetcher):
    _requests_module = None

    def __init__(self):
        assert self._requests_module

    def fetch(self, url):
        response = self._requests_module.get(url)
        if response.status_code != 200:
            raise RuntimeError('HTTPS request for {} failed with status code {}' \
                               .format(url, response.status_code))
        return response.json()

RemoteJSONFetcher._requests_module = requests