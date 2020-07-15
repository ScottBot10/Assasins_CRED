import csv

from ...school import Grade, Student, Class, School
from ...util.school import full_name, to_bool

CSV_NAME = "name"
CSV_SURNAME = "surname"
CSV_GRADE = "grade"
CSV_CLASS = "class"
CSV_CODE = "code"
CSV_TARGET_NAME = "target_name"
CSV_TARGET_SURNAME = "target_surname"
CSV_IS_DEAD = "is_dead"
CSV_HAS_KILLED = "has_killed"


def read_people(file: str) -> School:
    """
    Read from a csv file with a , delimiter into :class:`assassins_cred.class_grade.Class` in the format
        name,surname,grade,class,code,target,is_dead,has_killed
    :param file: The filename of the file
    :return: a Mapping: class_name to Grade
    """

    school = School("westerford")
    grades = {}
    classes = {}
    students = {}

    rows = []

    with open(file) as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            if row[CSV_TARGET_NAME] and row[CSV_TARGET_SURNAME]:
                rows.append(row)
            student = Student(row[CSV_NAME], row[CSV_SURNAME])
            student.code = row[CSV_CODE]
            student.is_dead = to_bool(row[CSV_IS_DEAD])
            student.has_killed = to_bool(row[CSV_HAS_KILLED])

            students[student.full_name] = student

            if row[CSV_GRADE] not in grades.keys():
                grade = Grade(int(row[CSV_GRADE]))
                grades[row[CSV_GRADE]] = grade
                school.add_grade(grade)
            grade = grades[row[CSV_GRADE]]

            full_class = row[CSV_GRADE] + row[CSV_CLASS]

            if full_class not in classes.keys():
                clazz = Class(row[CSV_GRADE], row[CSV_CLASS])
                classes[full_class] = clazz
                grade.add_class(clazz)
            clazz = classes.get(full_class)
            clazz.add_student(student)

    for row in rows:
        student_name = full_name(row[CSV_NAME], row[CSV_SURNAME])
        student = students[student_name]
        target_name = full_name(row[CSV_TARGET_NAME], row[CSV_TARGET_SURNAME])
        student.target = students[target_name]

    school.rsort()
    return school
