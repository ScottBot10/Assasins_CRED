import logging

logger = logging.getLogger("assassins_cred")
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('../logs/assassins_cred.log')

stream_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.INFO)

stream_handler.setFormatter(logging.Formatter("%(levelname)s:%(name)s: %(message)s"))
file_handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))

logger.addHandler(stream_handler)
logger.addHandler(file_handler)
