from gbfs.const import gbfs_systems_csv_local_filepath, gbfs_systems_csv_remote_url
from gbfs.data.fetchers import RemoteFileFetcher, LocalFileFetcher
from gbfs.data.providers import CSVDataProvider

__all__ = [
    'systems_provider_local_csv',
    'systems_provider_remote_csv',
    'systems_provider_default'
]

local_file_fetcher = LocalFileFetcher()
remote_file_fetcher = RemoteFileFetcher()

systems_provider_local_csv = CSVDataProvider(local_file_fetcher, gbfs_systems_csv_local_filepath)
systems_provider_remote_csv = CSVDataProvider(remote_file_fetcher, gbfs_systems_csv_remote_url)

systems_provider_default = systems_provider_local_csv