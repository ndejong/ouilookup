import json


def output(data, indent=2, sort_keys=False):
    if type(data) is str:
        print(data)
    else:
        print(json.dumps(data, indent=indent, sort_keys=sort_keys))
