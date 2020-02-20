
from .__name__ import NAME
from .__version__ import VERSION

LOGGER_LEVEL_DEFAULT = 'warning'
DATA_FILENAME = 'oui.json'
SOURCE_FILENAME = 'oui.txt'
SOURCE_URI = 'http://standards-oui.ieee.org/oui/oui.txt'
# DATA_PATH_DEFAULTS = ['/var/lib/ouilookup', '~/.ouilookup']
DATA_PATH_DEFAULTS = ['/var/lib/ouilookup']

from .utils import out
from .utils import timestamp

from .logger import Logger
from .main import OuiLookup
