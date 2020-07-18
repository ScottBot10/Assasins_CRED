import logging
import pprint

from assassins_cred.io.files import from_csv, read_people, write_people
from assassins_cred.mail import EMAIL_FORMAT
from assassins_cred.util.shuffle import shuffle_school_grade

logger = logging.getLogger("assassins_cred")

school = from_csv("./test_resources/grade 8.csv")
pprint.pprint(school)

write_people(school, "./test_resources/people.csv")

shuff = shuffle_school_grade(school)
pprint.pprint(shuff)

write_people(shuff, "./test_resources/people.csv")

school = read_people("./test_resources/people.csv")
pprint.pprint(school)

match = EMAIL_FORMAT.match("<Scott> scott.faurholm@gmail.com")
match_2 = EMAIL_FORMAT.match("<Jack Saunders> jsaunders@westerford.co.za")

logger.debug(match)
