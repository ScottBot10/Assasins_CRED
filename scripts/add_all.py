from assassins_cred import logger
from assassins_cred.io import IO
from assassins_cred.util.school import assign_codes

io = IO(init=True)

school = io.init_read()

io.write_people(school=assign_codes(school))

logger.info(f"Added all the people")
