# ouilookup

[![License: Apache 2.0](https://img.shields.io/badge/license-Apache_2.0-green.svg)](LICENSE)

```text
usage: ouilookup [-h] [-q <mac-address> | -u | --update-no-download | -s] [-d]

A CLI tool for interfacing with the OuiLookup library which can be easily
integrated programmatically into other projects - Up-to-date source data can
be easily managed and retrieved from the ieee.org site - outputs at the CLI
are JSON formatted allowing for easy chaining to other toolchains and
programmatic queries via OuiLookup return the same data-structures.

optional arguments:
  -h, --help            show this help message and exit
  -q <mac-address>, --query <mac-address>
                        Query to locate matching MAC hardware address(es) from
                        the oui database. Addresses may be expressed in
                        formats with or without ":" or "-" separators and are
                        case insensitive. Use a space between addresses for
                        more than one lookup in a single query line.
  -u, --update          Download from "standards-oui.ieee.org" a local copy of
                        the oui.txt file, then parse and update the locally
                        stored oui.json datafile for use with OuiLookup either
                        in programmatic or CLI use.
  --update-no-download  Parse the previously existing oui.txt file in the data
                        path and update the locally stored oui.json datafile.
  -s, --status          Return status information about the locally stored
                        oui.json datafile.

  -d, --debug           Provide debug logging output to stderr.
```
