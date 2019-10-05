# See setup.py for humans: https://github.com/navdeep-G/setup.py

import io
import os
import sys
import shutil
from setuptools import setup, find_packages, Command

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


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = [
        ('test', 't', 'Upload to PyPI test instance.')
    ]

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        self.test = False
        self.upload_args = ''
        self.install_args = ''

    def finalize_options(self):
        if self.test:
            self.upload_args = '--repository-url https://test.pypi.org/legacy/'
            self.install_args = '--index-url https://test.pypi.org/simple/'

    def run(self):
        try:
            import twine
        except ImportError:
            self.status('Please install twine to use upload command.')
            self.status('  $ pip install twine')
            self.status('Aborting.')
            sys.exit(1)

        self.status('Cleaning build...')
        os.system('{0} setup.py clean --all'.format(sys.executable))

        try:
            self.status('Removing previous builds...')
            shutil.rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution...')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))
        
        if self.test:
            self.status('Uploading the package to PyPI (test instance) via Twine...')
            os.system('twine upload --repository-url https://test.pypi.org/legacy/ dist/*')

            self.status('Installation command:')
            self.status('pip install --index-url https://test.pypi.org/simple/ {0}'.format(NAME))
            sys.exit()

        if '+' in VERSION:
            commits_ahead = VERSION.split('+')[1].split('.')[0]
            self.status('Build is {0} commits ahead of master.'.format(commits_ahead))
            self.status('Aborting.')

            sys.exit(1)

        self.status('Uploading the package to PyPI via Twine...')
        os.system('twine upload dist/*')
            
        self.status('Installation command:')
        self.status('pip install {0}'.format(NAME))

        self.status('Pushing git tags...')
        os.system('git tag v{0}'.format(VERSION))
        os.system('git push --tags')

        sys.exit()


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
