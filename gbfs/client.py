import datetime
import requests


from gbfs.data.fetchers import RemoteJSONFetcher
from gbfs.const import gbfs_client_default_language


__all__ = ['GBFSClient']


class GBFSClient(object):
    _json_fetcher = RemoteJSONFetcher()
    _posix_to_datetime_func = datetime.datetime.utcfromtimestamp
    _default_language = gbfs_client_default_language

    def __init__(self, url, language=None, json_fetcher=None):
        language = language or self._default_language

        if json_fetcher:
            self._json_fetcher = json_fetcher

        assert self._json_fetcher

        r = self._json_fetcher.fetch(url)
        
        data = r.get('data')
        if data is None:
            raise Exception('GBFS missing required key path: "data"')
        
        languages = data.keys()
        if language not in languages:
            raise Exception('Language must be one of: {}'.format(','.join(languages)))

        self.language = language
        
        feeds = data[language].get('feeds')
        if feeds is None:
            raise Exception('GBFS missing required json path: "data.{}.feeds"'.format(language))

        self.auto_discovery_url = url

        self.feeds = dict(
            map(lambda feed: (feed.get('name'), feed.get('url')), feeds)
        )
        
    @property
    def feed_names(self):
        return list(self.feeds.keys())

    def request_feed(self, feed_name):
        url = self.feeds.get(feed_name)
        if url is None:
            raise Exception('Feed name must be one of: {}'.format(','.join(self.feed_names)))

        data = self._json_fetcher.fetch(url)

        last_updated = data.get('last_updated')
        if last_updated:
            data['last_updated'] = self._posix_to_datetime_func(last_updated)

        return data

    def __repr__(self):
        return "{}('{}', '{}')".format(self.__class__.__name__, self.auto_discovery_url, self.language)