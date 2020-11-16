# -*- coding: utf-8 -*-

# Para este proyecto, realizarás un sistema para una escuela. Este sistema permite registrar nuevos alumnos, profesores y cursos.
# Un alumno es asignado a un curso y un curso puede tener asociado más de un profesor. Los profesores tienen un horario que indica cuando están en cada curso.
# El horario asociará un curso y un profesor para un día de la semana (Lunes, Martes, Miércoles, Jueves, Viernes, Sábado, Domingo), una hora desde y una hora hasta.
# El sistema permitirá exportar los alumnos que pertenecen a un curso, el horario de cada profesor y el horario del curso.
# Subir un archivo con extensión .py con el código fuente del programa.

import csv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Table, Text
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///:memory:')

Base = declarative_base()

class Teacher(Base):
    __tablename__ = "teacher"
    id = Column(Integer, Sequence('teacher_id_seq'), primary_key=True)
    firstname = Column(String)
    lastname = Column(String)

    horarios = relationship("Schedule", back_populates="teacher")

    def __repr__(self):
        return "{} {}".format(self.firstname, self.lastname)


class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, Sequence('course_id_seq'), primary_key=True)
    name = Column(String)
    
    students = relationship("Student", order_by="Student.id", back_populates="course") # One to many

    schedules = relationship("Schedule", back_populates="course")

    def __repr__(self):
        return "{}".format(self.name)


class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, Sequence('student_id_seq'), primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    course_id = Column(Integer, ForeignKey('course.id'))
    course = relationship("Course", back_populates="students") # One to many

    def __repr__(self):
        return "{} {}".format(self.firstname, self.lastname)


class Schedule(Base):
    __tablename__ = "schedule"
    id = Column(Integer, Sequence('schedule_id_seq'), primary_key=True)
    day_of_week = Column(String)
    time_from = Column(Integer,)
    time_to = Column(Integer)

    course_id = Column(Integer, ForeignKey('course.id'))
    course = relationship("Course", back_populates="schedule")

    teacher_id = Column(Integer, ForeignKey('teacher.id'))
    teacher = relationship("Teacher", back_populates="schedules")

    def __repr__(self):
        return "{} {}, at {} on {}s from {} to {}".format(self.teacher.firstname, self.teacher.lastname, self.course.name, self.day_of_week, self.time_from, self.time_to)

class SchoolClosedError(Exception):
    pass

class TimeExceededError(Exception):
    pass

class School(object):

    def __init__(self, session, name, opening_time, closing_time):
        self.session, self.name, self.opening_time, self.closing_time = session, name, opening_time, closing_time
        return

    def name(self):
        return self.name

    def session(self):
        return self.session

    def asign_course(self, day_of_week, time_from, time_to, teacher, course):
        """Creates schedule relation between a course and a teacher-

        Args:
            day_of_week (str): when the course will be taking place.
            time_from (int): starting time (in hours) of the course.
            time_to (int): ending time (in hourse) of the course.
            teacher (Teacher): to relate to.
            course (Course): to relate to.

        Raises:
            SchoolClosedError: when given time from or to is less than school's opening time or bigger than it's closing time.
            TimeExceededError: when given 'time_from' is bigger than 'time_to'
        """
        if time_from < self.opening_time or time_to < self.opening_time or time_from > self.closing_time or time_to > self.closing_time or day_of_week in ["Saturday","Sunday"]:
            raise SchoolClosedError("Provided course is out of school's day-time range")
        if time_to < time_from:
            raise TimeExceededError("Students can't spend the night at school.")
        schedule = Schedule(day_of_week=day_of_week, time_from=time_from, time_to=time_to)
        schedule.course = course
        schedule.teacher = teacher
        self.register([schedule])
        return

    def register(self, objs:list):
        """Adds given objects to database.

        Args:
            objs (list): any type of sql objects.
        """
        self.session.add_all(objs)
        return

    def enroll_student(self, student:Student, course:Course):
        """Asigns a student to a course.

        Args:
            student (Student): to asign to course.
            course (Course): to asing student.
        """
        student.course = course
        return

    def courses(self):
        return self.session.query(Course).all()

    def teachers(self):
        """Query for all teachers.

        Returns:
            list: containing all teachers.
        """
        return self.session.query(Teacher).all()

    def students(self):
        """Query for all students.

        Returns:
            list: containing all students.
        """
        return self.session.query(Student).all()

    def course_s_students(self, course:Course):
        """Query for course's students.

        Args:
            course (Course): to look for.

        Returns:
            list: containing course's students.
        """
        return self.session.query(Student).filter(Student.course_id==course.id).all()

    def teacher_s_schedules(self, teacher:Teacher):
        """Query for teacher's schedule.

        Args:
            course (Course): to look for.

        Returns:
            list: containing teacher's schedule.
        """
        return self.session.query(Schedule).filter(Schedule.teacher_id==teacher.id).order_by(Schedule.day_of_week).all()

    def course_s_schedules(self, course:Course):
        """Query for course's schedule.

        Args:
            course (Course): to look for.

        Returns:
            list: containing course's schedule.
        """
        return self.session.query(Schedule).filter(Schedule.course_id==course.id).order_by(Schedule.day_of_week).all()

    def export_students(self, course:Course, name=None):
        """Prepares a list of students enrolled to given course to export them in .csv format.

        Args:
            course (Course): to look students for.
            name (str, optional): to name the file. Defaults to None.

        Returns:
            bool: True when finished.
        """
        students = self.course_s_students(course)
        students = [[student.id, student.firstname, student.lastname] for student in students]
        name = name if name != None else course.name
        return self.exportar(students, ["id", "nombre", "apellido"], name)

    def export_teacher_schedules(self, teacher:Teacher, name=None):
        """Prepares teacher's schedules to export them in .csv format.

        Args:
            teacher (Teacher): to look schedules for.
            name (str, optional): to name the file. Defaults to None.

        Returns:
            bool: True when finished.
        """
        schedules = self.teacher_s_schedules(teacher)
        schedules = [[s.id, s.day_of_week, s.time_from, s.time_to, s.course.name] for s in schedules]
        name = name if name != None else "{}_{}".format(teacher.firstname, teacher.lastname)
        return self.exportar(schedules, ["id", "day_of_week", "from", "to", "course"], name)

    def export_course_schedule(self, course:Course, name=None):
        """Prepares course's schedules to export them in .csv format.

        Args:
            course (Course): to look schedules for.
            name (str, optional): to name the file. Defaults to None.

        Returns:
            bool: True when finished.
        """
        # Selects course's schedules
        schedules = self.course_s_schedules(course)
        schedules = [[s.id, s.day_of_week, s.time_from, s.time_to, s.teacher.firstname, s.teacher.lastname] for s in schedules]
        name = name if name != None else course.name
        return self.exportar(schedules, ["id", "dia_de_la_semana", "inicio", "fin", "nombre_profesor","apellido_profesor"], name)

    def exportar(self, iterable:list, title:list, name=None):
        """Generates a .csv file.

        Args:
            iterable (list): List of list to iterate for csv generation.
            name (str, optional): Output .csv's file name. Defaults to None.

        Returns:
            bool: Wether the write operation was successful.
        """
        with open('{}.csv'.format(name), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(title)
            writer.writerows(iterable)
        return True

    def delete(self, obj):
        return self.session.delete(obj)

    def guardar(self):
        self.session.commit()
        return

    def __repr__(self):
        return self.name

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Dejó acá ejemplos para probar:

school = School(session, "Pirates of The Caribbean School",8,16)

course_2_A = Course(name="Course 2A Morning")
course_3_A = Course(name="Course 3A Morning")
course_3_B = Course(name="Course 3B Afternoon")


student_a = Student(firstname="s_firstname_a", lastname="s_lastname_a")
student_b = Student(firstname="s_firstname_b", lastname="s_lastname_b")
student_c = Student(firstname="s_firstname_c", lastname="s_lastname_c")
student_d = Student(firstname="s_firstname_d", lastname="s_lastname_d")
student_e = Student(firstname="s_firstname_e", lastname="s_lastname_e")
student_f = Student(firstname="s_firstname_f", lastname="s_lastname_f")
student_g = Student(firstname="s_firstname_g", lastname="s_lastname_g")
student_h = Student(firstname="s_firstname_h", lastname="s_lastname_h")
student_i = Student(firstname="s_firstname_i", lastname="s_lastname_i")
student_j = Student(firstname="s_firstname_j", lastname="s_lastname_j")
student_k = Student(firstname="s_firstname_k", lastname="s_lastname_k")


teacher_a = Teacher(firstname="t_firstname_a", lastname="t_lastname_a")
teacher_b = Teacher(firstname="t_firstname_b", lastname="t_lastname_b")
teacher_c = Teacher(firstname="t_firstname_c", lastname="t_lastname_c")
teacher_d = Teacher(firstname="t_firstname_d", lastname="t_lastname_d")
teacher_e = Teacher(firstname="t_firstname_e", lastname="t_lastname_e")
teacher_f = Teacher(firstname="t_firstname_f", lastname="t_lastname_f")


student_a.curso = course_2_A
student_b.curso = course_2_A
student_c.curso = course_2_A
student_d.curso = course_2_A
student_e.curso = course_3_A
student_f.curso = course_3_A
student_g.curso = course_3_A
student_h.curso = course_3_B
student_i.curso = course_3_B
student_j.curso = course_3_B   
student_k.curso = course_3_B

school.register([course_2_A, course_3_A, course_3_B])
school.session.commit()

school.asign_course("Monday", 8, 10, teacher_a, course_2_A)
school.asign_course("Tuesday", 10, 12, teacher_b, course_2_A)
school.asign_course("Wednesday", 14, 16, teacher_a, course_2_A)
school.asign_course("Monday", 8, 10, teacher_c, course_2_A)
school.asign_course("Monday", 14, 15, teacher_a, course_2_A)
school.asign_course("Monday", 9, 11, teacher_b, course_3_A)
school.asign_course("Wednesday", 8, 10, teacher_a, course_3_A)
school.asign_course("Tuesday", 8, 10, teacher_a, course_3_A)
school.asign_course("Friday", 8, 10, teacher_a, course_3_A)
school.asign_course("Saturday", 8, 10, teacher_a, course_3_A)
school.asign_course("Monday", 8, 10, teacher_d, course_3_A)

school.course_s_students(course_2_A)
school.export_students(course_2_A, "{} -students".format(course_2_A.name))

school.teacher_s_schedules(teacher_a)
school.export_teacher_schedules(teacher_a,"{}_{}".format(teacher_a.firstname, teacher_a.lastname))

school.course_s_schedules(course_2_A)
school.export_course_schedule(course_2_A,course_2_A.name)

