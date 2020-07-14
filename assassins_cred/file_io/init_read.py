import csv
import re
import typing as t

from ..school import Student, Class, Grade

TXT_FORMAT = re.compile(r"([a-zA-Z()-]+) ([a-zA-Z() -]+) ((\d{1,3})([A-Z]))")
TXT_MATCH_LEN = 5
TXT_FIRST_NAME = 0
TXT_LAST_NAME = 1
TXT_FULL_ClASS = 2
TXT_GRADE = 3
TXT_CLASS = 4


def from_txt(file: str) -> t.Dict[str, Grade]:
    """
    Read from a txt file into :class:`assassins_cred.class_grade.Class` in the format
        Name Surname(s) Class
    :param file: The filename of the file
    :return: a Mapping: class_name to Grade
    """

    grades = {}
    classes = {}

    with open(file) as f:
        contents = f.read()

    matches = TXT_FORMAT.findall(contents)
    for match in matches:
        if len(match) == TXT_MATCH_LEN and all(match):
            student = Student(match[TXT_FIRST_NAME], match[TXT_LAST_NAME])
            if match[TXT_GRADE] not in grades.keys():
                grades[match[TXT_GRADE]] = Grade(int(match[TXT_GRADE]))
            grade = grades[match[TXT_GRADE]]

            if match[TXT_FULL_ClASS] not in classes.keys():
                clazz = Class(match[TXT_GRADE], match[TXT_CLASS])
                classes[match[TXT_FULL_ClASS]] = clazz
                grade.add_class(clazz)
            clazz = classes.get(match[TXT_FULL_ClASS])
            clazz.add_student(student)

    for grade in grades.values():
        grade.sort_classes()
        for clazz in grade.classes:
            clazz.sort_students()

    return grades


CSV_FIRST_NAME = "First name"
CSV_LAST_NAME = "Surname"
CSV_GRADE = "Grade"
CSV_CLASS = "Class"


def from_csv(file: str) -> t.Dict[str, Grade]:
    """
    Read from a csv file with a , delimiter into :class:`assassins_cred.class_grade.Class` in the format
        Name, Surname, Grade, Class
    :param file: The filename of the file
    :return: a Mapping: class_name to Grade
    """

    grades = {}
    classes = {}

    with open(file) as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            student = Student(row[CSV_FIRST_NAME], row[CSV_LAST_NAME])
            if row[CSV_GRADE] not in grades.keys():
                grades[row[CSV_GRADE]] = Grade(int(row[CSV_GRADE]))
            grade = grades[row[CSV_GRADE]]

            full_class = row[CSV_GRADE] + row[CSV_CLASS]

            if full_class not in classes.keys():
                clazz = Class(row[CSV_GRADE], row[CSV_CLASS])
                classes[full_class] = clazz
                grade.add_class(clazz)
            clazz = classes.get(full_class)
            clazz.add_student(student)
    for grade in grades.values():
        grade.sort_classes()
        for clazz in grade.classes:
            clazz.sort_students()

    return grades
