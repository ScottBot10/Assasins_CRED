import typing as t

Grade = t.Any
Student = t.Any
Class = t.Any


def _unpack_students_key(student):
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


def full_name(first_name: str, surname: str, middle_names=None):
    if middle_names is None:
        middle_names = []
    _full_name = f"{first_name} "
    if middle_names:
        _full_name += f"{' '.join(middle_names)} "
    _full_name += str(surname)
    return _full_name


def dict_str_grade(grades: t.Sequence[Grade]) -> t.Dict[str, Grade]:
    return {str(grade.grade): grade for grade in grades}


def students_by_grade(grades: t.Sequence[Grade]) -> t.Dict[Grade, t.List[Student]]:
    return {grade: unpack_students((grade,)) for grade in grades}


def to_bool(val: str) -> bool:
    return val.lower() == "true"
