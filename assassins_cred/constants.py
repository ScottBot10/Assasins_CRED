import re
import string
from os import path

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

PROJECT_ROOT = path.normpath(path.abspath(path.join(path.dirname(path.abspath(__file__)), '..')))

config_file = path.normpath(path.join(PROJECT_ROOT, "config.yaml"))

school_name = "westerford"

resource_file = "test_resources"

code_chars = string.ascii_lowercase + string.digits
code_length = 3

_NAME_PATTERN = r"(?P<full_name>(?P<first_name>[a-zA-Z()-]+) (?P<surname>[a-zA-Z() -]+))"
_CLASS_PATTERN = r"(?P<full_class>(?P<grade>\d{1,3})(?P<class>[A-Z]))"

NAME_FORMAT = re.compile(_NAME_PATTERN)
CLASS_FORMAT = re.compile(_CLASS_PATTERN)

TXT_FORMAT = re.compile(fr"{_NAME_PATTERN} {_CLASS_PATTERN}")

_EMAIL_PATTERN = r"(?P<email>(?P<address>[a-zA-Z.]+)@(?P<domain>[a-zA-Z.]+))"
EMAIL_FORMAT = re.compile(_EMAIL_PATTERN)

_EMAIL_FROM_PATTERN = fr"(?P<from>.+) <{_EMAIL_PATTERN}>"
EMAIL_FROM_FORMAT = re.compile(_EMAIL_FROM_PATTERN)
