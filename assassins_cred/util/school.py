from __future__ import annotations

import random
import time
import typing as t
from itertools import combinations
from typing import TYPE_CHECKING

from googleapiclient.discovery import build

from ..constants import code_length, code_chars
from ..util.google import create_token

if TYPE_CHECKING:
    from ..school import School, Grade, Class, Student


def _unpack_students_key(student: Student):
    return (
        (
            student.clazz.grade._sort_key(student.clazz),
            student.clazz._sort_key(student)
        ) if student.clazz.grade is not None else
        Class._sort_key(student)
    )


def assign_codes(school: School) -> School:
    combos_left = list(
        map(lambda x: ''.join(x), combinations(code_chars, code_length)))
    students = school.students
    if len(combos_left) < len(students):
        raise ValueError("There are not enough code combinations! Try increasing the code length")
    for student in students:
        code = random.choice(combos_left)
        combos_left.remove(code)
        student.code = code
    return school


def assign_code(school: School, student: Student) -> Student:
    combos = [student.code for student in school.students]
    combos_left = [
        combo for combo in
        map(lambda x: ''.join(x), combinations(code_chars.digits, code_length))
        if combo not in combos
    ]
    student.code = random.choice(combos_left)
    return student


def full_name(first_name: str, surname: str, middle_names=None):
    if middle_names is None:
        middle_names = []
    _full_name = f"{first_name} "
    if middle_names:
        _full_name += f"{' '.join(middle_names)} "
    _full_name += str(surname)
    return _full_name


def get_proper_emails(school: School, creds_file: str, token_file: str) -> t.Dict[Student, str]:
    changed_emails: t.Dict[Student, str] = {}

    creds = create_token(creds_file, token_file)
    people = build('people', 'v1', credentials=creds).people()
    for student in school.students:
        while True:
            try:
                person = people.searchDirectoryPeople(
                    readMask='names,emailAddresses,metadata',
                    sources=['DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE'],
                    query=student.full_name
                ).execute()
            except:
                print("Rate limit hit, waiting...")
                time.sleep(30)
            else:
                break
        # print(person)
        emails = [
            email['value'] for email in person['people'][0]['emailAddresses']
            if email['metadata'].get('primary')
        ]
        if emails:
            email = emails[0]
            if student.full_email.lower() != email.lower():
                changed_emails[student] = email.lower()
        else:
            print("Didn't work", student.full_name)
    return changed_emails


def email_student_dict(students: t.Sequence[Student]) -> t.Dict[str, Student]:
    return {student.email: student for student in students}


def dict_str_grade(grades: t.Sequence[Grade]) -> t.Dict[str, Grade]:
    return {str(grade.grade_num): grade for grade in grades}


def dict_str_class(classes: t.Sequence[Class]) -> t.Dict[str, Class]:
    return {str(clazz.name): clazz for clazz in classes}


def dict_str_student(students: t.Sequence[Student]) -> t.Dict[str, Student]:
    return {student.full_name: student for student in students}


def students_by_grade(school: School) -> t.Dict[Grade, t.List[Student]]:
    return {grade: grade.students for grade in school.grades}


def to_bool(val: str) -> bool:
    return str(val).lower() in ("yes", "true", "t", "1")
