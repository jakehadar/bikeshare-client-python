import csv
import requests

class StringEnum:
    country_code       = 'Country Code'
    name               = 'Name'
    location           = 'Location'
    system_id          = 'System ID'
    url                = 'URL'
    auto_discovery_url = 'Auto-Discovery URL'

class System(object):
    """Class describing a single GBFS system"""

    def __init__(self, **kwargs):
        self.country_code = kwargs.get(
            StringEnum.country_code)
        
        self.name = kwargs.get(
            StringEnum.country_code)

        self.location = kwargs.get(
            StringEnum.location)

        self.system_id = kwargs.get(
            StringEnum.system_id)

        self.url = kwargs.get(
            StringEnum.url)

        self.auto_discovery_url = kwargs.get(
            StringEnum.auto_discovery_url)
 
class ClientBase(object):
    """GBFS client base class"""

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

class DiscoveryService(ClientBase):
    """GBFS client discovery service 

    Attributes
    ----------
    systems_url : str
        Url to systems.csv file containing all known systems publishing GBFS feeds.
    """
    _systems_url = 'https://raw.githubusercontent.com/NABSA/gbfs/master/systems.csv'
    _default_language = 'en'
    _client_cls = GBFSClient

    def __init__(self):
        self.systems = {}

        request = self._fetch(self._systems_url)
        if request.status_code == 200:
            reader = csv.DictReader(request.iter_lines())
            self.systems = {}
            for kwargs in reader:
                system = System(**kwargs)
                self.systems[system.system_id] = system

    @property
    def system_ids(self):
        if len(self.systems) > 0:
            return self.systems.keys()

    def system_information(self, system_id):
        system = self.systems.get(system_id)
        if system is not None:
            return system.__dict__

    def instantiate_client(self, system_id, language=None):
        return DiscoveryService._client_cls(
            self.systems[system_id].auto_discovery_url,
            language if language else DiscoveryService._default_language,
        )
    
 
