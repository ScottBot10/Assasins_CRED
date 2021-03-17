from assassins_cred import config
from assassins_cred.io import IO
from assassins_cred.util.school import get_proper_emails

io = IO()

school = io.read_people()

emails = get_proper_emails(school, config.io.forms.creds_file, config.io.forms.token_file)
for student, email in emails.items():
    student._email = email.split('@')[0]

io.write_people(school=school)
