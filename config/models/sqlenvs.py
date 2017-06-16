from .sqlenv import SQLEnv
from ..utils import from_args as f, from_args_fallback as ff


class SQLEnvs:
    def __init__(self, args):
        self.debug = ff(args, 'debug', False)
        self.mysql = SQLEnv(f(args, 'mysql'))
        self.active = self.set_active()

    def set_active(self):
        return self.mysql
