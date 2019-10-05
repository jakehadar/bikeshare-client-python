import io
from setuptools import setup, find_packages

import versioneer

def read_requirements(extension=None):
    ext = '' if extension is None else '-{}'.format(extension)
    filename = 'requirements{}.txt'.format(ext)
    with io.open(filename, encoding='utf-8') as f:
        requirements = [r.strip() for r in f.readlines()]
        return requirements

setup(
    name='gbfs-client',
    version=versioneer.get_version(),
    author='Jake Hadar',
    author_email='jake1025@gmail.com',
    description='Python client for discovering and capturing GBFS bikeshare feeds.',
    long_description=io.open('README.md', encoding='utf-8').read(),
    cmdclass=versioneer.get_cmdclass(),
    include_package_data=True,
    package_data={'gbfs': ['gbfs/static/systems.csv']},
    long_description_content_type='text/markdown',
    url='https://github.com/jakehadar/gbfs-client',
    keywords='gbfs bikeshare client',
    packages=find_packages(),
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
    }
)
