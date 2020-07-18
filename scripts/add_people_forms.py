from assassins_cred import logger
from assassins_cred.io.files import write_people
from assassins_cred.io.forms import read_form
from assassins_cred.util.config import Config

config = Config("../config.yaml")

school = read_form("../test_resources/assassins-cred-test-c55dc518a1bf.json",
                   config.config["sheet_id"])

write_people(school, "../test_resources/people.csv")

logger.info(f"Added people from Google Forms")
