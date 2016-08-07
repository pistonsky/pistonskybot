import logging


logging.basicConfig(format='%(message)s', level=logging.DEBUG)

try:
    from local_settings import *
except ImportError:
    pass
