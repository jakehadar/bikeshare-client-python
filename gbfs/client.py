import requests


class System(object):
    """Class describing a single GBFS system"""

    def __init__(self, **kwargs):
        self.country_code = kwargs.get(
            SystemsCSVFields.country_code)
        
        self.name = kwargs.get(
            SystemsCSVFields.country_code)

        self.location = kwargs.get(
            SystemsCSVFields.location)

        self.system_id = kwargs.get(
            SystemsCSVFields.system_id)

        self.url = kwargs.get(
            SystemsCSVFields.url)

        self.auto_discovery_url = kwargs.get(
            SystemsCSVFields.auto_discovery_url)


class GBFSClient(object):
    """GBFS client

    Methods
    -------
    request_feed(feed_name)
        Fetches json feed from server.
    """

    _requests_module = None

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

        r = self._requests_module.get(url)

        return r.json()

GBFSClient._requests_module = requests