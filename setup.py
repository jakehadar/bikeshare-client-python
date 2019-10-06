# See setup.py for humans: https://github.com/navdeep-G/setup.py

import io
import os
import sys
import shutil
from setuptools import setup, find_packages, Command

# Python 2/3 compat.
try:
    from configparser import RawConfigParser
except ImportError:
    from ConfigParser import RawConfigParser

import versioneer


NAME = 'gbfs-client'
DESCRIPTION = 'Python client for discovering and capturing GBFS bikeshare feeds.'
URL = 'https://github.com/jakehadar/gbfs-client'
AUTHOR = 'Jake Hadar'
EMAIL = 'jake1025@gmail.com'
REQUIRES_PYTHON = '>=2.7'
VERSION = versioneer.get_version()


here = os.path.abspath(os.path.dirname(__file__))


def read_requirements(extension=None):
    ext = '' if extension is None else '-{}'.format(extension)
    filename = 'requirements{}.txt'.format(ext)
    with io.open(filename, encoding='utf-8') as f:
        requirements = [r.strip() for r in f.readlines()]
        return requirements


def read_current_version():
    """Read the current_version string in .bumpversion.cfg"""
    config = RawConfigParser()
    config.add_section('bumpversion')
    config.read_file(io.open('.bumpversion.cfg', 'rt', encoding='utf-8'))
    items = dict(config.items('bumpversion'))
    current_version = items.get('current_version')
    return current_version


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = [
        ('release', 'r', 'Upload to PyPI release instance. (Default: test instance)'),
        ('skip-tests', None, 'Upload without running test first. (Default: run tests)')
    ]

    def initialize_options(self):
        self.release = False
        self.skip_tests = False
        self.upload_cmd = 'twine upload --repository-url https://test.pypi.org/legacy/ dist/*'
        self.install_cmd = 'pip install --index-url https://test.pypi.org/simple/ {0}'.format(NAME)

    def finalize_options(self):
        if self.release:
            self.upload_cmd = 'twine upload dist/*'
            self.install_cmd = 'pip install {0}'.format(NAME)

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def abort(self):
        self.status('Upload aborted.')
        sys.exit(1)

    def validate_deps(self):
        """Validates required packages are installed."""
        _error = False

        try:
            import twine
        except ImportError:
            self.status('Please `pip install twine` to use upload command.')
            _error = True

        try:
            import bumpversion
        except ImportError:
            self.status('Please `pip install bumpversion` to use upload command.')
            _error = True

        if _error:
            self.abort()

    def validate_dirty(self):
        """Aborts upload if there are uncommitted changes."""
        if 'dirty' in VERSION:
            self.status('Uncommitted changes detected in branch.')
            self.abort()


    def run(self):
        self.validate_deps()
        self.validate_dirty()

        if not self.skip_tests:
            self.status('Testing build...')
            res = os.system('{0} setup.py test'.format(sys.executable))

            if res != 0:
                self.abort()

        current_version = read_current_version()
        if VERSION != current_version:
            self.status('Existing version:   {0}'.format(current_version))
            self.status('New patch detected: {0}'.format(VERSION))

            self.status('Bumping version...')
            res = os.system('bumpversion patch')

            if res != 0:
                self.abort()

            new_version = read_current_version()
            self.status('New version:        {0}'.format(new_version))
            os.system('git push --tags')

        self.status('Cleaning build...')
        os.system('{0} setup.py clean --all'.format(sys.executable))

        try:
            self.status('Removing previous builds...')
            shutil.rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution...')
        res = os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        if res != 0:
            self.abort()

        self.status('Uploading the package to PyPI via Twine...')
        res = os.system(self.upload_cmd)

        if res != 0:
            self.abort()
            
        self.status('Upload success!')
        self.status('Installation command: {0}'.format(self.install_cmd))

        sys.exit(0)


cmdclass = versioneer.get_cmdclass()
cmdclass.update({'upload': UploadCommand})


setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    url=URL,
    python_requires=REQUIRES_PYTHON,
    long_description=io.open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    cmdclass=cmdclass,
    include_package_data=True,
    package_data={'gbfs': ['gbfs/static/systems.csv']},
    keywords='gbfs bikeshare client',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
    ],
    install_requires=read_requirements(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    extras_require={
        'dev': read_requirements('dev'),
        'test': read_requirements('test')
    },
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli']
    # }
)
