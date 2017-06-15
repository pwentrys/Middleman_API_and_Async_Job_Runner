from .webenv import WebEnv
from ..utils import from_args as f, from_args_fallback as ff


class WebEnvs:
    def __init__(self, args):
        self.debug = ff(args, 'debug', False)
        self.dev = WebEnv(f(args, 'dev'))
        self.prod = WebEnv(f(args, 'prod'))
        self.active = self.set_active()

    def set_active(self):
        return self.dev if self.debug else self.prod
