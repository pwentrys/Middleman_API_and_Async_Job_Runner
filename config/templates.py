import os
from pathlib import Path

from config.strings import Strings as s


class Template:
    def __init__(self, projdir, path):
        self.path = path
        self.projdir = projdir
        self.name, self.ext = os.path.splitext(
            str(path).replace(str(projdir), s.empty))
        self.name = self.name[1:]

    def __getlog__(self):
        return f'{self.name}', f'{self.name}{self.ext}'


class Templates:
    def __init__(self, root_file):
        self.path = root_file
        self.realpath = os.path.realpath(self.path)
        self.filename = os.path.basename(self.realpath)
        self.projectdir = Path(os.path.dirname(self.realpath))
        self.templatedir = self.projectdir.joinpath(s.templates)
        self.templates = self.get_file_list(self.templatedir)

    def from_key(self, key):
        return self.templates.get(key, s.empty)

    @staticmethod
    def get_file_list(p):
        path = Path(str(p))
        if not path.exists():
            Templates.ensure_exists(Path)
            return []

        out_list = {}
        for item in path.iterdir():
            if item.is_file() and os.path.splitext(item)[1] == '.html':
                temp = Template(p, item).__getlog__()
                out_list[temp[0]] = temp[1]
        return out_list

    @staticmethod
    def ensure_exists(path):
        try:
            if not path.exists():
                path.mkdir()
        except Exception as e:
            print(path)
            print(e)

    def __getlog__(self):
        return f'Path: {self.path}\n' \
               f'RealPath: {self.realpath}\n' \
               f'Filename: {self.filename}\n' \
               f'ProjectDir: {self.projectdir}\n' \
               f'TemplateDir: {self.templatedir}\n' \
               f'Template Files: {self.templates}\n'

    def __log__(self):
        print(
            self.__getlog__()
        )
