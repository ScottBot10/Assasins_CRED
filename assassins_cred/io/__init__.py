import importlib

from assassins_cred import logger
from .. import config


class IO:
    def __init__(self, init=False, **kw):
        self.io_init = config.io_init
        self.io_type = config.io_type

        self.init_module = importlib.import_module(f"assassins_cred.io.{self.io_init}")
        self.io_module = importlib.import_module(f"assassins_cred.io.{self.io_type}")

        self.init = init

        self.init_setup = self.init_module.setup(self.init, **dict(config.io[self.io_init]))
        self.io_setup = self.io_module.setup(self.init, **dict(config.io[self.io_type]))

        self.kw = kw

    def init_read(self, *a, **kw):
        kw.update(self.init_setup)
        kw.update(**self.kw)
        read = self.init_module.init_read(*a, **kw)
        logger.debug(f"Ran init_read with io module {self.io_init}")
        return read

    def read_people(self, *a, **kw):
        kw.update(self.io_setup)
        kw.update(**self.kw)
        read = self.io_module.read_people(*a, **kw)
        logger.debug(f"Ran read_people with io module {self.io_type}")
        return read

    def write_people(self, *a, **kw):
        kw.update(self.io_setup)
        kw.update(**self.kw)
        self.io_module.write_people(*a, **kw)
        logger.debug(f"Ran write_people with io module {self.io_type}")
