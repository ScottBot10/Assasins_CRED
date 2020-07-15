import pprint

from assassins_cred.io.init_read import from_csv
from assassins_cred.io.read import read_people
from assassins_cred.io.write import write_people
from assassins_cred.shuffle import shuffle_school_grade

school = from_csv("./test_resources/grade 8.csv")
pprint.pprint(school)

write_people(school, "./test_resources/people.csv")

shuff = shuffle_school_grade(school)
pprint.pprint(shuff)

write_people(shuff, "./test_resources/people.csv")

school = read_people("./test_resources/people.csv")
pprint.pprint(school)
