from config.utils import from_args_fallback as ff, from_args_fallback_int as ffi
import requests
from win10toast import ToastNotifier


class Toaster:
    DEFAULT_DURATION = 3
    DEFAULT_MSG = ''
    DEFAULT_TITLE = 'Andromeda'
    DEFAULT_ICON = 'static\\icon.png'

    def __init__(self):
        self.t = ToastNotifier()
        self.address = f'http://192.168.1.172:8020/toast'

    def open(self):
        self.toast_args({'msg': 'Online.'})

    def close(self):
        self.toast_args({'msg': 'Offline.'})

    def toast_args(self, args):
        title = ff(args, 'title', 'Update')
        if not title.__contains__(Toaster.DEFAULT_TITLE):
            title = f'{Toaster.DEFAULT_TITLE} - {title}'
        msg = ff(args, 'msg', Toaster.DEFAULT_MSG)
        duration = ffi(args, 'duration', Toaster.DEFAULT_DURATION)
        requests.get(f'{self.address}/{title}/{msg}/{duration}')

        # self.t.show_toast(
        #     title=title,
        #     msg=msg,
        #     duration=duration
        # )
