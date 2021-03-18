import typing as t

from sqlalchemy import Column, String, Boolean, ForeignKey, create_engine
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

from assassins_cred import school, logger
from assassins_cred.constants import CLASS_FORMAT, school_name
from assassins_cred.util.school import full_name

Base = declarative_base()


class Grade(school.Grade, Base):
    __tablename__ = "grades"
    grade = Column(String, primary_key=True)
    classes = relationship("Class", backref="grade")

    def __init__(self, grade: str, classes: t.Optional[t.Dict[str, 'Class']] = None, school: t.Optional = None,
                 **kwargs):
        super().__init__(grade, classes, school)
        cls_ = type(self)
        for k in kwargs:
            if not hasattr(cls_, k):
                raise TypeError(
                    "%r is an invalid keyword argument for %s" % (k, cls_.__name__)
                )
            setattr(self, k, kwargs[k])

    @orm.reconstructor
    def init_on_load(self):
        self.school = None
        self.class_dict = {clazz.name: clazz for clazz in self.classes}

    @classmethod
    def from_school(cls, from_school: school.Grade):
        return cls(
            from_school.grade,
            classes=from_school.class_dict,
            school=school
        )

    @classmethod
    def from_school_recurse(cls, from_school: school.Grade):
        grade = cls(
            from_school.grade,
            school=school
        )
        grade.class_dict = {
            name: (Class.from_school_recurse(clazz, grade) if not isinstance(clazz, Class) else clazz)
            for name, clazz in from_school.class_dict.items()
        }
        return grade

    @property
    def class_dict(self):
        return {clazz.name: clazz for clazz in self.classes}

    @class_dict.setter
    def class_dict(self, value):
        self.classes = list(value.values())

    def add_class(self, clazz: 'Class'):
        if clazz.name in self.class_dict:
            return
        if not isinstance(clazz, Class):
            clazz = Class.from_school(clazz, self)
        else:
            clazz.grade = self
        self.class_dict = {**self.class_dict, clazz.name: clazz}

    def remove_class(self, clazz: 'Class'):
        if not isinstance(clazz, Class):
            clazz = Class.from_school(clazz, self)
        else:
            clazz.grade = self
        self.class_dict = {
            name: clasz for name, clasz in self.class_dict.items()
            if clasz != clazz
        }

    def check(self, session):
        return (
            session.query(Grade)
                .filter(Grade == self)
                .one_or_none()
        )

    def update(self, other: 'Grade'):
        columns = ('grade', 'classes')
        for column in columns:
            if hasattr(other, column) and hasattr(self, column):
                c_self, c_other = getattr(other, self), getattr(other, column)
                if c_other != c_self:
                    setattr(self, column, c_other)


class Class(school.Class, Base):
    __tablename__ = "classes"
    name = Column(String, primary_key=True)
    students = relationship("Student", backref="clazz")

    grade_name = Column(String, ForeignKey("grades.grade"))

    def __init__(self, name: str, students: t.Optional[t.Dict[str, 'Student']] = None,
                 grade: t.Optional = None, **kwargs):
        grade_name, class_name = self.get_names(name)
        super().__init__(grade_name, class_name, students, grade)
        self.name = name
        cls_ = type(self)
        for k in kwargs:
            if not hasattr(cls_, k):
                raise TypeError(
                    "%r is an invalid keyword argument for %s" % (k, cls_.__name__)
                )
            setattr(self, k, kwargs[k])

    def get_names(self, name):
        match = CLASS_FORMAT.match(name)
        if match is None:
            return
        return match.group('grade'), match.group('class')

    @orm.reconstructor
    def init_on_load(self):
        self.grade_name, self.class_name = self.get_names(self.name)

    @property
    def student_dict(self):
        return {student.full_name: student for student in self.students}

    @student_dict.setter
    def student_dict(self, value):
        self.students = list(value.values())

    def add_student(self, student: 'Student'):
        if not isinstance(student, Student):
            student = Student.from_school(student, self)
        else:
            student.clazz = self
        self.student_dict = {**self.student_dict, student.full_name: student}

    def remove_student(self, student: 'Student'):
        if not isinstance(student, Student):
            student = Student.from_school(student, self)
        else:
            student.clazz = self
        self.student_dict = {
            name: student_ for name, student_ in self.student_dict.items()
            if student_ != student
        }

    @classmethod
    def from_school(cls, from_class: school.Class):
        return cls(
            from_class.name,
            students=from_class.student_dict,
            grade=from_class.grade
        )

    @classmethod
    def from_school_recurse(cls, from_class: school.Class, from_grade: Grade):
        clazz = cls(
            from_class.name,
            grade=from_grade
        )
        clazz.students = [Student.from_school(student, clazz) for student in from_class.student_dict.values()]
        return clazz

    def check(self, session):
        return (
            session.query(Class)
                .filter(Class == self)
                .one_or_none()
        )


class Student(school.Student, Base):
    __tablename__ = "students"
    code = Column(String, primary_key=True)
    first_name = Column(String)
    middle_names = Column(String)
    surname = Column(String)
    is_dead = Column(Boolean)
    has_killed = Column(Boolean)

    target_code = Column(String, ForeignKey('students.code'))
    target = relationship("Student", remote_side=[code], post_update=True)

    class_name = Column(String, ForeignKey("classes.name"))
    _email = Column("email", String)

    def __init__(self, first_name: str, surname: str, middle_names: str = '', email: t.Optional[str] = None,
                 clazz: t.Optional = None, code: t.Optional[str] = None, **kwargs):
        super().__init__(first_name, surname, middle_names, email, clazz, code)
        cls_ = type(self)
        for k in kwargs:
            if not hasattr(cls_, k):
                raise TypeError(
                    "%r is an invalid keyword argument for %s" % (k, cls_.__name__)
                )
            setattr(self, k, kwargs[k])

    @orm.reconstructor
    def init_on_load(self):
        self._full_name = None
        self.clazz.add_student(self)

    def __hash__(self):
        return hash(repr(self))

    @property
    def full_name(self) -> str:
        mid = self.middle_names.split(',')
        self._full_name = full_name(self.first_name, self.surname, [] if mid == [''] else mid)
        return self._full_name

    @classmethod
    def from_school(cls, from_student: school.Student, clazz: Class):
        return cls(
            from_student.first_name,
            from_student.surname,
            ','.join(from_student.middle_names),
            code=from_student.code,
            clazz=clazz
        )

    def check(self, session):
        return (
            session.query(Student).join(Class).join(Grade)
                .filter(Student == self)
                .filter(Student.clazz == self.clazz)
                .filter(Grade == self.clazz.grade)
                .one_or_none()
        )

    def update(self, other: 'Student'):
        columns = ('code', 'first_name', 'middle_names', 'surname', 'is_dead', 'has_killed', 'target', 'clazz')
        for column in columns:
            if hasattr(other, column) and hasattr(self, column):
                c_self, c_other = getattr(other, self), getattr(other, column)
                if c_other != c_self:
                    setattr(self, column, c_other)


def setup(init, **kw):
    file = kw.pop('file', ':memory:')
    file = file if file == ':memory:' else '/' + file
    engine = create_engine(f"sqlite://{file}")
    Sess = sessionmaker()
    Sess.configure(bind=engine)
    session = Sess()
    if init:
        Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return {'session': session, **kw}


def write_people(session: Session, school: school.School):
    for grade in school.grades:
        if not isinstance(grade, Grade):
            grade = Grade.from_school_recurse(grade)
        grade_check = grade.check(session)
        if grade_check is None:
            session.add(grade)
    session.commit()


def read_people(session: Session):
    grades = session.query(Grade).all()

    return school.School(school_name, grades={grade.grade: grade for grade in grades})


def add_single_student(session: Session, student: Student):
    if None in (student.clazz, student.code):
        logger.error("Tried to add students to database without a class or code")
        return
    student_check = student.check(session)
    if student_check is not None:
        student_check.update(student)
        return
    if student.clazz.grade.check(session) is None:
        session.add(student.clazz.grade)
    if student.clazz.check(session) is None:
        session.add(student.clazz)

    session.add(student)


if __name__ == '__main__':
    db_path = "..\\..\\resources\\test.db"
    engine = create_engine(f"sqlite:///{db_path}")
    Sess = sessionmaker()
    Sess.configure(bind=engine)
    session = Sess()


    def create_all():
        grade = Grade('11')
        clazz = Class('11A')

        scott = Student("Scott", "Faurholm", code='aa7')
        jack = Student("Jack", "Saunders", code='bb7')
        malik = Student("Malik", "Cristie", code='cc7')

        students = [scott, jack, malik]
        students = {student.full_name: student for student in students}

        grade.add_class(clazz)

        print(students)
        for student in students.values():
            clazz.student_dict[student.full_name] = student
            add_single_student(session, student)
        session.commit()


    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    # create_all()
