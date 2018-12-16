bikeshare-client
----------------

A Python client for discovering and capturing live bikeshare data feeds made publically available by [hundreds of global bikeshare providers](https://raw.githubusercontent.com/NABSA/gbfs/master/systems.csv) in accordance with the [General Bikeshare Feed Specification (GBFS)](https://github.com/NABSA/gbfs/blob/master/gbfs.md) standard.

This module is built with the intention of laying some of the groundwork for supporting more complex applications built around the consumption of live bikeshare data.

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

Searching for bikeshare systems in WI and NY using the system discovery service:

``` {.sourceCode .python}
>>> from gbfs.services import SystemDiscoveryService
>>> ds = SystemDiscoveryService()
>>> len(ds.system_ids)
221
>>> [x.get('System ID') for x in ds.systems if 'WI' in x.get('Location')]
['bcycle_bublr', 'bcycle_madison']
>>> ds.get_system_by_id('bcycle_madison')
{'Country Code': 'US', 'Name': 'Madison B-cycle', 'Location': 'Madison, WI', 'System ID': 'bcycle_madison', 'URL': 'https://madison.bcycle.com', 'Auto-Discovery URL': 'https://gbfs.bcycle.com/bcycle_madison/gbfs.json'}
>>> [x.get('System ID') for x in ds.systems if 'citi bike' in x.get('Name').lower()]
['NYC', 'jump_nyc', 'lime_new_york', 'reddy_bikeshare', 'sobi_long_beach']
>>> ds.get_system_by_id('NYC')
{'Country Code': 'US', 'Name': 'Citi Bike', 'Location': 'NYC, NY', 'System ID': 'NYC', 'URL': 'https://www.citibikenyc.com', 'Auto-Discovery URL': 'https://gbfs.citibikenyc.com/gbfs/gbfs.json'}
```

Instantiating a GBFS client for Citi Bike (NYC) and exploring its available feeds:

```
>>> client = ds.instantiate_client('NYC')
>>> client.feed_names
['system_alerts', 'system_information', 'station_information', 'station_status', 'system_regions']
>>> client.request_feed('system_alerts')
{'last_updated': datetime.datetime(2018, 12, 3, 1, 49, 55), 'ttl': 10, 'data': {'alerts': []}}
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
