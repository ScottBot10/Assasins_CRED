from sqlalchemy import Column, String, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship, relation
from sqlalchemy.sql.expression import and_

from assassins_cred import school
from assassins_cred.util.shuffle import shuffle_all

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"
    code = Column(String, primary_key=True)
    first_name = Column(String)
    middle_names = Column(String)
    surname = Column(String)
    is_dead = Column(Boolean)
    has_killed = Column(Boolean)
    target_id = Column(String, ForeignKey('students.code'))
    target = relationship("Student", remote_side=[code])
    clazz = Column(String, ForeignKey("classes.clazz"))


class Clazz(Base):
    __tablename__ = "classes"
    clazz = Column(String, primary_key=True)
    grade_name = Column(String, ForeignKey("grades.grade"))


class Grade(Base):
    __tablename__ = "grades"
    grade = Column(String, primary_key=True)


def to_middle_name(middle_names: str):
    return ','.join(middle_names) if middle_names else None


def add_student(session: Session, student: school.Student):
    if not student.code:
        print("Bad Code")
        return
    check = (
        session.query(Student).join(Clazz).join(Grade)
        .filter(
            and_(
                 Student.code == student.code,
                 Student.first_name == student.first_name,
                 Student.surname == student.surname,
                 Student.middle_names == to_middle_name(student.middle_names))
                )
        .filter(student.clazz.name == Clazz.clazz)
        .filter(str(student.clazz.grade.grade_num) == Grade.grade)
        .one_or_none()
    )
    if check is not None:
        return

    grade = (
        session.query(Grade)
        .filter(
            Grade.grade == str(student.clazz.grade.grade_num)
        )
        .one_or_none()
    )

    if grade is None:
        session.add(Grade(str(student.clazz.grade.grade_num)))

    clazz = (
        session.query(Clazz)
        .filter(
            Clazz.clazz == student.clazz.name
        )
        .one_or_none()
    )

    if clazz is None:
        session.add(Clazz(clazz=student.clazz.name, grade_name=student.clazz.grade_name))

    session.add(Student(
        code=student.code,
        first_name=student.first_name,
        middle_names=student.middle_names or None,
        surname=student.surname,
        is_dead=student.is_dead,
        has_killed=student.has_killed,
        target_id=student.target.code if student.target else None,
        target=student.target or None,
        clazz=student.clazz.name or None))

    session.commit()


if __name__ == '__main__':
    db_path = "..\\..\\resources\\test.db"
    engine = create_engine(f"sqlite:///{db_path}")
    Sess = sessionmaker()
    Sess.configure(bind=engine)
    session = Sess()
    Base.metadata.create_all(engine)

    students = session.query(Student).all()
    print(students)

    grade = school.Grade(11)
    clazz = school.Class('11', 'A')

    student = school.Student("Jack", "Saunders")
    student.code = 'bb7'

    clazz.add_student(student)
    grade.add_class(clazz)

    print(student)
    add_student(session, student)
