import json
import requests

class GBFSClient(object):
    """GBFS client

    Attributes
    ----------
    systems_url : str
        Default url to list containing all known systems publishing GBFS feeds.
    feed_names

    Methods
    -------
    request_feed(feed_name)
        Fetches json feed from server.
    """    

    systems_url = 'https://raw.githubusercontent.com/NABSA/gbfs/master/systems.csv'

    def __init__(self, url, language):
        """Constructs a GBFSClient

        Parameters
        ----------
        url : str
            Full url path to gbfs.json (auto-discovery file) that links to other feed files.
        language : str
            The language feed was published in, (i.e "en", "fr", etc.).

        Returns
        -------
        GBFSClient
        """
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
        
    @property
    def feed_names(self):
        """Feed names available for instantiated system

        Returns
        -------
        str
        """
        return self.feeds.keys()

    def request_feed(self, feed_name):
        """Requests json feed from server

        Parameters
        ----------
        feed_name : str
            Name of feed to request

        Returns
        -------
        dict
        """
        url = self.feeds.get(feed_name)
        if url is None:
            raise Exception('Feed name must be one of: {}'.format(','.join(self.feeds.keys())))

        r = self._fetch(url)

        return r.json()

    def _fetch(self, url):
        """Fires off a GET request against url"""
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception('Request {} failed with status code: {}'.format(url, r.status_code))

        print '[GBFSClient] hit network, recieved {} bytes'.format(len(r.content))
        return r

