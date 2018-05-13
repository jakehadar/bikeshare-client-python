import json
import csv
import requests

class ClientBase(object):
    """GBFS client base class

    Attributes
    ----------
    systems_url : str
        Url to systems.csv file containing all known systems publishing GBFS feeds.
    """
    systems_url = 'https://raw.githubusercontent.com/NABSA/gbfs/master/systems.csv'

    def __init__(self):
        request = self._fetch(self.systems_url)

        if request.status_code == 200:
            reader = csv.DictReader(request.iter_lines())
            self.systems = {}
            for d in reader:
                system_id, url = d['System ID'], d['Auto-Discovery URL']
                self.systems[system_id] = url

    @property
    def system_names(self):
        if len(self.systems) > 0:
            return self.systems.keys()
        
    @staticmethod
    def _fetch(url):
        """Fires off a GET request against url"""
        r = requests.get(url)
        return r

class GBFSClient(ClientBase):
    """GBFS client

    Methods
    -------
    request_feed(feed_name)
        Fetches json feed from server.
    """    

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
        super(GBFSClient, self).__init__()

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


