from os.path import join

import gspread

from .. import constants, config
from ..school import School, Grade, Class, Student
from ..util.google import create_token

SCOPE = ['https://www.googleapis.com/auth/spreadsheets.readonly']

FORM_EMAIL = "Email address"
FORM_NAME = "Name and Surname"
FORM_FULL_CLASS = "Grade and Class (e.g 12B, 8C)"
FORM_PARTICIPATE = "Do you want to participate?"


def setup(init, **kw):
    if 'file' in kw:
        kw['file'] = join(constants.PROJECT_ROOT, kw['file'])
    return kw


def init_read(creds_file: str, token_file: str, sheet_id: str) -> School:
    school = School(constants.school_name)
    grades = {}
    classes = {}

    creds = create_token(join(constants.PROJECT_ROOT, creds_file),
                         join(constants.PROJECT_ROOT, token_file), scopes=SCOPE)
    gc = gspread.authorize(creds)

    sheet = gc.open_by_key(sheet_id).sheet1
    people = sheet.get_all_records()
    for person in people:
        if person[FORM_PARTICIPATE].lower() == 'yes':
            name_match = constants.NAME_FORMAT.match(person[FORM_NAME])
            if name_match is not None:
                class_match = constants.CLASS_FORMAT.match(person[FORM_FULL_CLASS])
                if class_match is not None:
                    student = Student(name_match["first_name"], name_match["surname"])
                    grade_num = class_match["grade"]
                    if grade_num not in grades:
                        grade = Grade(int(grade_num))
                        grades[grade_num] = grade
                        school.add_grade(grade)
                    grade = grades[grade_num]

                    if class_match["full_class"] not in classes:
                        clazz = Class(class_match["grade"], class_match["class"])
                        classes[class_match["full_class"]] = clazz
                        grade.add_class(clazz)
                    clazz = classes[class_match["full_class"]]
                    clazz.add_student(student)
    school.rsort()

    return school
