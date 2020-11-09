from assassins_cred import logger
from assassins_cred.io.files import write_people
from assassins_cred.io.forms import read_form
from assassins_cred.util.config import Config
from assassins_cred.constants import resource_file

config = Config("../config.yaml")

school = read_form(f"../{resource_file}/assassins-cred-test-c55dc518a1bf.json",
                   config.config["sheet_id"])

write_people(school, f"../{resource_file}/people.csv")

logger.info(f"Added people from Google Forms")
