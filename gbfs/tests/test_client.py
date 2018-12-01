import pytest


# Mock network classes

class dummy_requests_module:
    def __init__(self, response):
        self._response = response
    def get(self, *args, **kwargs):
        return self._response


class dummy_response_200:
    status_code = 200
    def iter_lines(self, *args, **kwargs):
        yield 'Country Code,Name,Location,System ID,URL,Auto-Discovery URL'
        yield 'AE,ADCB Bikeshare,"Abu Dhabi, AE",ABU,https://www.bikeshare.ae/,https://api-core.bikeshare.ae/gbfs/gbfs.json'


class dummy_response_404:
    status_code = 404
    def iter_lines(self, *ars, **kwargs):
        yield '404: Not Found'


# Unit tests

def test_systems_provider_http_200():
    from gbfs.client import SystemsProviderHTTPS

    SystemsProviderHTTPS._requests_module = dummy_requests_module(dummy_response_200())
    provider = SystemsProviderHTTPS()

    assert provider.get_all()


def test_systems_provider_http_404():
    from gbfs.client import SystemsProviderHTTPS

    SystemsProviderHTTPS._requests_module = dummy_requests_module(dummy_response_404())
    provider = SystemsProviderHTTPS()

    with pytest.raises(RuntimeError):
        provider.get_all()


def test_systems_provider_local():
    from gbfs.client import SystemsProviderLocal

    provider = SystemsProviderLocal()
    assert provider.get_all()
