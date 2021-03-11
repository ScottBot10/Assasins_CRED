import random
import typing as t

from ..school import Grade, Student, School
from ..util.school import students_by_grade, dict_str_student
from ..constants import school_name


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
        students = school.students
    elif grades is not None and school is None and students is None:
        students = School(name=school_name).students
    elif grades is None and students is None:
        raise Exception
    students = students.copy()
    random.shuffle(students)
    shuffled = dict(zip(students, students[1:] + [students[0]]))

    for student in students:
        if student in shuffled:
            student.target = shuffled[student]

    return dict_str_student(students)
