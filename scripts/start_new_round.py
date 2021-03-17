import smtplib
import typing as t

from assassins_cred import config
from assassins_cred import logger
from assassins_cred.io import IO
from assassins_cred.mail import send_to_each
from assassins_cred.school import Student
from assassins_cred.util.school import assign_codes
from assassins_cred.util.shuffle import shuffle_all

email_winners = """Congratulations, {student.first_name}, you have made it to the next round!
But the game is not over yet, you have received a new target!
Your new target is {student.target}.
They could be in any grade.
Death Code: {student.code}"""

email_not_killed = """Unfortunately, you failed to kill your target.
As such, you have been eliminated from the game.
Try again next time"""

winners: t.Dict[str, Student] = {}
dead: t.Dict[str, Student] = {}
not_killed: t.Dict[str, Student] = {}

io = IO()

school = io.read_people()

students = school.students

for student in students:
    if not student.is_dead and student.has_killed:
        winners[student.full_name] = student
    elif student.is_dead:
        dead[student.full_name] = student
    elif not student.is_dead and not student.has_killed:
        not_killed[student.full_name] = student

for name, dead_person in dead.items():
    dead_person.clazz.remove_student(dead_person)
for name, no_kill in not_killed.items():
    no_kill.clazz.remove_student(no_kill)

if len(winners) == 1:
    logger.info(f"The winner is: {list(winners.values())[0]}")
    exit()

shuffle_all(school)
assign_codes(school)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    try:
        smtp.login(config.creds.email, config.creds.password)
    except smtplib.SMTPAuthenticationError:
        logger.error('Turn on less secure access or check if you have the correct password')
        exit()
    to = None if not config.is_test else config.creds.test_to
    send_to_each(
        students=school.students,
        title="Assassin's CRED",
        body=email_winners,
        from_address=config.creds.email,
        smtp=smtp,
        to_address=to
    )
    send_to_each(
        students=not_killed.values(),
        title="Eliminated",
        body=email_not_killed,
        from_address=config.creds.email,
        smtp=smtp,
        to_address=to
    )
