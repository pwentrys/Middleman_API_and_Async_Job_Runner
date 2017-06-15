from ..utils import from_args as f


class Cookie:
    def __init__(self, args):
        self.domain = f(args, 'domain')
        self.name = f(args, 'name')
