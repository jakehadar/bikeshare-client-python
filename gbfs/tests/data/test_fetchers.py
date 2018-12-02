import os

import pytest


# Mock network classes

class dummy_requests_module:
    def __init__(self, response):
        self._response = response
    def get(self, *args, **kwargs):
        return self._response


class dummy_response_csv_200:
    status_code = 200
    def iter_lines(self, *args, **kwargs):
        yield 'Country Code,Name,Location,System ID,URL,Auto-Discovery URL'
        yield 'AE,ADCB Bikeshare,"Abu Dhabi, AE",ABU,https://www.bikeshare.ae/,https://api-core.bikeshare.ae/gbfs/gbfs.json'


class dummy_response_csv_404:
    status_code = 404
    def iter_lines(self, *ars, **kwargs):
        yield '404: Not Found'


class dummy_response_json:
    status_code = 200
    def json(self):
        return {'last_updated': 1543720674, 'ttl': 10, 'data': {'en': {'feeds': [{'name': 'station_status', 'url': 'https://api-core.bikeshare.ae/gbfs/en/station_status.json'}]}}}


def test_local_csv_fetcher():
    from gbfs.const import gbfs_systems_csv_local_filepath
    from gbfs.data.fetchers import LocalCSVFetcher

    fetcher = LocalCSVFetcher()

    assert fetcher.fetch(gbfs_systems_csv_local_filepath)


def test_remote_csv_fetcher_400():
    from gbfs.const import gbfs_systems_csv_remote_url
    from gbfs.data.fetchers import RemoteCSVFetcher

    fetcher = RemoteCSVFetcher(requests_module=dummy_requests_module(dummy_response_csv_200()))

    assert fetcher.fetch(gbfs_systems_csv_remote_url)


def test_remote_csv_fetcher_404():
    from gbfs.const import gbfs_systems_csv_remote_url
    from gbfs.data.fetchers import RemoteCSVFetcher

    fetcher = RemoteCSVFetcher(requests_module=dummy_requests_module(dummy_response_csv_404()))

    with pytest.raises(RuntimeError):
        fetcher.fetch(gbfs_systems_csv_remote_url)


def test_local_json_fetcher():
    from gbfs.const import package_tests_fixtures_dirpath
    from gbfs.data.fetchers import LocalJSONFetcher

    fetcher = LocalJSONFetcher()

    assert fetcher.fetch(os.path.join(package_tests_fixtures_dirpath, 'gbfs.json'))


def test_remote_json_fetcher():
    from gbfs.data.fetchers import RemoteJSONFetcher

    fetcher = RemoteJSONFetcher(requests_module=dummy_requests_module(dummy_response_json()))

    assert fetcher.fetch('http://path/to/gbfs.json')