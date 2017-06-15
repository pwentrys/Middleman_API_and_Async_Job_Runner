from ..utils import from_args as f


class WebEnv:
    def __init__(self, args):
        self.name = f(args, 'name')
        self.address = f(args, 'address')
        self.lifetime = f(args, 'lifetime')
        self.port = f(args, 'port')
        self.secret_key = f(args, 'secret_key')
