import pytest


def test_system_discovery_service():
    from gbfs.providers import systems_provider_local_csv
    from gbfs.services import SystemDiscoveryService

    # TODO: use mock classes for _systems_provider and _client_cls
    SystemDiscoveryService._systems_provider = systems_provider_local_csv

    ds = SystemDiscoveryService()

    assert ds.system_ids
    assert ds.system_information(ds.system_ids[0])
    assert ds.instantiate_client(ds.system_ids[0])
