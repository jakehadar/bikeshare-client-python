from gbfs.const import gbfs_systems_csv_local_filepath, gbfs_systems_csv_remote_url
from gbfs.data.fetchers import RemoteCSVFetcher, LocalCSVFetcher
from gbfs.data.providers import SystemDataProvider

__all__ = [
    'systems_provider_local_csv',
    'systems_provider_remote_csv',
    'systems_provider_default'
]

local_csv_fetcher = LocalCSVFetcher()
remote_csv_fetcher = RemoteCSVFetcher()

systems_provider_local_csv = SystemDataProvider(local_csv_fetcher, gbfs_systems_csv_local_filepath)
systems_provider_remote_csv = SystemDataProvider(remote_csv_fetcher, gbfs_systems_csv_remote_url)

systems_provider_default = systems_provider_remote_csv