import pytest

def test_client():
    from gbfs.client import GBFSClient


def test_system_discovery_service():
    from gbfs.services import SystemDiscoveryService
    ds = SystemDiscoveryService()
    assert ds.system_ids
