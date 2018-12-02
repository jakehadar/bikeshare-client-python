from gbfs.providers import systems_provider_default


class SystemsCSVFields:
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
    """GBFS client discovery service"""

    _default_language = 'en'
    _client_cls = None
    _systems_provider = None
    _system_attrs = None

    def __init__(self, run_on_init=True):
        assert self._client_cls
        assert self._systems_provider
        assert self._system_attrs

        self._systems_cache = {}

        if run_on_init:
            self._get_and_cache_all_systems()

    def _get_and_cache_all_systems(self):
        try:
            systems = self._systems_provider.get_all()
        except:
            raise

        for system in systems:
            system_id = system.get(self._system_attrs.system_id)
            if system_id is None:
                raise RuntimeError('Unexpected systems data format.')
            self._systems_cache[system_id] = system


    @property
    def system_ids(self):
        if self._systems_cache:
            return list(self._systems_cache.keys())

    def system_information(self, system_id):
        return self._systems_cache.get(system_id)

    def instantiate_client(self, system_id, language=None):
        system = self._systems_cache.get(system_id)
        if system:
            system_url = system.get(self._system_attrs.auto_discovery_url)
            if system_url:
                try:
                    client = self._client_cls(system_url, language if language else self._default_language)
                except:
                    raise RuntimeError('Could not instantiate client with system url: {}'.format(system_url))
                return client

# Runtime config

DiscoveryService._system_attrs = SystemsCSVFields
DiscoveryService._client_cls = GBFSClient
DiscoveryService._systems_provider = systems_provider_default
