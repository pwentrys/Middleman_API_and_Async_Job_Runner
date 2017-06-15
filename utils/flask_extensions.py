from config.strings import Strings as s


def _add_url_vars_list(app, var_list, string, func):
    string = string.replace(s.slash, s.underscoreX2)
    for var in var_list:
        app.add_url_rule(var, string, func)


def _get_vars(string):
    return [
        f'/{string}',
        f'/{string}/'
    ]


def _get_vars_html(string):
    return _get_vars(string) + _get_vars(f'{string}.html')


def _format_url_string(string):
    while string[0] == s.slash:
        string = string[1:]
    while string[len(string) - 1] == s.slash:
        string = string[:-1]
    return string


def add_url_vars(app, string, func):
    string = _format_url_string(string)

    _add_url_vars_list(app, _get_vars(string), string, func)


def add_url_vars_html(app, string, func):
    string = _format_url_string(string)

    _add_url_vars_list(app, _get_vars_html(string), string, func)
