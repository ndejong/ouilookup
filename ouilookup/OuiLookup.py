
import os
import json
import argparse
import time
import hashlib
import urllib.request
from ouilookup import LoggerManager


class OuiLookupException(Exception):
    pass


class OuiLookup:

    SOURCE_URI = 'http://standards-oui.ieee.org/oui.txt'
    DATA_PATH = '/var/lib/ouilookup'
    LOCAL_FILENAME = 'oui.txt'
    DATA_FILENAME = 'oui.json'

    Log = None

    args = None
    debug = None
    datafile = None

    def __init__(self):
        self.arg_parse()
        self.Log = LoggerManager.LoggerManager().build_logger(
            'ouilookup',
            is_console_quiet=True,
            is_console_debug=self.debug
        )
        self.datafile = os.path.join(self.DATA_PATH, self.DATA_FILENAME)

    def arg_parse(self):
        ArgParse = argparse.ArgumentParser(
            prog='ouilookup',
            description='A CLI tool for interfacing with the OuiLookup library which can be easily integrated '
                        'programmatically into other projects - Up-to-date source data can be easily managed and '
                        'retrieved from the ieee.org site - outputs at the CLI are JSON formatted allowing for '
                        'easy chaining to other toolchains and programmatic queries via OuiLookup return the same '
                        'data-structures.',
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
                 'locally stored oui.json datafile for use with OuiLookup either in programmatic or CLI use.'
        )
        ArgParseGroup0.add_argument(
            '--update-no-download',
            required=False,
            default=False,
            action='store_true',
            help='Parse the previously existing oui.txt file in the data path and update the locally stored oui.json '
                 'datafile.'
        )
        ArgParseGroup0.add_argument(
            '-s',
            '--status',
            required=False,
            default=False,
            action='store_true',
            help='Return status information about the locally stored oui.json datafile.'
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

    def main(self):
        self.Log.debug('OuiLookup::main()')

        response = None

        if self.args.update is True:
            response = self.datafile_update()

        elif self.args.update_no_download is True:
            response = self.datafile_update(skip_download=True)

        else:

            try:
                self.datafile_checks()
            except OuiLookupException as e:
                self.Log.fatal(e)
                exit(1)

            if self.args.status is True:
                response = self.datafile_status()

            if self.args.query is not False:
                response = self.query(expression=self.args.query)

        print(json.dumps(response, indent='  ', sort_keys=True))
        return response

    def query(self, expression):
        self.Log.debug('OuiLookup::query(expression={})'.format(expression))

        terms = expression.replace('-','').replace(':','').upper().split(' ')
        self.Log.debug('OuiLookup::query() - terms {}'.format(terms))

        response = []

        with open(self.datafile, 'r') as f:
            data = json.load(f)

        for vendor_key, vendor_name in data['vendors'].items():
            for term in terms:
                if term.startswith(vendor_key):
                    response.append({term: vendor_name})

        return response

    def datafile_status(self):
        self.Log.debug('OuiLookup::datafile_status()')

        with open(self.datafile, 'r') as f:
            data = json.load(f)

        data['meta']['data_path'] = self.DATA_PATH
        data['meta']['data_file'] = self.datafile

        return data['meta']

    def datafile_checks(self):
        self.Log.debug('OuiLookup::datafile_checks()')

        if not os.path.isdir(self.DATA_PATH):
            raise OuiLookupException('Unable to locate required data path, try running with --update to create the '
                                     'path and download the required oui datafile.', self.DATA_PATH)

        if not os.path.isfile(self.datafile):
            raise OuiLookupException('Unable to locate required data file, try running with --update to download the '
                                     'oui data and create the required datafile.', self.datafile)

        self.Log.debug('OuiLookup::datafile_checks() - Okay')
        return True

    def datafile_update(self, skip_download=False):
        self.Log.debug('OuiLookup::datafile_update()')

        if not os.path.isdir(self.DATA_PATH):
            try:
                os.makedirs(self.DATA_PATH, mode=0o0755, exist_ok=True)
            except Exception as e:
                self.Log.fatal('Unable to create data path - {}'.format(e))
                exit(1)
            self.Log.debug('OuiLookup::datafile_update() - data path created {}'.format(self.DATA_PATH))

        local_filename = os.path.join(self.DATA_PATH, self.LOCAL_FILENAME)

        if skip_download is False:
            try:
                self.Log.debug('OuiLookup::datafile_update() - downloading {} to {}'.format(self.SOURCE_URI, local_filename))
                urllib.request.urlretrieve(self.SOURCE_URI, local_filename)
            except Exception as e:
                self.Log.fatal('Unable to download from data source - {}'.format(e))
                exit(1)

        if not os.path.isfile(local_filename):
            self.Log.fatal('Missing local source file {}'.format(local_filename))
            exit(1)
        self.Log.debug('Local source file {}'.format(local_filename))

        with open(local_filename, 'rb') as f:
            raw = f.read()

        data = {}
        data['meta'] = {
            'timestamp_retrieved': time.strftime("%Y%m%dZ%H%M%S", time.gmtime(os.path.getctime(local_filename))),
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
            with open(self.datafile, 'w') as f:
                f.write(json.dumps(data, indent='  ', sort_keys=True))
        except Exception as e:
            self.Log.fatal('Unable to save datafile - {}'.format(e))
            exit(1)

        return data['meta']
