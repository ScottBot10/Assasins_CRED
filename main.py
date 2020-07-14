from assassins_cred.shuffle import shuffle_by_grade
import pprint

from assassins_cred.file_io.init_read import from_csv
from assassins_cred.file_io.read import read_people
from assassins_cred.file_io.write import write_people
from assassins_cred.shuffle import shuffle_by_grade

grades = from_csv("./test_resources/grade 8.csv")
pprint.pprint(grades)

write_people(grades.values(), "./test_resources/people.csv")

shuff = shuffle_by_grade(list(grades.values()))
pprint.pprint(shuff)

write_people(shuff.values(), "./test_resources/people.csv")

ppl = read_people("./test_resources/people.csv")
pprint.pprint(ppl)
