import logging
import os
from atexit import register
from datetime import datetime
from inspect import stack
from io import StringIO
from threading import current_thread

from config import CONFIG
from util import Dict

LEVELS = Dict(NOTSET=0, DEBUG=1, INFO=2, WARNING=3, ERROR=4, CRITICAL=5)
PREFS = Dict(LEVEL=LEVELS.NOTSET, SHOW_TAGS=True, ENABLE_THREAD_TAG=True, ENABLE_MODULE_TAG=True, ENABLE_FUNC_TAG=True)

has_init = False


def init():
    level = CONFIG.log_level
    PREFS.LEVEL = level
    _log_start(level)


def _log_start(level=LEVELS.NOTSET):
    tm = datetime.now()
    # file_name = str(manager).replace('-', '').replace(' ', '').replace(':', '.')
    file_name = str(tm.year).zfill(4) + '.' + str(tm.month).zfill(2) + '.' + str(tm.day).zfill(2)
    try:
        logging.basicConfig(filename="log/%s.log" % file_name, level=_conv_level(level))
    except FileNotFoundError as e:
        os.makedirs("log")
        logging.basicConfig(filename="log/%s.log" % file_name, level=_conv_level(level))

    info("------------START------------", header=False)
    global has_init
    has_init = True


@register
def _log_end():
    global has_init
    if has_init:
        info("-------------END-------------\n", header=False)


def blank(count=1):
    print('\n' * count, end='')


def debug(*args, header=True, sep=' ', end='\n'):
    _prnt(logging.getLogger(__name__).debug, *args, header=_get_header(stack()) if header else '', sep=sep, end=end)


def info(*args, header=True, sep=' ', end='\n'):
    _prnt(logging.getLogger(__name__).info, *args, header=_get_header(stack()) if header else '', sep=sep, end=end)


def warn(*args, header=True, sep=' ', end='\n'):
    _prnt(logging.getLogger(__name__).warning, *args, header=_get_header(stack()) if header else '', sep=sep, end=end)


def err(*args, header=True, sep=' ', end='\n'):
    _prnt(logging.getLogger(__name__).error, *args, header=_get_header(stack()) if header else '', sep=sep, end=end)


def crit(*args, header=True, sep=' ', end='\n'):
    _prnt(logging.getLogger(__name__).critical, *args, header=_get_header(stack()) if header else '', sep=sep, end=end)


def _prnt(log_func, *args, header='', **kwargs):
    # args passes as is to keep log file clean
    time = "[%s]" % datetime.now()
    log_func(time + _format_data(header, *args))

    func_name = log_func.__name__

    lvl = 1 if func_name == 'debug' else 2 if func_name == 'info' else 3 if func_name == 'warning' else 4 if func_name == 'error' else 5

    if lvl >= PREFS.LEVEL:
        print("[%s]" % func_name + time + (header if PREFS.SHOW_TAGS else ''), *args, **kwargs)


def _get_header(stack):
    inspection_stack = stack[1]

    calling_module = inspection_stack[1]
    calling_func = inspection_stack[3]
    thread_name = current_thread().name

    header = ''

    if PREFS.ENABLE_THREAD_TAG:
        header += ("[%s]" % thread_name)
    if PREFS.ENABLE_MODULE_TAG:
        header += ("[%s]" % (calling_module[calling_module.rfind("\\") + 1:]))
    if PREFS.ENABLE_FUNC_TAG:
        header += ("[%s]" % calling_func)

    header += ':'

    return header


def _format_data(header, *args):
    io = StringIO()
    print(header, *args, end='', file=io)
    res = io.getvalue()
    io.close()
    return res


def _conv_level(level):
    return logging.NOTSET if level == LEVELS.NOTSET else logging.DEBUG if level == LEVELS.DEBUG else logging.INFO if level == LEVELS.INFO else logging.WARNING if level == LEVELS.WARNING else logging.ERROR if level == LEVELS.ERROR else logging.CRITICAL
