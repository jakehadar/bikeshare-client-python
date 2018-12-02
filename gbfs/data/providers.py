import abc
import csv
import requests


class DataProvider(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_all(self):
        pass


class CSVDataProvider(DataProvider):
    _csv_dict_reader = None

    def __init__(self, file_fetcher_strategy, csv_url):
        self._csv_url = csv_url
        self._file_fetcher_strategy = file_fetcher_strategy
        assert self._csv_dict_reader

    def get_all(self):
        data = self._file_fetcher_strategy.fetch(self._csv_url)
        reader = self._csv_dict_reader(data)
        for item in reader:
            assert item.__class__.__name__ == 'OrderedDict'
            yield dict(item)
        raise StopIteration

CSVDataProvider._csv_dict_reader = csv.DictReader