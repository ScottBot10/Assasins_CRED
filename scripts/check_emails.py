import imaplib
import smtplib

from assassins_cred import logger
from assassins_cred.io.files import read_people, write_people
from assassins_cred.mail import get_mail
from assassins_cred.util.config import Config
from assassins_cred.util.school import unpack_students, email_student_dict

school = read_people("../test_resources/people.csv")
students = unpack_students(school.grades)
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
                has_changed = get_mail(
                    smtp=smtp,
                    imap=imap,
                    students=students,
                    config=config
                )
                if has_changed:
                    write_people(school, "../test_resources/people.csv")
except:
    pass
finally:
    write_people(school, "../test_resources/people.csv")

logger.info("Finished checking emails")
