from assassins_cred.io.files import write_people
from assassins_cred.io.forms import read_form

school = read_form("../test_resources/assassins-cred-test-c55dc518a1bf.json",
                   "1WSvIL8ve5fRtF28vIv6jsvQN7QDMX1ynScmms9AC0CQ")

write_people(school, "../test_resources/people.csv")
