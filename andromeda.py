# --------------------------------------------------------------------------- #
#                                                                             #
#                             Args Parse                                      #
#                                                                             #
# --------------------------------------------------------------------------- #
from argparse import ArgumentParser

from app import run
from config.strings import Strings as s

parser = ArgumentParser(__file__, description=f'Andromeda')

parser.add_argument(
    f'--development',
    '-dev',
    help=f'Dev Mode.',
    action=f'store_true'
)

parser.add_argument(
    f'--production',
    f'-prod',
    help=f'Prod Mode.',
    action=f'store_true'
)

args = parser.parse_args()

# --------------------------------------------------------------------------- #
#                                                                             #
#                               Launch                                        #
#                                                                             #
# --------------------------------------------------------------------------- #

if __name__ == s.main:
    app = run()
    app.toaster.open()
    app.run(
        host=app.authinfo.web.active.address,
        port=app.authinfo.web.active.port,
        debug=app.debug,
        threaded=True
    )
    app.toaster.close()
    # _app.toaster.toast_args({'msg': 'Offline.'})
