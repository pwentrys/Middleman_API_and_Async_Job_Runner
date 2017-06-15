from win10toast import ToastNotifier
from config.utils import from_args_fallback as ff, from_args_fallback_int as ffINT
import os


class Toaster:
    DEFAULT_DURATION = 1
    DEFAULT_MSG = ''
    DEFAULT_TITLE = 'Andromeda'
    DEFAULT_ICON = 'static\\icon.png'

    def __init__(self):
        self.t = ToastNotifier()

    def show_default_toast(self):
        self.t.show_toast("Hello World!!!",
                           "Python is awsm by default!")

    def toast_custom(self, args):
        self.t.show_toast(f'Custom Toast',
                          f'{args.get("message", "ERROR")}'
                          )

    def toast_args(self, args):
        self.t.show_toast(title=ff(args, 'title', Toaster.DEFAULT_TITLE),
                          msg=ff(args, 'msg', Toaster.DEFAULT_MSG),
                          # icon_path=ff(args, 'icon_path', Toaster.DEFAULT_ICON),
                          duration=ffINT(args, 'duration', Toaster.DEFAULT_DURATION)
                          )

    def toast_title(self, title):
        self.t.show_toast(
            title=title,
            msg=''
        )

    def toast_body(self, msg):
        self.t.show_toast(
            title='',
            msg=msg
        )

    def toast_titlebody(self, title, msg):
        self.t.show_toast(
            title=title,
            msg=msg
        )

    def toast_titlebodyicon(self, title, msg, icon_path):
        self.t.show_toast(
            title=title,
            msg=msg,
            icon_path=icon_path
        )

    def toast_titlebodyicondur(self, title, msg, icon_path, duration):
        self.t.show_toast(
            title=title,
            msg=msg,
            icon_path=icon_path,
            duration=int(duration)
        )
