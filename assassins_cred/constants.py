import re

people_fieldnames = [
    "name",
    "surname",
    "grade",
    "class",
    "code",
    "target_name",
    "target_surname",
    "is_dead",
    "has_killed"
]

code_length = 3

_NAME_PATTERN = r"(?P<full_name>(?P<first_name>[a-zA-Z()-]+) (?P<surname>[a-zA-Z() -]+))"
_CLASS_PATTERN = r"(?P<full_class>(?P<grade>\d{1,3})(?P<class>[A-Z]))"

NAME_FORMAT = re.compile(_NAME_PATTERN)
CLASS_FORMAT = re.compile(_CLASS_PATTERN)

TXT_FORMAT = re.compile(fr"{_NAME_PATTERN} {_CLASS_PATTERN}")

_EMAIL_PATTERN = r"(?P<from>.+) <(?P<email>(?P<address>[a-zA-Z.]+)@(?P<domain>[a-zA-Z.]+))>"
EMAIL_FORMAT = re.compile(_EMAIL_PATTERN)


class Email:
    email_subject = "elimination"
    email_domain = "westerford.co.za"

    class Titles:
        email_success = "Successful Assassination"
        email_failure = "Unsuccessful Assassination"
        email_assassinated = "You have been Assassinated"
        email_dead = email_failure

    email_success = """You have successfully assassinated your target!
Please wait until the next round and try not to get assassinated yourself!
    
Good luck, Agent!
Do not fail me."""

    email_failure = """You have failed to kill your target!
This is the incorrect death code for your target.
Your target is {student.target}
Get the correct code from your target and email that to us!
    
Good luck, Agent!
Do not fail me."""

    email_dead = """You have already been assassinated and cannot assassinate your target.
    
Better luck next time!
Do not fail me."""

    email_assassinated = """You are probably aware, but you have been assassinated.
Thank you for participating in Assassin's Cred.
    
And next time,
Do not fail me."""
