from assassins_cred.io.files.init_read import from_csv
from assassins_cred.io.files.write import write_people

ppl = from_csv("../test_resources/grade 8.csv")

write_people(ppl, "../test_resources/people.csv")
