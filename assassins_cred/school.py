import typing as t

from . import constants
from .util.school import full_name


class Student:
    """
    Simple class representing a single pupil
    """

    def __init__(self,
                 first_name: str,
                 surname: str,
                 middle_names: t.Sequence[str] = None,
                 grade_class: t.Optional = None):
        """
        :param first_name: The pupil's first name
        :param surname: The pupil's surname
        :param middle_names: The pupil's middle name
        """
        if middle_names is None:
            middle_names = []
        self.first_name = first_name
        self.middle_names = middle_names
        self.surname = surname

        self._full_name = None
        self._email = None

        self.code: t.Optional[str] = None
        self.target: t.Optional[Student] = None
        self.is_dead: bool = False
        self.has_killed: bool = False

        self.clazz: t.Optional[Class] = grade_class

    def __repr__(self):
        return self.full_name

    def __str__(self):
        return self.__repr__()

    @property
    def full_name(self) -> str:
        if self._full_name is None:
            self._full_name = full_name(self.first_name, self.surname, self.middle_names)
        return self._full_name

    @property
    def email(self) -> str:
        if self._email is None:
            self._email = self._make_email()
        return self._email

    def _make_email(self) -> str:
        return (
            f"{self.first_name[0].lower()}"
            f"{self.surname.lower().replace('-', '').replace(' ', '')}@"
            f"{constants.email_domain}"
        )


class Class:
    """
    Simple class respresenting a school class e.g. 10A 12B 8C
    """
    def __init__(self, grade_name: str, class_name: str, students: t.Optional[t.Sequence[Student]] = None,
                 grade: t.Optional = None):
        """

        :param class_name: The name class e.g: 9A, 11F
        :param students: A sequence of :class:`assassins_cred.class_grade.Student`
        """
        self.class_name = class_name
        self.grade_name = grade_name
        self.name = self.grade_name + self.class_name

        self.student_dict = {} if students is None else students

        self.grade = grade

    def add_student(self, student: Student):
        if student.clazz is None:
            student.clazz = self
        self.student_dict[student.full_name] = student

    @property
    def students(self) -> list:
        return self.student_dict.values()

    @staticmethod
    def _sort_key(student: Student):
        split = student.surname.split()
        return (
            split[-1],
            ' '.join(split[:-1])
        )

    def sort_students(self) -> None:
        self.student_dict = dict(sorted(self.student_dict.items(), key=lambda x: self._sort_key(x[1])))


class Grade:
    """
    Simple class respresenting a grade
    """

    def __init__(self, grade: int, classes: t.Optional[t.Sequence[Class]] = None):
        """

        :param grade: The grade number
        :param classes: A sequence of :class:`assassins_cred.class_grade.Class`
        """
        self.grade = grade

        self.class_dict = {} if classes is None else classes

    def add_class(self, clazz: Class):
        if clazz.grade is None:
            clazz.grade = self
        self.class_dict[clazz.name] = clazz

    @property
    def classes(self) -> list:
        return list(self.class_dict.values())

    @staticmethod
    def _sort_key(clazz: Class):
        return (
            int(clazz.grade_name),
            clazz.class_name
        )

    def sort_classes(self) -> None:
        self.class_dict = dict(sorted(self.class_dict.items(), key=lambda x: self._sort_key(x[1])))
