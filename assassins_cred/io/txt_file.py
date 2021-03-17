import logging

from ..constants import TXT_FORMAT, school_name, PROJECT_ROOT
from ..school import School, Student, Grade, Class

logger = logging.getLogger("assassins_cred")

INIT_TXT_FIRST_NAME = "first_name"
INIT_TXT_LAST_NAME = "surname"
INIT_TXT_FULL_ClASS = "full_class"
INIT_TXT_GRADE = "grade"
INIT_TXT_CLASS = "class"


def setup(init, **kw):
    if 'file' in kw:
        kw['file'] = join(PROJECT_ROOT, kw['file'])
    return kw


def init_read(file: str) -> School:
    """
    Read from a txt file into :class:`assassins_cred.class_grade.Class` in the format
        Name Surname(s) Class
    :param file: The filename of the file
    :return: a Mapping: class_name to Grade
    """

    school = School(school_name)
    grades = {}
    classes = {}

    with open(file) as f:
        contents = f.read()
    for line in contents.splitlines():
        match = TXT_FORMAT.match(line)
        logger.debug(match)
        if match is not None:
            student = Student(match[INIT_TXT_FIRST_NAME], match[INIT_TXT_LAST_NAME])
            if match[INIT_TXT_GRADE] not in grades:
                grade = Grade(int(match[INIT_TXT_GRADE]))
                grades[match[INIT_TXT_GRADE]] = grade
                school.add_grade(grade)
            grade = grades[match[INIT_TXT_GRADE]]

            if match[INIT_TXT_FULL_ClASS] not in classes:
                clazz = Class(match[INIT_TXT_GRADE], match[INIT_TXT_CLASS])
                classes[match[INIT_TXT_FULL_ClASS]] = clazz
                grade.add_class(clazz)
            clazz = classes.get(match[INIT_TXT_FULL_ClASS])
            clazz.add_student(student)

    school.rsort()

    return school
