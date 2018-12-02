import os
import sys

# TODO: Make this dynamic
root_path = '/Users/jameshadar/dev/GBFSClient'


package_root_dirname = 'gbfs'
package_root_dirpath = os.path.join(root_path, package_root_dirname)
assert os.path.exists(package_root_dirpath)

package_static_dirname = 'static'
package_static_dirpath = os.path.join(package_root_dirpath, package_static_dirname)
assert os.path.exists(package_static_dirpath)

gbfs_systems_csv_remote_url = 'https://raw.githubusercontent.com/NABSA/gbfs/master/systems.csv'
gbfs_systems_csv_local_filepath = os.path.join(package_static_dirpath, 'systems.csv')
assert os.path.exists(gbfs_systems_csv_local_filepath)


class gbfs_systems_csv_fields:
    country_code       = 'Country Code'
    name               = 'Name'
    location           = 'Location'
    system_id          = 'System ID'
    url                = 'URL'
    auto_discovery_url = 'Auto-Discovery URL'