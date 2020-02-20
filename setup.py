#!/usr/bin/env python3

from setuptools import setup, find_packages
from OuiLookup import NAME
from OuiLookup import VERSION

with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name=NAME,
    version=VERSION,
    description='A CLI tool and Python3 module for looking up hardware MAC addresses from the published OUI source at ieee.org.',

    long_description=long_description,
    long_description_content_type='text/markdown',

    classifiers=[
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Networking :: Monitoring',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
    ],
    keywords='ouilookup oui mac mac-address hw-address ether ethernet',

    author='Verb Networks Pty Ltd',
    author_email='contact@verbnetworks.com',
    url='https://github.com/verbnetworks/ouilookup',
    license='BSD-2-Clause',

    zip_safe=False,
    packages=find_packages(),
    package_data={
        'OuiLookup': ['data/*.json', 'data/*.txt'],
    },
    scripts=['bin/ouilookup'],

    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],

)
