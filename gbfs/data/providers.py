import csv
import datetime

import csv23
import six
import abc

@six.add_metaclass(abc.ABCMeta)
class DataProvider(object):
    @abc.abstractmethod
    def get_all(self):
        pass


class SystemDataProvider(DataProvider):
    _csv_dict_reader = csv23.DictReader

    def __init__(self, file_fetcher, csv_url):
        self._file_fetcher = file_fetcher
        self._csv_url = csv_url
        assert self._csv_dict_reader

    def get_all(self):
        data = self._file_fetcher.fetch(self._csv_url)
        reader = self._csv_dict_reader(data)
        for item in reader:
            yield dict(item)


class StationDataProvider(DataProvider):
    _posix_to_datetime_func = datetime.datetime.utcfromtimestamp

    def __init__(self, json_fetcher, json_url):
        self._json_fetcher = json_fetcher
        self._json_url = json_url

    def get_all(self, json_url):
        data = self._json_fetcher.fetch(self._json_url)

        last_updated = data.get('last_updated')
        if last_updated:
            data['last_updated'] = self._posix_to_datetime_func(last_updated)

        return data
