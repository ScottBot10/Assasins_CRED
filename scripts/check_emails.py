import imaplib
import smtplib
from datetime import datetime

from assassins_cred import logger
from assassins_cred.io.files import read_people, write_people
from assassins_cred.mail import get_mail
from assassins_cred.util.config import Config
from assassins_cred.util.school import email_student_dict
from assassins_cred.util.stats_logging import StatsLogger
from assassins_cred.constants import resource_file

STAT_FILE = f"../{resource_file}/stats_log.json"
PEOPLE_FILE = f"../{resource_file}/people.csv"

stats = StatsLogger(STAT_FILE)

school = read_people(PEOPLE_FILE)
students = school.students
students = email_student_dict(students)

config = Config("../config.yaml")

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        try:
            smtp.login(config.creds["email"], config.creds["password"])
        except smtplib.SMTPAuthenticationError:
            logger.error('Turn on less secure access or check if you have the correct password')
            exit()
        with imaplib.IMAP4_SSL("imap.gmail.com") as imap:
            try:
                imap.login(config.creds["email"], config.creds["password"])
            except imap.abort:
                logger.error('Turn on less secure access or check if you have the correct password')
                exit()
            logger.debug("Checking emails")
            while True:
                if get_mail(
                        smtp=smtp,
                        imap=imap,
                        students=students,
                        config=config
                ):
                    write_people(school, PEOPLE_FILE)
                    stats.add_stat(school, datetime.now())
except:
    pass
finally:
    write_people(school, PEOPLE_FILE)
    stats.write()

logger.info("Finished checking emails")
