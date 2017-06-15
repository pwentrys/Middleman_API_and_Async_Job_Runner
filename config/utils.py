from pathlib import Path
from datetime import datetime


def dt2f(x):
    return x.strftime('%Y-%m-%d %H:%M:%S')


def ts2dt(x):
    return datetime.fromtimestamp(x)


def ts2dt2f(x):
    return dt2f(ts2dt(x))


def from_args(args, key):
    return args[key] if args.__contains__(key) else f'ERROR'


def from_args_fallback(args, key, fallback):
    return args[key] if args.__contains__(key) else f'{fallback}'


def from_args_fallback_int(args, key, fallback):
    return int(args[key]) if args.__contains__(key) else fallback


def to_decimal__xy(x, y):
    return '{0:2.2f}'.format(x / y)


def to_percent__xy(x, y):
    return '{:.2%}'.format(x / y)


def to_percent(x):
    return '{:.2%}'.format(x)


def format_percent(x):
    return '{0:2.2f}{1}'.format(x, '%')


def format_column_header(string):
    _name = str(string).lower()
    _name = f'{_name[0].upper()}{_name[1:]}'
    _name = _name.replace('_', ' ').replace('-', ' ')
    return _name


def create_ifnexist(path):
    if not path.exists():
        if not Path(path.parent).exists():
            if path != path.drive:
                create_ifnexist(Path(path.parent))
        path.mkdir()
