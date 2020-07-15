import csv

from ... import constants
from ...school import School
from ...util.school import unpack_students


def write_people(school: School, file: str) -> None:
    """
    Write to a csv file in the format
            name,class,email,code,target,isdead,haskilled
    :param school:
    :param file: The filename to write to
    """
    with open(file, "w", newline='') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        students = unpack_students(school.grades)
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
