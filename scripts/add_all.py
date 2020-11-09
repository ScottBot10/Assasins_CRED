from assassins_cred import logger
from assassins_cred.io.files import from_csv, write_people
from assassins_cred.constants import resource_file

ppl = from_csv(f"{resource_file}/grade 8.csv")

write_people(ppl, f"{resource_file}/people.csv")

logger.info(f"Added all the people")
