#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='ouilookup',
    version='2018.1',
    description='A tool and library for looking up hardware MAC addresses in the OUI list from ieee.org.',

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
    data_files=[
        ('/var/lib/ouilookup/oui.txt', ['data/oui.txt']),
        ('/var/lib/ouilookup/oui.json', ['data/oui.json']),
    ],
    scripts=['bin/ouilookup'],
    install_requires=[],

)
