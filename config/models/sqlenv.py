from ..utils import from_args as f, from_args_fallback as ff, from_args_fallback_int as ffi


class SQLEnv:
    def __init__(self, args):
        self.username = f(args, 'USERNAME')
        self.password = f(args, 'PASSWORD')
        self.address = ff(args, 'ADDRESS', '192.168.1.172')
        self.database = ff(args, 'DATABASE', 'andromeda')
        self.port = ffi(args, 'PORT', 3306)
        self.configs = ff(args, 'CONFIGS', '?charset=utf8')
