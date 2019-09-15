from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

with open('requirements.txt', 'r') as f:
    requirements = [req.strip() for req in f.readlines()] 

setup(
    name='gbfs-client',
    version='0.0.2',
    author='Jake Hadar',
    author_email='jake1025@gmail.com',
    description='Python client for discovering and capturing GBFS bikeshare feeds.',
    long_description=long_description,
    include_package_data=True,
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
    install_requires=requirements,
)
