import typing as t

from .core import constants


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

    @property
    def full_name(self) -> str:
        if self._full_name is None:
            self._full_name = f"{self.first_name} "
            if self.middle_names:
                self._full_name += f"{' '.join(self.middle_names)} "
            self._full_name += str(self.surname)
        return self._full_name

    @property
    def email(self) -> str:
        if self._email is None:
            self._email = self._make_email()
        return self._email

    def _make_email(self):
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

        self.students = [] if students is None else students

        self.grade = grade

    def add_student(self, student: Student):
        if student.clazz is None:
            student.clazz = self
        self.students.append(student)

    @staticmethod
    def _sort_key(student: Student):
        split = student.surname.split()
        return (
            split[-1],
            ' '.join(split[:-1])
        )

    def sort_students(self):
        self.students.sort(key=self._sort_key)


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

        self.classes = [] if classes is None else classes

    def add_class(self, clas: Class):
        if clas.grade is None:
            clas.grade = self
        self.classes.append(clas)

    @staticmethod
    def _sort_key(clazz: Class):
        return (
            int(clazz.grade_name),
            clazz.class_name
        )

    def sort_classes(self):
        self.classes.sort(key=self._sort_key)
