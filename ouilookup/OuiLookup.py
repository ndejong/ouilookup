
import os
import json
import argparse
import time
import hashlib
import urllib.request
from shutil import copyfile
from ouilookup import LoggerManager


class OuiLookupException(Exception):
    pass


class OuiLookup:

    SOURCE_URI = 'http://standards-oui.ieee.org/oui.txt'
    DATA_PATHS = ['/var/lib/ouilookup', '~/.ouilookup', os.path.join(os.path.dirname(__file__),'data')]
    SOURCE_FILENAME = 'oui.txt'
    DATA_FILENAME = 'oui.json'

    Log = None

    args = None
    debug = None
    data_file = None

    __data_cache = None

    def __init__(self):
        self.Log = LoggerManager.LoggerNull()

    def arg_parse(self):
        ArgParse = argparse.ArgumentParser(
            prog='ouilookup',
            description='A CLI tool for interfacing with the OuiLookup library, to access the query(), update() and '
                        'status() functions. Outputs at the CLI are JSON formatted allowing for easy chaining to other '
                        'toolchains and return the same data-structures when calling via the OuiLookup library '
                        'directly. The update() function updates directly from "standards-oui.ieee.org" and the '
                        'ouilookup package provides a fallback oui.txt updated at time of packaging.',
        )

        ArgParseGroup0 = ArgParse.add_mutually_exclusive_group()
        ArgParseGroup0.add_argument(
            '-q',
            '--query',
            required=False,
            default=False,
            type=str,
            metavar='<mac-address>',
            help='Query to locate matching MAC hardware address(es) from the oui database. Addresses may be expressed '
                 'in formats with or without ":" or "-" separators and are case insensitive.  Use a space between '
                 'addresses for more than one lookup in a single query line.'
        )
        ArgParseGroup0.add_argument(
            '-u',
            '--update',
            required=False,
            default=False,
            action='store_true',
            help='Download from "standards-oui.ieee.org" a local copy of the oui.txt file, then parse and update the '
                 'locally stored oui.json data_file for use with the OuiLookup library. The following paths (in order) '
                 'are examined for write-access to save the oui.json data_file: {}'.format(', '.join(self.DATA_PATHS))
        )
        ArgParseGroup0.add_argument(
            '--update-no-download',
            required=False,
            default=False,
            action='store_true',
            help='Parse a previously existing oui.txt file in the data_path and update the locally stored oui.json '
                 'data_file without attempting to download from "standards-oui.ieee.org".'
        )
        ArgParseGroup0.add_argument(
            '-s',
            '--status',
            required=False,
            default=False,
            action='store_true',
            help='Return status information about oui.json data_file available to OuiLookup.'
        )

        ArgParseGroup1 = ArgParse.add_argument_group()
        ArgParseGroup1.add_argument(
            '-d',
            '--debug',
            required=False,
            default=False,
            action='store_true',
            help='Provide debug logging output to stderr.'
        )

        self.args = ArgParse.parse_args()
        self.debug = self.args.debug

        if self.args.query is False and \
                self.args.status is False and \
                self.args.update is False and \
                self.args.update_no_download is False:
            ArgParse.print_help()
            exit(1)

    def cli(self):

        self.arg_parse()

        self.Log = LoggerManager.LoggerManager().build_logger(
            'ouilookup',
            is_console_quiet=True,
            is_console_debug=self.debug
        )

        self.Log.debug('OuiLookup::cli()')

        response = None

        try:
            if self.args.update is True:
                response = self.update()

            elif self.args.update_no_download is True:
                response = self.update(skip_download=True)

            elif self.args.status is True:
                response = self.status()

            elif self.args.query is not False:
                response = self.query(expression=self.args.query)

            else:
                raise OuiLookupException('Unexpected args condition')

        except OuiLookupException as e:
            self.Log.fatal(e)
            exit(1)

        print(json.dumps(response, indent='  ', sort_keys=True))
        return response

    def query(self, expression):
        self.Log.debug('OuiLookup::query(expression={})'.format(expression))

        terms = expression.replace('-','').replace(':','').upper().split(' ')
        self.Log.debug('OuiLookup::query() - terms {}'.format(terms))

        response = []
        data = self.__get_data()

        for vendor_key, vendor_name in data['vendors'].items():
            for term in terms:
                if term.startswith(vendor_key):
                    response.append({term: vendor_name})

        return response

    def status(self):
        self.Log.debug('OuiLookup::status()')

        data = self.__get_data()

        return {
            **data['meta'],
            **{'data_path': os.path.dirname(self.data_file), 'data_file': self.data_file}
        }

    def update(self, skip_download=False):
        self.Log.debug('OuiLookup::update()')

        data_path_usable = None
        data_file_usable = None
        for data_path in self.DATA_PATHS:
            data_path_expanded = os.path.expanduser(data_path)
            if not os.path.isdir(data_path_expanded):
                try:
                    os.makedirs(data_path_expanded, mode=0o0755, exist_ok=True)
                    self.Log.debug('OuiLookup::update() - data path created {}'.format(data_path_expanded))
                except Exception:
                    pass

            if os.path.isdir(data_path_expanded):
                try:
                    data_file_usable = os.path.join(data_path_expanded, self.DATA_FILENAME)
                    self.file_touch(data_file_usable)
                    data_path_usable = data_path_expanded
                    break
                except Exception:
                    pass

        if data_path_usable is None:
            raise OuiLookupException('Unable to locate a data_path with write permissions', self.DATA_PATHS)

        source_filename = os.path.join(data_path_usable, self.SOURCE_FILENAME)

        if skip_download is False:
            try:
                self.Log.debug('OuiLookup::update() - downloading {} to {}'.format(self.SOURCE_URI, source_filename))
                urllib.request.urlretrieve(self.SOURCE_URI, source_filename)
            except Exception as e:
                raise OuiLookupException('Unable to download from data source - {}'.format(e))

        if not os.path.isfile(source_filename):
            for data_path_source in self.DATA_PATHS:
                source_filename_probe = os.path.join(data_path_source, self.SOURCE_FILENAME)
                if os.path.isfile(source_filename_probe):
                    self.Log.debug('OuiLookup::update() - copying {} to {}'.format(source_filename_probe, source_filename))
                    copyfile(source_filename_probe, source_filename)
                    break

        if not os.path.isfile(source_filename):
            raise OuiLookupException('Unable to locate any source_file to work with')

        self.Log.debug('OuiLookup::update() - using source file {}'.format(source_filename))

        with open(source_filename, 'rb') as f:
            raw = f.read()

        data = {}
        data['meta'] = {
            'timestamp': time.strftime("%Y%m%dZ%H%M%S", time.gmtime(os.path.getctime(source_filename))),
            'source_uri': self.SOURCE_URI,
            'source_bytes': len(raw),
            'source_md5': hashlib.md5(raw).hexdigest(),
            'source_sha1': hashlib.sha1(raw).hexdigest(),
            'source_sha256': hashlib.sha256(raw).hexdigest(),
            'vendor_count': 0,
        }

        data['vendors'] = {}
        for raw_line in raw.decode('utf8').replace('\r','').split('\n'):
            if '(hex)' in raw_line and '-' in raw_line:
                address = raw_line[0:raw_line.find('(hex)')].rstrip(' ').replace('-','')
                name = raw_line[raw_line.find('(hex)'):].replace('(hex)', '').replace('\t','').lstrip(' ').rstrip(' ')
                data['vendors'][address] = name
                data['meta']['vendor_count'] +=1

        try:
            self.Log.debug('OuiLookup::update() - writing data_file {}'.format(data_file_usable))
            with open(data_file_usable, 'w') as f:
                f.write(json.dumps(data, indent='  ', sort_keys=True))
        except Exception as e:
            raise OuiLookupException('Unable to save data_file - {}'.format(e))

        self.data_file = data_file_usable
        self.__data_cache = data
        return data['meta']

    def file_touch(self, filename, times=None):
        with open(filename, 'a'):
            os.utime(filename, times)

    def __get_data(self):
        self.Log.debug('OuiLookup::__get_data()')

        if self.__data_cache is None:
            for data_path in self.DATA_PATHS:
                data_file = os.path.expanduser(os.path.join(data_path, self.DATA_FILENAME))
                if os.path.isfile(data_file):
                    self.data_file = data_file
                    self.Log.debug('OuiLookup::__get_data() - loading data_file {}'.format(data_file))
                    with open(self.data_file, 'r') as f:
                        self.__data_cache = json.load(f)
                        break

            if self.__data_cache is None:
                raise OuiLookupException('Unable to locate a data file in paths', self.DATA_PATHS)

        return self.__data_cache
