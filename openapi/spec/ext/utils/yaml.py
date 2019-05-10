from yaml import load, dump

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


def load_yaml(stream):
    return load(stream, Loader=Loader)


def read_yaml(path):
    with open(path) as f:
        return load_yaml(f)


def dump_yaml(data):
    return dump(data, Dumper=Dumper)


def write_yaml(data, path, mode='w'):
    with open(path, mode=mode) as f:
        f.write(dump_yaml(data))
