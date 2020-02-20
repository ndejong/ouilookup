
import os
import json
import time
import hashlib
import urllib.request
from shutil import copyfile

from . import NAME
from . import VERSION
from . import DATA_PATH_DEFAULTS
from . import DATA_FILENAME
from . import SOURCE_FILENAME
from . import SOURCE_URI
from . import logger


class OuiLookupException(Exception):
    pass


class OuiLookup:

    data_file = None
    data_paths = None
    __data_cache = None

    def __init__(self, logger_level='warning'):
        logger.init(name=NAME, level=logger_level)
        logger.debug('{} v{}'.format(NAME, VERSION))
        self.data_paths = self.__data_paths_expand()
        logger.debug({'data_paths': self.data_paths})

    def query(self, expression):
        logger.debug('OuiLookup::query(expression={})'.format(expression))

        terms = expression.strip().replace(':','').replace('-','').replace('.','').upper().split(' ')
        logger.debug('OuiLookup::query() - terms {}'.format(terms))

        response = []
        data = self.__load_datafile()

        for term in terms:
            if len(term) < 1:
                continue
            term_found = False
            for vendor_key, vendor_name in data['vendors'].items():
                if term.startswith(vendor_key):
                    response.append({term: vendor_name})
                    term_found = True
                    break
            if term_found is not True:
                response.append({term: None})

        return response

    def status(self):
        logger.debug('OuiLookup::status()')
        data = self.__load_datafile()
        return {
            **data['meta'],
            **{
                'data_path': os.path.dirname(self.data_file),
                'data_file': self.data_file
            }
        }

    def update(self, skip_download=False):
        logger.debug('OuiLookup::update()')

        data_path_writeable = None
        source_file_writeable = None
        for data_path in self.data_paths:
            if not os.path.isdir(data_path):
                try:
                    os.makedirs(data_path, mode=0o0755, exist_ok=True)
                    logger.debug('OuiLookup::update() - data path created {}'.format(data_path))
                except PermissionError:
                    pass

            if os.path.isdir(data_path):
                source_file_writeable = os.path.join(data_path, SOURCE_FILENAME)
                data_path_writeable = data_path
                try:
                    with open(source_file_writeable, 'a'):
                        os.utime(source_file_writeable, None)
                    os.unlink(source_file_writeable)
                except PermissionError:
                    source_file_writeable = None
                    data_path_writeable = None
                break

        if data_path_writeable is None or source_file_writeable is None:
            raise OuiLookupException('Unable to locate a data_path with write permissions', self.data_paths)

        if skip_download is False:
            try:
                logger.debug('OuiLookup::update() - downloading {} to {}'.format(SOURCE_URI, source_file_writeable))
                urllib.request.urlretrieve(SOURCE_URI, source_file_writeable)
            except Exception as e:
                raise OuiLookupException('Unable to download from data source - {}'.format(e))

        if not os.path.isfile(source_file_writeable):
            for data_path_source in self.data_paths:
                source_filename_probe = os.path.join(data_path_source, SOURCE_FILENAME)
                if os.path.isfile(source_filename_probe):
                    logger.debug('OuiLookup::update() - copying {} to {}'.format(source_filename_probe, source_file_writeable))
                    copyfile(source_filename_probe, source_file_writeable)
                    break

        if not os.path.isfile(source_file_writeable):
            raise OuiLookupException('Unable to locate any source_file to work with')

        logger.debug('OuiLookup::update() - using source file {}'.format(source_file_writeable))

        with open(source_file_writeable, 'rb') as f:
            raw = f.read()

        data = {}
        data['meta'] = {
            'timestamp': time.strftime("%Y%m%dZ%H%M%S", time.gmtime(os.path.getctime(source_file_writeable))),
            'source_uri': SOURCE_URI,
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
                name = raw_line[raw_line.find('(hex)'):].replace('(hex)', '').replace('\t','').strip()
                data['vendors'][address] = name
                data['meta']['vendor_count'] +=1

        data_filename = os.path.join(data_path_writeable, DATA_FILENAME)

        try:
            logger.debug('OuiLookup::update() - writing data_file {}'.format(data_filename))
            with open(data_filename, 'w') as f:
                f.write(json.dumps(data, indent='  ', sort_keys=True))
        except Exception as e:
            raise OuiLookupException('Unable to save data_file - {}'.format(e))

        self.data_file = data_filename
        self.__data_cache = data
        return data['meta']

    def __load_datafile(self):
        logger.debug('OuiLookup::__load_datafile()')

        if self.__data_cache is None:
            for data_path in self.data_paths:
                data_file = os.path.join(data_path, DATA_FILENAME)
                if os.path.isfile(data_file):
                    self.data_file = data_file
                    logger.debug('OuiLookup::__load_datafile() - loading data_file {}'.format(data_file))
                    with open(self.data_file, 'r') as f:
                        self.__data_cache = json.load(f)
                        break
            if self.__data_cache is None:
                raise OuiLookupException('Unable to locate a data file in paths', self.data_paths)

        return self.__data_cache

    def __data_paths_expand(self):
        data_paths = []
        DATA_PATH_DEFAULTS.append(os.path.join(os.path.dirname(__file__), 'data'))
        for data_path in DATA_PATH_DEFAULTS:
            data_path_expanded = os.path.abspath(os.path.expanduser(data_path))
            data_paths.append(data_path_expanded)
        return data_paths

    def __get_writeable_datafile(self, filename, times=None):
        with open(filename, 'a'):
            os.utime(filename, times)
