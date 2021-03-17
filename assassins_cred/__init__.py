import logging
import os

logger = logging.getLogger("assassins_cred")
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
file = '../logs/assassins_cred.log'
file = os.path.normpath(os.path.abspath(file))
os.makedirs(os.path.dirname(file), exist_ok=True)
file_handler = logging.FileHandler(file, mode='a+')

stream_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.INFO)

stream_handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s: %(message)s"))
file_handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
