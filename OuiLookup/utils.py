
import json
import datetime


def timestamp():
    return datetime.datetime.utcnow().strftime("%Y%m%dZ%H%M%S")


def out(data, indent=2, sort_keys=False):
    if type(data) is str:
        print(data)
    else:
        print(json.dumps(data, indent=indent, sort_keys=sort_keys))
