# See setup.py for humans: https://github.com/navdeep-G/setup.py

import io
from setuptools import setup, find_packages

import versioneer


NAME = 'gbfs-client'
DESCRIPTION = 'Python client for discovering and capturing GBFS bikeshare feeds.'
URL = 'https://github.com/jakehadar/gbfs-client'
AUTHOR = 'Jake Hadar'
EMAIL = 'jake1025@gmail.com'
REQUIRES_PYTHON = '>=3.7'
VERSION = versioneer.get_version()


def read_requirements(extension=None):
    ext = '' if extension is None else '-{}'.format(extension)
    filename = 'requirements{}.txt'.format(ext)
    with io.open(filename, encoding='utf-8') as f:
        requirements = [r.strip() for r in f.readlines()]
        return requirements


cmdclass = versioneer.get_cmdclass()


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
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
    ],
    install_requires=read_requirements(),
    extras_require={
        'dev': read_requirements('dev'),
        'test': read_requirements('test')
    },
    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli']
    # }
)
