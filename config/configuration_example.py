from .models.config import Config
from .models.webenvs import WebEnvs


appname = f'GAPPI'
appnamelower = appname.lower()
is_debug = False  # SUPER IMPORTANT

config = Config({
    'name': appname,
    'cookie_domain': f'{appnamelower}',
    'cookie_name': f'{appnamelower}_dev' if is_debug else f'{appnamelower}',
    'debug': is_debug,
    'web': WebEnvs({
        'dev': {
            'name': f'Dev',
            'address': f'0.0.0.0',
            'port': 8000,
            'secret_key': f'SUPER_SECRET_DEV',
            'lifetime': 1  # session lifetime in days.
        },
        'prod': {
            'name': f'Prod',
            'address': f'0.0.0.0',
            'port': 5000,
            'secret_key': f'SUPER_SECRET',
            'lifetime': 1  # session lifetime in days.
        },
    }),
})
