import requests


from gbfs.data.fetchers import RemoteJSONFetcher, LocalJSONFetcher


__all__ = ['GBFSClient']


class GBFSClient(object):
    _json_fetcher = None

    def __init__(self, url, language):
        assert self._json_fetcher

        r = self._json_fetcher.fetch(url)
        
        data = r.get('data')
        if data is None:
            raise Exception('GBFS missing required key path: "data"')
        
        languages = data.keys()
        if language not in languages:
            raise Exception('Language must be one of: {}'.format(','.join(languages)))
        
        feeds = data[language].get('feeds')
        if feeds is None:
            raise Exception('GBFS missing required key path: "data.{}.feeds"'.format(language))

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

        return self._json_fetcher.fetch(url)

GBFSClient._json_fetcher = RemoteJSONFetcher()