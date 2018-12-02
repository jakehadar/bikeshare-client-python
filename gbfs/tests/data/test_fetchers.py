import pytest


# Mock network classes

class dummy_requests_module:
    def __init__(self, response):
        self._response = response
    def get(self, *args, **kwargs):
        return self._response


class dummy_response_200:
    status_code = 200
    def iter_lines(self, *args, **kwargs):
        yield 'Country Code,Name,Location,System ID,URL,Auto-Discovery URL'
        yield 'AE,ADCB Bikeshare,"Abu Dhabi, AE",ABU,https://www.bikeshare.ae/,https://api-core.bikeshare.ae/gbfs/gbfs.json'


class dummy_response_404:
    status_code = 404
    def iter_lines(self, *ars, **kwargs):
        yield '404: Not Found'


def test_local_file_fetcher():
    from gbfs.const import gbfs_systems_csv_local_filepath
    from gbfs.data.fetchers import LocalFileFetcher

    fetcher = LocalFileFetcher()

    assert fetcher.fetch(gbfs_systems_csv_local_filepath)


def test_remote_file_fetcher_400():
    from gbfs.const import gbfs_systems_csv_remote_url
    from gbfs.data.fetchers import RemoteFileFetcher

    RemoteFileFetcher._requests_module = dummy_requests_module(dummy_response_200())

    fetcher = RemoteFileFetcher()

    assert fetcher.fetch(gbfs_systems_csv_remote_url)


def test_remote_file_fetcher_404():
    from gbfs.const import gbfs_systems_csv_remote_url
    from gbfs.data.fetchers import RemoteFileFetcher

    RemoteFileFetcher._requests_module = dummy_requests_module(dummy_response_404())

    fetcher = RemoteFileFetcher()

    with pytest.raises(RuntimeError):
        fetcher.fetch(gbfs_systems_csv_remote_url)