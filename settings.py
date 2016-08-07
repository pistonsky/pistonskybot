import logging


logging.basicConfig(format='%(message)s', level=logging.INFO)

try:
    from local_settings import *
except ImportError:
    pass
