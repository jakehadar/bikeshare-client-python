from gbfs.providers import systems_provider_remote_csv
from gbfs.client import GBFSClient
from gbfs.const import gbfs_systems_csv_fields


__all__ = ['SystemDiscoveryService']


class SystemDiscoveryService(object):
    """GBFS client discovery service"""

    _default_language = 'en'
    _client_cls = None
    _systems_provider = None
    _system_attrs = None

    def __init__(self, run_on_init=True, systems_provider=None):
        if systems_provider:
            self._systems_provider = systems_provider

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
    def systems(self):
        return list(self._systems_cache.values())

    @property
    def system_ids(self):
        if self._systems_cache:
            return list(self._systems_cache.keys())

    def get_system_by_id(self, system_id):
        return self._systems_cache.get(system_id)

    def instantiate_client(self, system_id, language=None):
        system = self._systems_cache.get(system_id)
        if system:
            system_url = system.get(self._system_attrs.auto_discovery_url)
            if system_url:
                return self._instantiate_client(system_url, language if language else self._default_language)

    def _instantiate_client(self, system_url, language, json_fetcher=None):
        return self._client_cls(system_url, language, json_fetcher=json_fetcher)

# Runtime config
SystemDiscoveryService._system_attrs = gbfs_systems_csv_fields
SystemDiscoveryService._client_cls = GBFSClient
SystemDiscoveryService._systems_provider = systems_provider_remote_csv
