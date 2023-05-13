# ouilookup

[![PyPi](https://img.shields.io/pypi/v/ouilookup.svg)](https://pypi.python.org/pypi/ouilookup/)
[![Python Versions](https://img.shields.io/pypi/pyversions/ouilookup.svg)](https://github.com/ndejong/ouilookup/)
[![build tests](https://github.com/ndejong/ouilookup/actions/workflows/build-tests.yml/badge.svg)](https://github.com/ndejong/ouilookup/actions/workflows/build-tests.yml)
[![License](https://img.shields.io/github/license/ndejong/ouilookup.svg)](https://github.com/ndejong/ouilookup)

A CLI tool and Python module for looking up hardware MAC addresses from the published OUI source list at ieee.org.

## Project
* https://github.com/ndejong/ouilookup/

## Install
#### via PyPi
```bash
pip3 install ouilookup
```

## Versions
Legacy versions based on year-date (eg v2018.2) have been hard-deprecated in favour of a backward incompatible 
standard versioning scheme (eg v0.2.0).

## CLI usage
```text
usage: ouilookup [-h] [-q [<hwaddr> ...] | -s | -u | -ul <filename>] [-d] [-df <data-file>]

ouilookup v0.3.0

options:
  -h, --help            show this help message and exit
  -q [<hwaddr> ...], --query [<hwaddr> ...]
                        Query to locate matching MAC hardware address(es) from 
                        the oui ouilookup.json data file. Addresses may be 
                        expressed in formats with or without ':' or '-' 
                        separators. Use a space or comma between addresses to 
                        query for more than one item in a single query.
  -s, --status          Return status metadata about the ouilookup.json data 
                        file.
  -u, --update          Download the latest from 
                        https://standards-oui.ieee.org/oui/oui.txt then parse 
                        and save as a ouilookup.json data file.
  -ul <filename>, --update-local <filename>
                        Supply a local oui.txt then parse and save as a 
                        ouilookup.json data file.

  -d, --debug           Enable debug logging
  -df <data-file>, --data-file <data-file>
                        Use a data file that is not in the default data file 
                        search paths: /home/<user>/.local/ouilookup, 
                        <package-path>/ouilookup/data, /var/lib/ouilookup

A CLI tool for interfacing with the OuiLookup module that provides CLI access 
the query(), update() and status() functions. Outputs at the CLI are JSON 
formatted allowing for easy chaining with other toolchains. The update() 
function updates directly from "standards-oui.ieee.org".
```

## Python3 Module usage

```console
>>> from OuiLookup import OuiLookup

>>> OuiLookup().query('00:00:aa:00:00:00')
[{'0000AA000000': 'XEROX CORPORATION'}]

>>> OuiLookup().query(['00:00:01:00:00:00','00-00-10-00-00-00','000011000000'])
[{'000001000000': 'XEROX CORPORATION'}, {'000010000000': 'SYTEK INC.'}, {'000011000000': 'NORMEREL SYSTEMES'}]

>>> OuiLookup().update()
{'timestamp': '2023-05-13T14:11:17+00:00', 'source_url': 'https://standards-oui.ieee.org/oui/oui.txt', 'source_data_file': '/tmp/ouilookup-qm5aq0dk/oui.txt', 'source_bytes': '5468392', 'source_md5': '55a434f90da0c24c1a4fcfefe5b2b64b', 'source_sha1': 'dd5e8849ab8c65b2fb12c4b5aef290afee6bbfcd', 'source_sha256': 'af7e4bb1394109f4faad814074d3a6d5b792078074549a5d554c0904612c0bfc', 'vendor_count': '33808', 'data_file': '~/.local/ouilookup/ouilookup.json'}
>>> OuiLookup().status()
{'timestamp': '2023-05-13T14:11:17+00:00', 'source_url': 'https://standards-oui.ieee.org/oui/oui.txt', 'source_data_file': '/tmp/ouilookup-qm5aq0dk/oui.txt', 'source_bytes': '5468392', 'source_md5': '55a434f90da0c24c1a4fcfefe5b2b64b', 'source_sha1': 'dd5e8849ab8c65b2fb12c4b5aef290afee6bbfcd', 'source_sha256': 'af7e4bb1394109f4faad814074d3a6d5b792078074549a5d554c0904612c0bfc', 'vendor_count': '33808', 'data_file': '~/.local/ouilookup/ouilookup.json'}
```

## Authors
* [Nicholas de Jong](https://nicholasdejong.com)

## License
BSD-2-Clause - see LICENSE file for full details.

NB: License change from Apache-2.0 to BSD-2-Clause in February 2020 at version 0.2.0
