from gbfs.services import SystemDiscoveryService

def example():
    ds = SystemDiscoveryService()

    # Count number of systems discovered
    print('Found {} bikeshare systems.'.format(len(ds.systems)))

    # Show 10 systems...
    print('Showing 10 of the systems_ids found:')
    for system_id in ds.system_ids[:10]:
        print(system_id)
    print('')

    # Select a system with a known system_id
    known_system_id = 'NYC'
    print('Showing system information for a known station_id: {}'.format(known_system_id))
    system = ds.get_system_by_id(known_system_id)
    print(system)
    print('')

    # Instantiate a new GBFSClient from known system_id
    print('Instantiating a GBFSClient for known system_id: {}'.format(known_system_id))
    client = ds.instantiate_client(known_system_id)
    print('')

    # Show the names of available feeds from client
    print('{} system publishes {} feeds:'.format(known_system_id, len(client.feeds)))
    for feed_name in client.feed_names:
        print(feed_name)
    print('')

    # Request some feeds and put together a useful live stat for some arbitrary station

    print('Requesting some live feeds...')
    station_information = client.request_feed('station_information')
    station_status = client.request_feed('station_status')

    stations = station_information.get('data').get('stations')
    print('{} system has {} stations in its network'.format(known_system_id, len(stations)))
    print('')

    first_station = stations[0]

    statuses = station_status.get('data').get('stations')
    first_station_status = [s for s in statuses if s.get('station_id') == first_station.get('station_id')][0]

    print('Station {} has a total capacity of {} and currently has {} bikes available to rent.'.format(
        first_station.get('name'), first_station.get('capacity'), first_station_status.get('num_bikes_available')))
    print('')


if __name__ == '__main__':
    example()