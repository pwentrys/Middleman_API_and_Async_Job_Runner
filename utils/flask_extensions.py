from config.strings import Strings as s


def _add_url_vars_list(app, var_list, string, func):
    """
    Add url variables list.
    :param app:
    :param var_list:
    :param string:
    :param func:
    :return:
    """
    string = string.replace(s.slash, s.underscoreX2)
    for var in var_list:
        app.add_url_rule(var, string, func)


def _get_vars(string):
    """
    Get variables.
    :param string:
    :return:
    """
    return [
        f'/{string}',
        f'/{string}/'
    ]


def _get_vars_html(string):
    """
    Get variables html page.
    :param string:
    :return:
    """
    return _get_vars(string) + _get_vars(f'{string}.html')


def _format_url_string(string):
    """
    Normalize url.
    :param string:
    :return:
    """
    while string[0] == s.slash:
        string = string[1:]
    while string[len(string) - 1] == s.slash:
        string = string[:-1]
    return string


def add_url_vars(app, string, func):
    """
    Add url variables.
    :param app:
    :param string:
    :param func:
    :return:
    """
    string = _format_url_string(string)

    _add_url_vars_list(app, _get_vars(string), string, func)


def add_url_vars_html(app, string, func):
    """
    Add url variables html page.
    :param app:
    :param string:
    :param func:
    :return:
    """
    string = _format_url_string(string)

    _add_url_vars_list(app, _get_vars_html(string), string, func)
