"""
SETTINGS

This file contains all settings and configurations for running your project
"""
from os.path import dirname, abspath, join
import os

INFO = True
# INFO = False

ERROR = True
# ERROR = False

DEBUG = True
# DEBUG = False

PROJECT_DIR = join(dirname(abspath(__file__)), os.pardir)
BACKEND_DIR = join(PROJECT_DIR, 'backend')
STATIC_DIR = join(PROJECT_DIR, 'static')
DATABASE_FP = join(BACKEND_DIR, 'database/db.json')
STREAM_DIR = join(BACKEND_DIR, 'stream')

GARAGE_DOOR_IP_ADDRESS = '169.254.186.211'
GARAGE_DOOR_PORT = 7654
STREAM_PORT = 8854

MASTER_KEY = "0x4cd9c30446bf0fd0b72b63c57ada73b34fcd0576a18de673945d66edbbdb6c4d"



