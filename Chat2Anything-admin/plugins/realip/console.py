"""
输出控制台日志
"""
import sys
import time
import ctypes

NONE = "\033[m"
RED = "\033[0;32;31m"
LIGHT_RED = "\033[1;31m"
GREEN = "\033[0;32;32m"
LIGHT_GREEN = "\033[1;32m"
BLUE = "\033[0;32;34m"
LIGHT_BLUE = "\033[1;34m"
DARY_GRAY = "\033[1;30m"
CYAN = "\033[0;36m"
LIGHT_CYAN = "\033[1;36m"
PURPLE = "\033[0;35m"
LIGHT_PURPLE = "\033[1;35m"
BROWN = "\033[0;33m"
YELLOW = "\033[1;33m"
LIGHT_GRAY = "\033[0;37m"
WHITE = "\033[1;37m"

# 开启 Windows 下对于 ESC控制符 的支持
if sys.platform == "win32":
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


def _print(level, msg):
    time_ = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    level_name = {10: "Plain",
                  11: "Log",
                  12: "Info",
                  13: "Debug",
                  14: "Success",
                  15: "Warning",
                  16: "Error"}

    color = {10: NONE,
             11: LIGHT_CYAN,
             12: LIGHT_BLUE,
             13: PURPLE,
             14: GREEN,
             15: YELLOW,
             16: RED}

    print(f'{color.get(level, NONE)}[{time_}]({level_name.get(level, "Plain")}):', msg, f"{NONE}")


def plain(*args, sep=' '):
    msg = sep.join(str(_) for _ in args)
    _print(10, msg)


def log(*args, sep=' '):
    msg = sep.join(str(_) for _ in args)
    _print(11, msg)


def info(*args, sep=' '):
    msg = sep.join(str(_) for _ in args)
    _print(12, msg)


def debug(*args, sep=' '):
    msg = sep.join(str(_) for _ in args)
    _print(13, msg)


def success(*args, sep=' '):
    msg = sep.join(str(_) for _ in args)
    _print(14, msg)


def warn(*args):
    warning(*args)


def warning(*args, sep=' '):
    msg = sep.join(str(_) for _ in args)
    _print(15, msg)


def error(*args, sep=' '):
    msg = sep.join(str(_) for _ in args)
    _print(16, msg)
