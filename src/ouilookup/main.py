import hashlib
import json
import os
import time
import urllib.request
from functools import lru_cache

from . import __data_filename__, __data_path_defaults__, __data_source_url__, __logger_name__
from .exceptions import OuiLookupException
from .models import OuiData, OuiDataMeta, OuiDataVendor
from .utils import logger_get, temppath_create, temppath_delete

logger = logger_get(__logger_name__)


class OuiLookup:
    data_file = None

    def __init__(self, data_file=None):
        if data_file:
            self.data_file = data_file
        else:
            self.data_file = self.__find_data_file(data_paths=__data_path_defaults__)

    def query(self, expression):
        logger.debug(f"OuiLookup.query({expression=})")

        if isinstance(expression, str):
            expression = [expression]

        terms = []
        for expression_item in expression:
            term = (
                expression_item.strip()
                .replace(":", "")
                .replace("-", "")
                .replace(".", "")
                .replace(",", " ")
                .upper()
                .split(" ")
            )
            terms += term
        logger.debug(f"Query expression normalized to terms [{', '.join(terms)}]")

        response = []
        data = self.__load_data_file()

        for term in terms:
            if len(term) < 1:
                continue
            term_found = False
            for vendor_key, vendor_name in data["vendors"].items():
                if term.startswith(vendor_key):
                    response.append({term: vendor_name})
                    term_found = True
                    break
            if term_found is not True:
                response.append({term: None})

        return response

    def status(self):
        logger.debug("OuiLookup.status()")
        data = self.__load_data_file()
        return {**data["meta"], **{"data_file": self.data_file}}

    def update(self, data_file=None, source_data_file=None):
        logger.debug(f"OuiLookup.update({data_file=}, {source_data_file=})")

        if not self.data_file and not data_file:
            data_file = os.path.join(__data_path_defaults__[0], __data_filename__)
            logger.debug(f"OuiLookup.update() - setting data_file to {data_file!r}")
        elif not data_file:
            data_file = self.data_file
            logger.debug(f"OuiLookup.update() - setting data_file to {data_file!r}")

        temp_path = temppath_create(pathname_prefix="ouilookup-")

        if source_data_file is None:
            source_data_file = os.path.join(temp_path, "oui.txt")
            logger.debug(f"OuiLookup.update() - download source data file from {__data_source_url__!r}")
            try:
                urllib.request.urlretrieve(__data_source_url__, source_data_file)
            except Exception as e:
                raise OuiLookupException(f"Unable to download from data source {str(e)}")
        else:
            logger.debug(f"OuiLookup.update() - using supplied source data file {source_data_file!r}")

        if not os.path.isfile(source_data_file):
            raise OuiLookupException(f"Unable to locate source data file {source_data_file!r}")

        with open(source_data_file, "rb") as f:
            oui_rawdata = f.read()

        metadata = OuiDataMeta(
            timestamp=time.gmtime(os.path.getmtime(source_data_file)),
            source_bytes=len(oui_rawdata),
            source_data_file=source_data_file,
            source_md5=hashlib.md5(oui_rawdata).hexdigest(),
            source_sha1=hashlib.sha1(oui_rawdata).hexdigest(),
            source_sha256=hashlib.sha256(oui_rawdata).hexdigest(),
            source_url=__data_source_url__,
            vendor_count=0,
        )

        temppath_delete(temp_path)

        vendors = []
        for oui_line in oui_rawdata.decode("utf8").replace("\r", "").split("\n"):
            if "(hex)" in oui_line and "-" in oui_line:
                address = oui_line[0 : oui_line.find("(hex)")].rstrip(" ").replace("-", "")
                name = oui_line[oui_line.find("(hex)") :].replace("(hex)", "").replace("\t", "").strip()
                vendors.append(OuiDataVendor(vendor=name, hwaddr_prefix=address))
                metadata.vendor_count += 1

        oui_data = OuiData(meta=metadata, vendors=vendors)

        logger.debug(f"OuiLookup.update() - saving new data file to {data_file!r}")
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        with open(data_file, "w") as f:
            f.write(json.dumps(oui_data.serialize(), indent="  ", sort_keys=True))

        return {**metadata.as_dict(), **{"data_file": data_file}}

    @lru_cache
    def __load_data_file(self, data_file=None):
        if not data_file:
            data_file = self.data_file

        logger.debug(f"OuiLookup.__load_data_file({data_file=})")

        if not data_file or not os.path.isfile(data_file):
            raise OuiLookupException(f"Unable to locate OuiLookup data file {data_file!r}")

        with open(data_file, "r") as f:
            return json.load(f)

    def __find_data_file(self, data_paths):
        logger.debug(f"OuiLookup.__find_data_file({data_paths=})")

        for data_path in [os.path.abspath(os.path.expanduser(x)) for x in set(data_paths) if os.path.isdir(x)]:
            data_file = os.path.join(data_path, __data_filename__)
            if os.path.isfile(data_file):
                return data_file

        logger.warning(f"Unable to locate any {__data_filename__!r} data file in {data_paths!r}")
