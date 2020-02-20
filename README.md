# ouilookup

[![PyPi](https://img.shields.io/pypi/v/ouilookup.svg)](https://pypi.python.org/pypi/ouilookup/)
[![Python Versions](https://img.shields.io/pypi/pyversions/ouilookup.svg)](https://github.com/verbnetworks/ouilookup/)
[![Build Status](https://api.travis-ci.org/verbnetworks/ouilookup.svg?branch=master)](https://travis-ci.org/verbnetworks/ouilookup/)
[![License](https://img.shields.io/github/license/verbnetworks/ouilookup.svg)](https://github.com/verbnetworks/ouilookup)

A CLI tool and Python3 module for looking up hardware MAC addresses from the published OUI source list at ieee.org.

## Project
* https://github.com/verbnetworks/ouilookup/

## Install
#### via PyPi
```bash
pip3 install ouilookup
```

#### via Source
```bash
git clone https://github.com/verbnetworks/ouilookup
cd ouilookup
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 setup.py clean
python3 setup.py test
python3 setup.py install
```

## Versions
Legacy versions based on year-date (eg v2018.2) have been hard-deprecated in favour of a backward incompatible 
standard versioning scheme (eg v0.2.0).

## CLI usage
```text
usage: ouilookup [-h] [-q <hwaddr> | -u | -un | -s] [-d]

ouilookup v0.0.2

optional arguments:
  -h, --help            show this help message and exit
  -q <hwaddr>, --query <hwaddr>
                        Query to locate matching MAC hardware address(es) from
                        the oui database. Addresses may be expressed in
                        formats with or without ":" or "-" separators. Use a
                        space between addresses for more than one lookup in a
                        single query line.
  -u, --update          Download the latest oui.txt from "standards-
                        oui.ieee.org" and parse it to generate a local
                        oui.json for use by OuiLookup. The following paths (in
                        order) are examined for write-access to save the
                        oui.json data-file: /var/lib/ouilookup
  -un, --update-no-download
                        Parse the oui.txt file in the data-path and update the
                        local oui.json data-file without downloading the
                        latest oui.txt update from "standards-oui.ieee.org".
  -s, --status          Return status information about the oui.json data-file
                        available to OuiLookup.

  -d, --debug           Provide debug logging output to stderr.

A CLI tool for interfacing with the OuiLookup module that provides CLI access
the query(), update() and status() functions. Outputs at the CLI are JSON
formatted thus allowing for easy chaining to other toolchains. The update()
function updates directly from "standards-oui.ieee.org" and the ouilookup
package provides an internal fallback oui.txt updated at time of packaging.
```

## Python3 Module usage

```console
>>> from OuiLookup import OuiLookup

>>> OuiLookup().query('00:00:aa:00:00:00')
[{'0000AA000000': 'XEROX CORPORATION'}]

>>> OuiLookup().query('00:00:01:00:00:00 00-00-10-00-00-00 000011000000')
[{'000001000000': 'XEROX CORPORATION'}, {'000010000000': 'SYTEK INC.'}, {'000011000000': 'NORMEREL SYSTEMES'}]

>>> OuiLookup().update()
{'timestamp': '20200218Z234257', 'source_uri': 'http://standards-oui.ieee.org/oui/oui.txt', 'source_bytes': 4359180, 'source_md5': 'd901b821bbe2506e5837a1a522b48be6', 'source_sha1': '15511c01f00de7b4b9c03f081fc09693fca0f9ca', 'source_sha256': 'a32da3183b0e683082cdf35c85da78d407e017465f184dbd4f6aecd405e561eb', 'vendor_count': 27550}

>>> OuiLookup().status()
{'source_bytes': 4359180, 'source_md5': 'd901b821bbe2506e5837a1a522b48be6', 'source_sha1': '15511c01f00de7b4b9c03f081fc09693fca0f9ca', 'source_sha256': 'a32da3183b0e683082cdf35c85da78d407e017465f184dbd4f6aecd405e561eb', 'source_uri': 'http://standards-oui.ieee.org/oui/oui.txt', 'timestamp': '20200218Z234257', 'vendor_count': 27550, 'data_path': '/usr/local/lib/python3.6/dist-packages/ouilookup/data', 'data_file': '/usr/local/lib/python3.6/dist-packages/ouilookup/data/oui.json'}
```

## Authors
* [Nicholas de Jong](https://nicholasdejong.com)
* Managed by [Verb Networks](https://github.com/verbnetworks).

## License
BSD-2-Clause - see LICENSE file for full details.

NB: License change from Apache-2.0 to BSD-2-Clause in February 2020 at version 0.2.0
