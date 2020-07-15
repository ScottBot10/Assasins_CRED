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
    def __init__(self, grade_name: str, class_name: str, students: t.Optional[t.Dict[str, Student]] = None,
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

    def remove_student(self, student: Student):
        for name, _student in self.student_dict.copy().items():
            if _student == student:
                self.student_dict.pop(name)
                return
        raise ValueError(f"{student} is not in the class")

    @property
    def students(self) -> t.List[Student]:
        return list(self.student_dict.values())

    @staticmethod
    def _sort_key(student: Student):
        split = student.surname.split()
        return (
            split[-1],
            ' '.join(split[:-1])
        )

    def sort(self, key=None) -> None:
        key = key or self._sort_key
        self.student_dict = dict(sorted(self.student_dict.items(), key=lambda x: key(x[1])))


class Grade:
    """
    Simple class respresenting a grade
    """

    def __init__(self, grade: int, classes: t.Optional[t.Dict[str, Class]] = None, school: t.Optional = None):
        """

        :param grade: The grade number
        :param classes: A sequence of :class:`assassins_cred.class_grade.Class`
        """
        self.grade_num = grade

        self.class_dict: t.Dict[str, Class] = {} if classes is None else classes

        self.school = school

    def add_class(self, clazz: Class):
        if clazz.grade is None:
            clazz.grade = self
        self.class_dict[clazz.name] = clazz

    def remove_class(self, clazz: Class):
        for name, _clazz in self.class_dict.copy().items():
            if _clazz == clazz:
                self.class_dict.pop(name)
                return
        raise ValueError(f"{clazz} is not in the class")

    @property
    def classes(self) -> t.List[Class]:
        return list(self.class_dict.values())

    @staticmethod
    def _sort_key(clazz: Class):
        return (
            int(clazz.grade_name),
            clazz.class_name
        )

    def sort(self, key=None) -> None:
        key = key or self._sort_key
        self.class_dict = dict(sorted(self.class_dict.items(), key=lambda x: key(x[1])))

    def rsort(self, key=None) -> None:
        key = key or self._sort_key
        for clazz in self.classes:
            clazz.sort()
        self.sort(key)


class School:
    def __init__(self, name: str, grades: t.Optional[t.Dict[str, Grade]] = None):
        self.name = name

        self.grade_dict: t.Dict[str, Grade] = {} if grades is None else grades

    def add_grade(self, grade: Grade):
        if grade.school is None:
            grade.school = self
        self.grade_dict[grade.grade_num] = grade

    @property
    def grades(self) -> t.List[Grade]:
        return list(self.grade_dict.values())

    @staticmethod
    def _sort_key(grade: Grade):
        return grade.grade_num

    def sort(self, key=None) -> None:
        """
        Sorts the grades
        """
        key = key or self._sort_key
        self.grade_dict = dict(sorted(self.grade_dict.items(), key=lambda x: key(x[1])))

    def rsort(self, key=None) -> None:
        """
        Sorts the grade, classes and students
        """
        key = key or self._sort_key
        for grade in self.grades:
            grade.rsort()
        self.sort(key)
