import os


import pytest


# TODO: Use mock network services
def test_gbfs_client():
    from gbfs.const import package_tests_fixtures_dirpath
    from gbfs.data.fetchers import LocalJSONFetcher
    from gbfs.client import GBFSClient

    c = GBFSClient(os.path.join(package_tests_fixtures_dirpath, 'gbfs.json'), 'en',
                   json_fetcher=LocalJSONFetcher())

    assert c.feeds
    assert c.feed_names
    #assert c.request_feed('station_status')