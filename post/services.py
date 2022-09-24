from django.db.models import Q


def is_empty(_str):
    if isinstance(_str, str):
        return is_none(_str) or len(_str.strip()) == 0
    return False

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

def add_query(query, condition, is_and = True):
    if is_null_or_empty(query):
        if is_and:
            query = & condition
        else:
            query = | condition
    else:
        query = condition
    return query
