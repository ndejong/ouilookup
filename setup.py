#!/usr/bin/env python3

from setuptools import setup

setup(
    name='ouilookup',
    version='2018.6',
    description='A tool and library for looking up hardware MAC addresses in the OUI list from ieee.org.',
    long_description='A tool and library for looking up hardware MAC addresses in the OUI list from ieee.org.',

    classifiers=[
        'Environment :: Console',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'Topic :: System :: Networking :: Monitoring',
        'License :: OSI Approved :: Apache Software License',
    ],
    keywords='ouilookup oui mac mac-address hw-address ether ethernet arp',

    author='Nicholas de Jong',
    author_email='me@nicholasdejong.com',
    url='https://github.com/ndejong/ouilookup',
    license='Apache',

    packages=['ouilookup'],

    package_data={
        'ouilookup': ['data/*.json', 'data/*.txt'],
    },

    scripts=['bin/ouilookup'],

    install_requires=[],

)
