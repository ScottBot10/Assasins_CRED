import csv
import logging
from os.path import join

from .. import constants
from ..constants import school_name, PROJECT_ROOT
from ..school import School, Student, Grade, Class
from ..util.school import to_bool, full_name

logger = logging.getLogger("assassins_cred")

INIT_CSV_FIRST_NAME = "First name"
INIT_CSV_MIDDLE_NAMES = "Middle names"
INIT_CSV_LAST_NAME = "Surname"
INIT_CSV_GRADE = "Grade"
INIT_CSV_CLASS = "Class"


def setup(init, **kw):
    if 'file' in kw:
        kw['file'] = kw['file']
    return kw


def init_read(file: str) -> School:
    """
    Read from a csv file with a , delimiter into :class:`assassins_cred.class_grade.Class` in the format
        Name, Surname, Grade, Class
    :param file: The filename of the file
    :return: a Mapping: class_name to Grade
    """
    school = School(constants.school_name)
    grades = {}
    classes = {}

    with open(file) as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            student = Student(row[INIT_CSV_FIRST_NAME], row[INIT_CSV_LAST_NAME],
                              middle_names=row.get(INIT_CSV_MIDDLE_NAMES, '').split())
            if row[INIT_CSV_GRADE] not in grades.keys():
                grade = Grade(int(row[INIT_CSV_GRADE]))
                grades[row[INIT_CSV_GRADE]] = grade
                school.add_grade(grade)
            grade = grades[row[INIT_CSV_GRADE]]

            full_class = row[INIT_CSV_GRADE] + row[INIT_CSV_CLASS]

            if full_class not in classes.keys():
                clazz = Class(row[INIT_CSV_GRADE], row[INIT_CSV_CLASS])
                classes[full_class] = clazz
                grade.add_class(clazz)
            clazz = classes.get(full_class)
            clazz.add_student(student)

    school.rsort()

    return school


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

    school = School(school_name)
    grades = {}
    classes = {}
    students = {}

    rows = []

    with open(file) as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            if row[CSV_TARGET_NAME] and row[CSV_TARGET_SURNAME]:
                rows.append(row)
            student = Student(row[CSV_NAME], row[CSV_SURNAME], code=row[CSV_CODE])
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


def write_people(file: str, school: School) -> None:
    """
    Write to a csv file in the format
            name,class,email,code,target,isdead,haskilled
    :param school:
    :param file: The filename to write to
    """
    with open(file, "w", newline='') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        students = school.students
        csv_writer.writerow(constants.people_fieldnames)
        rows = [
            (
                student.first_name,
                student.surname,
                student.clazz.grade_name,
                student.clazz.class_name,
                student.code,
                student.target.first_name if student.target is not None else None,
                student.target.surname if student.target is not None else None,
                student.is_dead,
                student.has_killed
            )
            for student in students
        ]
        csv_writer.writerows(rows)
