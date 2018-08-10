import time
from inspect import stack


class Dict(dict):
    def __setattr__(self, key, item):
        self[key] = item

    def __getattr__(self, key):
        return self.get(key)

    def __add__(self, keyval):
        if isinstance(keyval, dict):
            self.update(keyval)
        elif isinstance(keyval, (list, tuple)):
            self[keyval[0]] = keyval[1]


class Timer:
    __slots__ = ['start_time', 'end_time', 'time_diff']

    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.time_diff = 0

    def reset(self):
        self.start_time = 0
        self.end_time = 0
        self.time_diff = 0

    def start(self):
        self.start_time = time.time()

    def end(self):
        self.end_time = time.time()
        self.time_diff = self.end_time - self.start_time
        return self.time_diff

    def get(self):
        return self.time_diff


def is_intable(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_floatable(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def type_check(var_name, var, *expected_types):
    err_header = stack()[1].filename
    flag = True
    var_type = None

    for typ in expected_types:
        if isinstance(var, typ):
            flag = False
            var_type = typ
            break

    if flag:
        raise Exception(err_header + ": - Invalid Data: Expected type(s) %s for \'%s\' but instead got %s" % (str(expected_types), var_name, str(type(var))))

    return var_type


# Converts the given var to type Number if possible
def numify(var):
    if is_intable(var):
        return int(var)
    elif is_floatable(var):
        return float(var)

    err_header = stack()[1].filename

    raise Exception(err_header + ": - Could not convert %s to primitive number type" % var)


def clamp(value, min_value, max_value):
    return max(min(value, max_value), min_value)
