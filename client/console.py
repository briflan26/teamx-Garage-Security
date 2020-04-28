import settings


def info(s):
    if settings.INFO:
        print('[INFO]  ' + s.strip())


def error(s):
    if settings.ERROR:
        print('[ERROR] ' + s.strip())


def debug(s):
    if settings.DEBUG:
        print('[DEBUG] ' + s.strip())
