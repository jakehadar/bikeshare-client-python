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

    def abort(self):
        self.status('Aborted upload.')
        sys.exit(1)

    def validate_deps(self):
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


    def initialize_options(self):
        self.test = False
        self.upload_cmd = 'twine upload dist/*'
        self.install_cmd = 'pip install {0}'.format(NAME)

    def finalize_options(self):
        if self.test:
            self.upload_cmd = 'twine upload --repository-url https://test.pypi.org/legacy/ dist/*'
            self.install_cmd = 'pip install --index-url https://test.pypi.org/simple/ {0}'.format(NAME)

    def run(self):
        self.validate_deps()

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
        print('Installation command:'.format(self.install_cmd))

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
