from assassins_cred import logger
from assassins_cred.io.files import read_people
from assassins_cred.io.files import write_people
from assassins_cred.util.school import assign_codes
from assassins_cred.util.shuffle import shuffle_school_grade
from assassins_cred.constants import resource_file

school = read_people(f"../{resource_file}/people.csv")

school = assign_codes(school)
school = shuffle_school_grade(school)

write_people(school, f"../{resource_file}/people.csv")

logger.info(f"Assigned targets and codes")
