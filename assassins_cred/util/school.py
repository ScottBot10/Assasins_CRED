import typing as t

from ..school import Grade, Student, Class


def _unpack_students_key(student: Student):
    return (
        (
            student.clazz.grade._sort_key(student.clazz),
            student.clazz._sort_key(student)
        ) if student.clazz.grade is not None else
        Class._sort_key(student)
    )


def unpack_students(grades: t.Sequence[Grade], sort=True) -> t.List[Student]:
    students = []

    for grade in grades:
        for clazz in grade.classes:
            students.extend(clazz.students)

    if sort:
        students.sort(key=_unpack_students_key)

    return students
