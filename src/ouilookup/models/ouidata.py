import time
from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass
class OuiDataMeta:
    timestamp: datetime
    source_url: str
    source_data_file: str
    source_bytes: int
    source_md5: str
    source_sha1: str
    source_sha256: str
    vendor_count: int

    def as_dict(self):
        data = {}
        for k, v in asdict(self).items():
            if k == "timestamp":
                data[k] = time.strftime("%Y-%m-%dT%H:%M:%S+00:00", v)
            else:
                data[k] = str(v)
        return data


@dataclass
class OuiDataVendor:
    vendor: str
    hwaddr_prefix: str


@dataclass
class OuiData:
    meta: OuiDataMeta
    vendors: list[OuiDataVendor]

    def serialize(self):
        data = {"meta": self.meta.as_dict(), "vendors": {}}
        for vendor in self.vendors:
            data["vendors"][vendor.hwaddr_prefix] = vendor.vendor
        return data
