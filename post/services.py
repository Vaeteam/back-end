from django.db.models import Q


def is_null_or_empty(_str):
    if _str is None:
        return True
    if isinstance(_str, str):
        if len(_str.strip()) == 0:
            return True
        if len(_str.strip()) > 0:
            return _str.strip().isspace()
        return True
    return False

def is_null_or_empty_params(*args):
    for arg in args:
        if is_null_or_empty(arg):
            return True
    return False
