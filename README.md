# ouilookup

[![License: Apache 2.0](https://img.shields.io/badge/license-Apache_2.0-green.svg)](LICENSE)

A tool and library for looking up hardware MAC addresses in the OUI list from ieee.org. 

## library usage

```
>>> from ouilookup import OuiLookup

>>> OuiLookup().query('00:00:aa:00:00:00')
[{'0000AA000000': 'XEROX CORPORATION'}]

>>> OuiLookup().query('00:00:01:00:00:00 00-00-10-00-00-00 000011000000')
[{'000001000000': 'XEROX CORPORATION'}, {'000010000000': 'SYTEK INC.'}, {'000011000000': 'NORMEREL SYSTEMES'}]

>>> OuiLookup().update()
{'timestamp': '20180611Z153932', 'source_uri': 'http://standards-oui.ieee.org/oui.txt', 'source_bytes': 3911106, 'source_md5': 'af9157e8d969100e8b00bf281f92d2ac', 'source_sha1': '2f835cbb45ab01cd0d36c94450bbee9b1b59dc84', 'source_sha256': '306e1f5078017a5c3bc999ae69b052b4e68d5ae83ca04053ae102596c9c553d2', 'vendor_count': 24967}

>>> OuiLookup().status()
{'source_bytes': 3911106, 'source_md5': 'af9157e8d969100e8b00bf281f92d2ac', 'source_sha1': '2f835cbb45ab01cd0d36c94450bbee9b1b59dc84', 'source_sha256': '306e1f5078017a5c3bc999ae69b052b4e68d5ae83ca04053ae102596c9c553d2', 'source_uri': 'http://standards-oui.ieee.org/oui.txt', 'timestamp': '20180611Z103551', 'vendor_count': 24967, 'data_path': '/usr/local/lib/python3.6/dist-packages/ouilookup/data', 'data_file': '/usr/local/lib/python3.6/dist-packages/ouilookup/data/oui.json'}
```


## command-line usage
```text
usage: ouilookup [-h] [-q <mac-address> | -u | --update-no-download | -s] [-d]

A CLI tool for interfacing with the OuiLookup library, to access the query(),
update() and status() functions. Outputs at the CLI are JSON formatted
allowing for easy chaining to other toolchains and return the same data-
structures when calling via the OuiLookup library directly. The update()
function updates directly from "standards-oui.ieee.org" and the ouilookup
package provides a fallback oui.txt updated at time of packaging.

arguments:
  -h, --help            show this help message and exit
  -q <mac-address>, --query <mac-address>
                        Query to locate matching MAC hardware address(es) from
                        the oui database. Addresses may be expressed in
                        formats with or without ":" or "-" separators and are
                        case insensitive. Use a space between addresses for
                        more than one lookup in a single query line.
  -u, --update          Download from "standards-oui.ieee.org" a local copy of
                        the oui.txt file, then parse and update the locally
                        stored oui.json data_file for use with the OuiLookup
                        library. The following paths (in order) are examined
                        for write-access to save the oui.json data_file:
                        /var/lib/ouilookup, ~/.ouilookup,
                        /usr/local/lib/python3.6/dist-packages/ouilookup/data
  --update-no-download  Parse a previously existing oui.txt file in the
                        data_path and update the locally stored oui.json
                        data_file without attempting to download from
                        "standards-oui.ieee.org".
  -s, --status          Return status information about oui.json data_file
                        available to OuiLookup.
  -d, --debug           Provide debug logging output to stderr.
```
