import os


import pytest


def test_system_discovery_service():
    from gbfs.const import package_tests_fixtures_dirpath
    from gbfs.providers import systems_provider_local_csv
    from gbfs.services import SystemDiscoveryService
    from gbfs.data.fetchers import LocalJSONFetcher

    ds = SystemDiscoveryService(systems_provider=systems_provider_local_csv)

    assert ds.systems
    assert ds.system_ids
    assert len(ds.systems) == len(ds.system_ids)
    assert ds.get_system_by_id('ABU')
    assert ds._instantiate_client(os.path.join(package_tests_fixtures_dirpath, 'gbfs.json'), 'en',
                                  json_fetcher=LocalJSONFetcher())
