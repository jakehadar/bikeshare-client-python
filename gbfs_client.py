import json
import requests

class GBFSClient(object):
    def __init__(self, url, language):
        r = self._fetch(url)
        
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
        
    def feed_names(self):
        return self.feeds.keys()

    def request_feed(self, feed_name):
        url = self.feeds.get(feed_name)
        if url is None:
            raise Exception('Feed name must be one of: {}'.format(','.join(self.feeds.keys())))

        r = self._fetch(url)

        return r.json()

    def _fetch(self, url):
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception('Request {} failed with status code: {}'.format(url, r.status_code))

        print '[GBFSClient] hit network, recieved {} bytes'.format(len(r.content))
        return r

