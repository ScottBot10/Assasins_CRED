import smtplib

from assassins_cred import logger
from assassins_cred.constants import Email
from assassins_cred.io.files import read_people
from assassins_cred.mail import send_to_each
from assassins_cred.util.config import Config
from assassins_cred.util.school import unpack_students

school = read_people("../test_resources/people.csv")
students = unpack_students(school.grades)

config = Config("../config.yaml")

body = """To {student.first_name}

The hunt begins Monday 29 July. This email has 2 important details, your target and your death code. Locate your target around the school and 'eliminate' them. If someone around your target notices, your kill can be halted. Upon death your target will give you their death code, the same applies to you. An assassin must send an email with the subject: '{subject}' and the death code in the body. After the end of the round if you have not been eliminated and have made your kill, you will be notified and assigned a new target. If, by the end of the round, you have failed to kill your target, you will be automatically eliminated. The first round will run for 2 weeks, each further round will be one week until only one assassin remains. Please send your emails to {cred_email}
Good luck and happy hunting.
Your target is: {student.target}.
They are in your grade.
Death Code: {student.code}"""

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    try:
        smtp.login(config.creds["email"], config.creds["password"])
    except smtplib.SMTPAuthenticationError:
        logger.error('Turn on less secure access or check if you have the correct password')
        exit()
    send_to_each(
        students=students,
        title="Assassin's CRED",
        body=body,
        from_address=config.creds["email"],
        smtp=smtp,
        to_address=None if not config.is_test else config.creds["test_to"],
        format_kws={'subject': Email.email_subject, 'cred_email': config.creds["email"]}
    )
