from assassins_cred import logger
from assassins_cred.io import IO
from assassins_cred.util.shuffle import shuffle_school_grade

io = IO()

school = io.read_people()

school = shuffle_school_grade(school)

io.write_people(school=school)

logger.info(f"Assigned targets")
