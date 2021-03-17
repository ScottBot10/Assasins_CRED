import imaplib
import smtplib
from datetime import datetime

from assassins_cred import config
from assassins_cred import logger
from assassins_cred.io import IO
from assassins_cred.mail import get_mail
from assassins_cred.util.school import email_student_dict
from assassins_cred.util.stats_logging import StatsLogger

io = IO()

stats = StatsLogger(config.stats_file)

school = io.read_people()
students = school.students
students = email_student_dict(students)

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        try:
            smtp.login(config.creds.email, config.creds.password)
        except smtplib.SMTPAuthenticationError:
            logger.error('Turn on less secure access or check if you have the correct password')
            exit()
        with imaplib.IMAP4_SSL("imap.gmail.com") as imap:
            try:
                imap.login(config.creds.email, config.creds.password)
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
                    io.write_people(school)
                    stats.add_stat(school, datetime.now())
except:
    pass
finally:
    io.write_people(school)
    stats.write()

logger.info("Finished checking emails")
