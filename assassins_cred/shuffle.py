import random
import typing as t

from .school import Grade
from .util.school import students_by_grade, dict_str_grade


def shuffle_by_grade(grades: t.Sequence[Grade]) -> t.Dict[str, Grade]:
    shuffled = {}
    by_grade = students_by_grade(list(grades))

    for grade, students in by_grade.items():
        values = students.copy()
        random.shuffle(values)
        mappings = list(zip(values, values[1:] + [values[0]]))
        shuffled.update(mappings)

    for grade in grades:
        for clazz in grade.classes:
            for student in clazz.students:
                if student in shuffled:
                    student.target = shuffled[student]

    return dict_str_grade(grades)
