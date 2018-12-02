import abc
import csv
import requests


class DataProvider(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_all(self):
        pass


class SystemDataProvider(DataProvider):
    _csv_dict_reader = csv.DictReader

    def __init__(self, file_fetcher, csv_url):
        self._file_fetcher = file_fetcher
        self._csv_url = csv_url
        assert self._csv_dict_reader

    def get_all(self):
        data = self._file_fetcher.fetch(self._csv_url)
        reader = self._csv_dict_reader(data)
        for item in reader:
            assert item.__class__.__name__ == 'OrderedDict'
            yield dict(item)


class StationDataProvider(DataProvider):
    pass
