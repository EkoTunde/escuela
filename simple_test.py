from school import * 


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


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

