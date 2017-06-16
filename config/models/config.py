from .cookie import Cookie
from ..utils import from_args as f


class Config:
    def __init__(self, args):
        """
        Expected in args:
            'name' - string
            'debug' - bool
            'cookie_domain' - 'name' in .lower()
            'cookie_name' - 'name' in .lower()
            'web' - dev + prod objects
        :param args:
        """
        self.name = f(args, 'name')
        self.debug = f(args, 'debug')
        self.cookie = Cookie({
            'domain': f(args, 'cookie_domain'),
            'name': f(args, 'cookie_name')
        })
        self.web = f(args, 'web')
        self.sql = f(args, 'sql')
