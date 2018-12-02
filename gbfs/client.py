import requests


class GBFSClient(object):
    _requests_module = None

    def __init__(self, url, language):
        assert self._requests_module

        r = self._requests_module.get(url)
        
        data = r.json().get('data')
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

        r = self._requests_module.get(url)

        return r.json()

GBFSClient._requests_module = requests