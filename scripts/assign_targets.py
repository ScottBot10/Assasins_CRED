from assassins_cred.mail.school import assign_codes

from assassins_cred.io.files.read import read_people
from assassins_cred.io.files.write import write_people
from assassins_cred.shuffle import shuffle_school_grade

school = read_people("../test_resources/people.csv")

school = assign_codes(school)
school = shuffle_school_grade(school)

write_people(school, "../test_resources/people.csv")
