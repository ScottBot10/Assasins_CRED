import random
import typing as t

from assassins_cred.school import Grade, Student, School
from assassins_cred.util.school import students_by_grade, unpack_students, dict_str_student


def shuffle_school_grade(school: School) -> School:
    by_grade = students_by_grade(school)
    shuffled = {}
    for grade, students in by_grade.items():
        values = students.copy()
        random.shuffle(values)
        mappings = list(zip(values, values[1:] + [values[0]]))
        shuffled.update(mappings)

    for grade in school.grades:
        for clazz in grade.classes:
            for student in clazz.students:
                if student in shuffled:
                    student.target = shuffled[student]

    return school


def shuffle_school_class(school: School) -> School:
    for grade in school.grades:
        for clazz in grade.classes:
            students = clazz.students.copy()
            random.shuffle(students)
            shuffled = dict(zip(students, students[1:] + [students[0]]))

            for student in clazz.students:
                student.target = shuffled[student]


def shuffle_all(school: School = None,
                grades: t.Sequence[Grade] = None,
                students: t.Sequence[Student] = None) -> t.Dict[str, Student]:
    if school is not None and grades is None and students is None:
        students = unpack_students(school.grades)
    elif grades is not None and school is None and students is None:
        students = unpack_students(grades)
    elif grades is None and students is None:
        raise Exception
    random.shuffle(values)
    shuffled = dict(zip(students, students[1:] + [students[0]]))

    for student in students:
        if student in shuffled:
            student.target = shuffled[student]

    return dict_str_student(students)
