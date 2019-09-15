import os


package_root_dirpath = os.path.abspath(os.path.dirname(__file__))

package_static_dirname = 'static'
package_static_dirpath = os.path.join(package_root_dirpath, package_static_dirname)

package_tests_dirname = 'tests'
package_tests_dirpath = os.path.join(package_root_dirpath, package_tests_dirname)

package_tests_fixtures_dirname = 'fixtures'
package_tests_fixtures_dirpath = os.path.join(package_tests_dirpath, package_tests_fixtures_dirname)

gbfs_systems_csv_remote_url = 'https://raw.githubusercontent.com/NABSA/gbfs/master/systems.csv'
gbfs_systems_csv_local_filepath = os.path.join(package_static_dirpath, 'systems.csv')


class gbfs_systems_csv_fields:
    country_code       = 'Country Code'
    name               = 'Name'
    location           = 'Location'
    system_id          = 'System ID'
    url                = 'URL'
    auto_discovery_url = 'Auto-Discovery URL'


gbfs_client_default_language = 'en'
