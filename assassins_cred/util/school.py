from __future__ import annotations

import random
import string
import typing as t
from itertools import combinations
from typing import TYPE_CHECKING

from ..constants import code_length

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
        map(lambda x: ''.join(x), combinations(string.ascii_lowercase + string.digits + "_", code_length)))
    students = unpack_students(school.grades)
    if len(combos_left) < len(students):
        raise ValueError("There are not enough code combinations! Try increasing the length")
    for student in students:
        code = random.choice(combos_left)
        combos_left.remove(code)
        student.code = code
    return school


def unpack_students(grades: t.Sequence[Grade], sort=True) -> t.List[Student]:
    students = []

    for grade in grades:
        for clazz in grade.classes:
            students.extend(clazz.students)

    if sort:
        students.sort(key=_unpack_students_key)

    return students


def full_name(first_name: str, surname: str, middle_names=None):
    if middle_names is None:
        middle_names = []
    _full_name = f"{first_name} "
    if middle_names:
        _full_name += f"{' '.join(middle_names)} "
    _full_name += str(surname)
    return _full_name


def dict_str_grade(grades: t.Sequence[Grade]) -> t.Dict[str, Grade]:
    return {str(grade.grade_num): grade for grade in grades}


def dict_str_class(classes: t.Sequence[Class]) -> t.Dict[str, Class]:
    return {str(clazz.name): clazz for clazz in classes}


def dict_str_student(students: t.Sequence[Student]) -> t.Dict[str, Student]:
    return {student.full_name: student for student in students}


def students_by_grade(grades: t.Sequence[Grade]) -> t.Dict[Grade, t.List[Student]]:
    return {grade: unpack_students((grade,)) for grade in grades}


def to_bool(val: str) -> bool:
    return val.lower() == "true"
