# -*- coding: utf8 -*-
# Copyright (c) 2018-2023 Nicholas de Jong

__author__ = "Nicholas de Jong <contact@nicholasdejong.com>"
__version__ = "0.3.1"
__title__ = "ouilookup"
__logger_name__ = "ouilookup"

import os

__data_filename__ = "ouilookup.json"
__data_source_url__ = "https://standards-oui.ieee.org/oui/oui.txt"
__data_path_localuser__ = os.path.abspath(os.path.expanduser("~/.local/ouilookup"))
__data_path_package__ = os.path.abspath(os.path.join(os.path.dirname(__file__), "data"))
__data_path_system__ = "/var/lib/ouilookup"
__data_path_defaults__ = [__data_path_localuser__, __data_path_package__, __data_path_system__]

from .utils.logger import logger_get

__logger_level__ = "debug" if os.getenv("OUILOOKUP_DEBUG", "").lower().startswith(("true", "yes", "enable")) else "info"
logger_get(name=__logger_name__, loglevel=__logger_level__)

from .main import OuiLookup  # noqa: E402
