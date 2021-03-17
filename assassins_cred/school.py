import logging
import typing as t

from . import constants, config
from .util.school import full_name

logger = logging.getLogger("assassins_cred")


class Student:
    """
    Simple class representing a single pupil
    """

    def __init__(self,
                 first_name: str,
                 surname: str,
                 middle_names: t.Sequence[str] = None,
                 email: t.Optional[str] = None,
                 clazz: t.Optional = None,
                 code: t.Optional[str] = None):
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
        self._email = email

        self.code: t.Optional[str] = code
        self.target: t.Optional[Student] = None
        self.is_dead: bool = False
        self.has_killed: bool = False

        self.clazz = clazz
        if isinstance(self.clazz, Class):
            self.clazz.add_student(self)

    def __eq__(self, other):
        return all((
            self.code == other.code,
            self.first_name == other.first_name,
            self.middle_names == other.middle_names,
            self.surname == other.surname,
            self.target == other.target,
            self.is_dead == other.is_dead,
            self.has_killed == other.has_killed,
            self.clazz == other.clazz,
        ))

    def short_eq(self, other):
        return all((
            getattr(self, 'code', None) == getattr(other, 'code', None),
            getattr(self, 'first_name', None) == getattr(other, 'first_name', None),
            getattr(self, 'middle_names', None) == getattr(other, 'middle_names', None),
            getattr(self, 'surname', None) == getattr(other, 'surname', None)
        ))

    def _to_str(self):
        return (f"{self.__class__.__qualname__}("
                f"name='{self.full_name}', "
                f"code='{self.code}', "
                f"target={self.target.full_name if self.target is not None else None}, "
                f"is_dead={self.is_dead}, "
                f"has_killed={self.has_killed})")

    def __repr__(self):
        return f"<{self._to_str()}>"

    def __str__(self):
        return self._to_str()

    def __hash__(self):
        return hash(repr(self))

    @property
    def full_name(self) -> str:
        if self._full_name is None:
            self._full_name = full_name(self.first_name, self.surname, self.middle_names)
        return self._full_name

    @property
    def email(self) -> str:
        email = self._email
        if email is None:
            email = self._make_email()
        return email

    @property
    def full_email(self) -> str:
        return self.email + f"@{config.email.domain}"

    def _make_email(self, with_domain=False) -> str:
        email = (
            f"{self.first_name[0].lower()}"
            f"{self.surname.lower().replace('-', '').replace(' ', '')}"
        )
        email += f"@{config.email.domain}" if with_domain else ''
        return email


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

        self.student_dict = {} if students is None else students

        self.grade: Grade = grade

    def __eq__(self, other):
        return all((
            getattr(self, 'class_name', None) == getattr(other, 'class_name', None),
            getattr(self, 'grade_name', None) == getattr(other, 'grade_name', None),
            getattr(self, 'grade', None) == getattr(other, 'grade', None)
        ))

    def _to_str(self):
        return f"{self.__class__.__qualname__}({self.name})"

    def __repr__(self):
        return f"<{self._to_str()}>"

    def __str__(self):
        return self._to_str()

    def __hash__(self):
        return hash(repr(self))

    def add_student(self, student: Student):
        if student.full_name in self.student_dict:
            return
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
    def name(self):
        return self.grade_name + self.class_name

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

    def __init__(self, grade: str, classes: t.Optional[t.Dict[str, Class]] = None, school: t.Optional = None):
        """

        :param grade: The grade number
        :param classes: A sequence of :class:`assassins_cred.class_grade.Class`
        """
        self.grade = grade

        self.class_dict: t.Dict[str, Class] = {} if classes is None else classes

        self.school = school

    def __eq__(self, other):
        return getattr(self, 'grade', None) == getattr(other, 'grade', None)

    def _to_str(self):
        return f"{self.__class__.__qualname__}({self.grade})"

    def __repr__(self):
        return f"<{self._to_str()}>"

    def __str__(self):
        return self._to_str()

    def __hash__(self):
        return hash(repr(self))

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

    @property
    def students(self) -> t.List[Student]:
        students = []

        for clazz in self.classes:
            students.extend(clazz.students)

        return students

    def rsort(self, key=None) -> None:
        key = key or self._sort_key
        for clazz in self.classes:
            clazz.sort()
        self.sort(key)


class School:
    def __init__(self, name: str, grades: t.Optional[t.Dict[str, Grade]] = None):
        self.name = name

        self.grade_dict: t.Dict[str, Grade] = {} if grades is None else grades

        logger.debug(f"New school created: {self.name}")

    def __eq__(self, other):
        return all((
            getattr(self, 'name', None) == getattr(other, 'name', None),
            getattr(self, 'grades', None) == getattr(other, 'grades', None)
        ))

    def add_grade(self, grade: Grade):
        if grade.school is None:
            grade.school = self
        self.grade_dict[grade.grade] = grade

    @property
    def grades(self) -> t.List[Grade]:
        return list(self.grade_dict.values())

    @staticmethod
    def _sort_key(grade: Grade):
        return grade.grade

    def sort(self, key=None) -> None:
        """
        Sorts the grades
        """
        key = key or self._sort_key
        self.grade_dict = dict(sorted(self.grade_dict.items(), key=lambda x: key(x[1])))

    @property
    def students(self) -> t.List[Student]:
        students = []

        for grade in self.grades:
            students.extend(grade.students)

        return students

    def rsort(self, key=None) -> None:
        """
        Sorts the grade, classes and students
        """
        key = key or self._sort_key
        for grade in self.grades:
            grade.rsort()
        self.sort(key)
