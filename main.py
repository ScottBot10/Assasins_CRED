from assassins_cred.file_io.init_read import from_csv
import pprint

from assassins_cred.file_io.init_read import from_csv
from assassins_cred.file_io.write import write_people

grades = from_csv("./test_resources/grade 8.csv")
pprint.pprint(grades)

write_people(grades.values(), "./test_resources/people.csv")
