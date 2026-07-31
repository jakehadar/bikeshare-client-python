bikeshare-client-python
-----------------------
[![Test](https://github.com/jakehadar/bikeshare-client-python/actions/workflows/test.yml/badge.svg)](https://github.com/jakehadar/bikeshare-client-python/actions/workflows/test.yml)
[![Coverage Status](https://coveralls.io/repos/github/jakehadar/bikeshare-client-python/badge.svg?branch=master)](https://coveralls.io/github/jakehadar/bikeshare-client-python?branch=master)

A Python client for discovering and capturing live bikeshare data feeds made publically available by [hundreds of global bikeshare providers](https://raw.githubusercontent.com/NABSA/gbfs/master/systems.csv) in accordance with the [General Bikeshare Feed Specification (GBFS)](https://github.com/NABSA/gbfs/blob/master/gbfs.md) standard.

This module is built with the intention of laying some of the groundwork for supporting more complex applications built around the consumption of live bikeshare data.


System coverage
---------------

As of writing, this Python client supports every bikeshare system published in the GBFS community's systems directory (over 1.5k systems across dozens of countries and regions).

The list of bikeshare systems supported by this client is [actively maintained by the GBFS community](https://github.com/NABSA/gbfs/blob/master/README.md#systems-implementing-gbfs) and can be found here:
* [systems.csv](https://raw.githubusercontent.com/NABSA/gbfs/master/systems.csv)

The code example below demonstrates how to discover and filter these systems programatically.


Installation
------------

Install from PyPi using
[pip](http://www.pip-installer.org/en/latest/), a package manager for
Python.

``` {.sourceCode .bash}
 pip install gbfs-client
```

Examples
--------

A sample implementation (Flask JSON endpoint) can be found here:

* [bikeshare-json-api](https://github.com/jakehadar/bikeshare-json-api)


Interactive walk-through
------------------------

Searching for bikeshare systems in WI and NY using the system discovery service:

``` {.sourceCode .python}
>>> from gbfs.services import SystemDiscoveryService
>>> ds = SystemDiscoveryService()
>>> len(ds.system_ids)
1519
>>> [x.get('System ID') for x in ds.systems if 'WI' in x.get('Location')]
['bcycle_bublr', 'bcycle_madison', 'provider-null-milwaukee']
>>> ds.get_system_by_id('bcycle_madison')
{'Country Code': 'US', 'Name': 'Madison B-cycle', 'Location': 'Madison, WI', 'System ID': 'bcycle_madison', 'URL': 'https://madison.bcycle.com', 'Auto-Discovery URL': 'https://gbfs.bcycle.com/bcycle_madison/gbfs.json', 'Supported Versions': '1.1', 'Authentication Info URL': '', 'Authentication Type': '', 'Authentication Parameter Name': ''}
>>> [x.get('System ID') for x in ds.systems if 'citi bike' in x.get('Name').lower()]
['lyft_nyc']
>>> ds.get_system_by_id('lyft_nyc')
{'Country Code': 'US', 'Name': 'Citi Bike', 'Location': 'New York, NY', 'System ID': 'lyft_nyc', 'URL': 'https://www.citibikenyc.com', 'Auto-Discovery URL': 'https://gbfs.citibikenyc.com/gbfs/2.3/gbfs.json', 'Supported Versions': '2.3', 'Authentication Info URL': '', 'Authentication Type': '', 'Authentication Parameter Name': ''}
```

Instantiating a GBFS client for Citi Bike (NYC) and exploring its available feeds:

```
>>> client = ds.instantiate_client('lyft_nyc')
>>> client.feed_names
['gbfs', 'system_information', 'station_information', 'station_status', 'free_bike_status', 'system_hours', 'system_calendar', 'system_regions', 'system_pricing_plans', 'system_alerts', 'gbfs_versions', 'vehicle_types']
>>> client.request_feed('system_alerts')
{'data': {'alerts': []}, 'last_updated': datetime.datetime(2026, 7, 31, 15, 11, 43), 'ttl': 60, 'version': '2.3'}
```

Instantiating a GBFS client directly (without the discovery service) using the auto-discovery URL for Citi Bike (found earlier):

```{.sourceCode .python}
>>> from gbfs.client import GBFSClient
>>> client = GBFSClient('https://gbfs.citibikenyc.com/gbfs/gbfs.json', 'en')
```

Searching Citi Bike's station_information feed for two specific stations, one near 49th/8th ave and the other near Barclay/Church:

```
>>> stations = client.request_feed('station_information').get('data').get('stations')
>>> [(x.get('name'), x.get('station_id')) for x in stations if '49' in x.get('name')]
[('Broadway & W 49 St', '173'), ('W 49 St & 8 Ave', '450'), ('49 Ave & 21 St', '3606')]
>>> home = next(filter(lambda x: x.get('station_id') == '450', stations))
>>> home
{'station_id': '450', 'name': 'W 49 St & 8 Ave', 'lat': 40.76227205, 'lon': -73.98788205, 'capacity': 59}
>>> [(x.get('name'), x.get('station_id')) for x in stations if 'Barclay' in x.get('name')]
[('Barclay St & Church St', '417')]
>>> work = next(filter(lambda x: x.get('station_id') == '417', stations))
>>> work
{'station_id': '417', 'name': 'Barclay St & Church St', 'lat': 40.71291224, 'lon': -74.01020234, 'capacity': 23}
```

Building a small app to poll a station's live status and print a nice message:

```{.sourceCode .python}
>>> def live_status_for(station):
...     all_statuses = client.request_feed('station_status').get('data').get('stations')
...     return next(filter(lambda x: x.get('station_id') == station.get('station_id'), all_statuses))
...

>>> def print_status_message(station):
...     bikes_available = live_status_for(station).get('num_bikes_available')
...     print('{} is currently at {}% capacity with {} bikes available to rent.'.format(
...         station.get('name'), int(100*bikes_available/station.get('capacity')), bikes_available))

>>> print_status_message(home)
W 49 St & 8 Ave is currently at 16% capacity with 10 bikes available to rent.
>>> print_status_message(work)
Barclay St & Church St is currently at 91% capacity with 21 bikes available to rent.
```


Contributing
------------

This project targets Python 3.7+, and is tested in CI against 3.9 through 3.14.

**Set up a development environment**

Clone the repo and install it in editable mode with the `dev` and `test` extras, which pull in `tox`, `coverage`, `pytest`, and related tooling:

``` {.sourceCode .bash}
git clone https://github.com/jakehadar/bikeshare-client-python.git
cd bikeshare-client-python
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev,test]"
```

**Run the tests**

``` {.sourceCode .bash}
pytest
```

With coverage:

``` {.sourceCode .bash}
coverage run -m pytest
coverage report -m
```

**Run the full tox matrix**

`tox` runs the test suite across every supported Python version (3.9-3.14) that's installed on your machine. Any versions you don't have installed locally are skipped; the full matrix still runs in CI on every push and pull request.

``` {.sourceCode .bash}
tox
```

To test against a single interpreter, editable-installed in place (`usedevelop = True`):

``` {.sourceCode .bash}
tox -e dev
```

Change log
----------

### 0.1.9

Add support for Python 3.9 through 3.14, and drop support for Python 2 and versions of Python 3 below 3.7.

* Removed the `six` dependency and the Python 2/3 compatibility shims it enabled.
* Fixed an install-breaking bug in the vendored `versioneer.py` on Python 3.12+ (`configparser.SafeConfigParser` was removed in 3.12).
* Replaced the unmaintained `pytest-runner`/`setup.py test` integration with running `pytest` directly.
* Replaced the dormant Travis CI setup with GitHub Actions, testing across Python 3.9-3.14.
* Extended `tox` to cover the same matrix, skipping any interpreters not installed locally.
* Added a Contributing section to this README outlining development environment setup, running tests, and using `tox`.
* Fixed New York City's outdated `NYC` system_id (now `lyft_nyc`) in the README and example script — thanks to [@kjcole](https://github.com/kjcole) for reporting and fixing ([#8](https://github.com/jakehadar/bikeshare-client-python/issues/8)).

### 0.1.8

Add support for bespoke feeds with tokenized URL templates.

For example, Barcelona's supplemental `'nearby_stations'` URL is tokenized with `{station_id}`:
```
{
    "name": "nearby_stations",
    "url": "https://barcelona-sp.publicbikesystem.net/ube/gbfs/v1/en/station_information/{station_id}/nearby_stations"
}
```
The consumer is required to interpolate `station_id` into the URL string before requesting the feed.

`GBFSClient`'s `request_feed` method now accepts kwargs for formatting URL templates of this kind.

Example:

```
c = GBFSClient('https://barcelona.publicbikesystem.net/ube/gbfs/v1/gbfs.json')

c.request_feed('nearby_stations', station_id=2)
```

### 0.1.5

Baseline release.
