import pytest


# TODO: Use mock network services
def test_gbfs_client():
    from gbfs.client import GBFSClient

    c = GBFSClient('https://api-core.bikeshare.ae/gbfs/gbfs.json', 'en')
    assert c.feeds
    assert c.feed_names
    assert c.request_feed('station_status')